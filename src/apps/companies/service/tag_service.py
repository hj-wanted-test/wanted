from collections import defaultdict

from apps.companies.dto import CompanyTagNameDto
from apps.companies.model import Company, Tag, TagLang
from apps.companies.repository.company_tag_repository import CompanyTagRepository
from apps.companies.repository.tag_repository import TagRepository
from apps.search.model import KeywordTag
from apps.search.repository.keyword_tag_repository import KeywordTagRepository


class TagService:
    def __init__(
        self,
        tag_repository: TagRepository,
        company_tag_repository: CompanyTagRepository,
        keyword_tag_repository: KeywordTagRepository,
    ):
        self.tag_repository = tag_repository
        self.company_tag_repository = company_tag_repository
        self.keyword_tag_repository = keyword_tag_repository

    def check_tag_exists(self, tags: list[CompanyTagNameDto]) -> list[Tag]:
        tags = self.tag_repository.find_all_exist_tags(tags)

        group_by_tagname = defaultdict(list)
        for tag in tags:
            group_by_tagname[tag.tag_name].append(tag)
        print(group_by_tagname)

    def associate_tags_to_company(
        self, company: Company, tags: list[CompanyTagNameDto]
    ):

        self.check_tag_exists(tags)
        return
        save_objs = []
        for tag_dto in tags:
            tag_parent_name = list(tag_dto.tag_name.values())[0]
            tag = Tag(tag_name=tag_parent_name)
            # save_objs.append(tag)
            for lang, name in tag_dto.tag_name.items():
                tag_lang = TagLang(tag=tag, lang=lang, tag_name=name)
                tag.languages.append(tag_lang)
                # save_objs.append(tag_lang)
            # print(tag)
            save_objs.append(tag)
            company.tags.append(tag)
            save_objs.append(company)
            # self.company_tag_repository.save(tag, commit=True)
        self.company_tag_repository.save_all(save_objs, commit=True)

    # def associate_tags_to_company(self, company_id: int, tags: list[CompanyTagNameDto]):
    #     unique_tags = []
    #     for tag in tags:
    #         for name in tag.tag_name.values():
    #             if name not in unique_tags:
    #                 unique_tags.append(name)
    #
    #     check_exists_tags: list[KeywordTag] = (
    #         self.keyword_tag_repository.get_tags_by_names(unique_tags)
    #     )
    #     tag_name_dict = {tag.tag_name: tag.id for tag in check_exists_tags}
    #
    #     new_keyword_tags = []
    #     for tag in unique_tags:
    #         if tag not in tag_name_dict:
    #             new_keyword_tags.append(KeywordTag(tag_name=tag))
    #     if new_keyword_tags:
    #         self.keyword_tag_repository.save_bulk(new_keyword_tags, commit=True)
    #         check_add_tags = self.keyword_tag_repository.get_tags_by_names(
    #             [tag.tag_name for tag in new_keyword_tags]
    #         )
    #         tag_name_dict.update({tag.tag_name: tag.id for tag in check_add_tags})
    #
    #     new_company_tags = []
    #
    #     exist_tags = self.company_tag_repository.find_all_by(
    #         CompanyTag.company_id == company_id,
    #         CompanyTag.tag_id.in_(tag_name_dict.values()),
    #     )
    #     exist_tag_ids = []
    #     if exist_tags:
    #         exist_tag_ids = [tag.tag_id for tag in exist_tags]
    #
    #     for tag in tags:
    #         for lang, name in tag.tag_name.items():
    #             if tag_name_dict[name] in exist_tag_ids:
    #                 continue
    #
    #             new_company_tags.append(
    #                 CompanyTag(
    #                     company_id=company_id, tag_id=tag_name_dict[name], lang=lang
    #                 )
    #             )
    #
    #     self.company_tag_repository.save_bulk(new_company_tags, commit=True)
    #
    #     return True

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
        # self.company_tag_repository.delete_all_by(
        #     CompanyTag.company_id == company_id,
        #     CompanyTag.tag_id.in_(tag_ids),
        # )
