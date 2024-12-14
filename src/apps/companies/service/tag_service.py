from apps.companies.dto import CompanyTagNameDto
from apps.companies.model import CompanyTag
from apps.companies.repository.company_tag_repository import CompanyTagRepository
from apps.search.model import KeywordTag
from apps.search.repository.keyword_tag_repository import KeywordTagRepository


class TagService:
    def __init__(
        self,
        company_tag_repository: CompanyTagRepository,
        keyword_tag_repository: KeywordTagRepository,
    ):
        self.company_tag_repository = company_tag_repository
        self.keyword_tag_repository = keyword_tag_repository

    def associate_tags_to_company(self, company_id: int, tags: list[CompanyTagNameDto]):
        unique_tags = []
        for tag in tags:
            for name in tag.tag_name.values():
                if name not in unique_tags:
                    unique_tags.append(name)

        check_exists_tags: list[KeywordTag] = (
            self.keyword_tag_repository.get_tags_by_names(unique_tags)
        )
        tag_name_dict = {tag.tag_name: tag.id for tag in check_exists_tags}

        new_keyword_tags = []
        for tag in unique_tags:
            if tag not in tag_name_dict:
                new_keyword_tags.append(KeywordTag(tag_name=tag))
        if new_keyword_tags:
            self.keyword_tag_repository.save_bulk(new_keyword_tags, commit=True)
            check_add_tags = self.keyword_tag_repository.get_tags_by_names(
                [tag.tag_name for tag in new_keyword_tags]
            )
            tag_name_dict.update({tag.tag_name: tag.id for tag in check_add_tags})

        new_company_tags = []

        exist_tags = self.company_tag_repository.find_all_by(
            CompanyTag.company_id == company_id,
            CompanyTag.tag_id.in_(tag_name_dict.values()),
        )
        exist_tag_ids = []
        if exist_tags:
            exist_tag_ids = [tag.tag_id for tag in exist_tags]

        for tag in tags:
            for lang, name in tag.tag_name.items():
                if tag_name_dict[name] in exist_tag_ids:
                    continue

                new_company_tags.append(
                    CompanyTag(
                        company_id=company_id, tag_id=tag_name_dict[name], lang=lang
                    )
                )

        self.company_tag_repository.save_bulk(new_company_tags, commit=True)

        return True

    def get_tags_and_lang(self, company_id: int, lang: str) -> list[str]:
        tags = self.company_tag_repository.get_company_tags_by_lang(company_id, lang)
        return tags

    def find_tag(self, tag_name: str) -> list[KeywordTag]:
        tags: list[KeywordTag] = self.keyword_tag_repository.find_all_by(
            KeywordTag.tag_name == tag_name
        )
        return tags

    def dissociate_tags_to_company(self, company_id: int, tag_ids: list[KeywordTag]):
        tag_ids = [tag.id for tag in tag_ids]
        self.company_tag_repository.delete_all_by(
            CompanyTag.company_id == company_id,
            CompanyTag.tag_id.in_(tag_ids),
        )
