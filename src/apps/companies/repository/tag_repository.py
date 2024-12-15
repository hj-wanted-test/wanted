from itertools import chain

from sqlalchemy import select

from apps.companies.model import Company, Tag, TagLang
from core.repository import Repository


class TagRepository(Repository):

    __table__ = Tag

    def find_all_exist_tags(self, tags):
        query = (
            select(
                Tag.id,
                TagLang.tag_name,
                TagLang.lang,
            )
            .select_from(Tag)
            .join(TagLang, Tag.id == TagLang.tag_id)
            .filter(
                TagLang.tag_name.in_(chain.from_iterable([list(tag.tag_name.values()) for tag in tags]))
            )
        )

        return self.fetch_all(query, raw=True)
