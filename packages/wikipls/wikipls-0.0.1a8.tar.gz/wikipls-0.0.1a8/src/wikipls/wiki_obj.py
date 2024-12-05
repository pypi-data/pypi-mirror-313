# -*- coding: hebrew -*-
from typing import Any

from .func import *


class Article:
    def __init__(self, key: str):
        """
        :param key: Case-sensitive
        """
        self.details: dict[str, Any] = get_article_data(key)

        # Map details to class
        self.title: str = self.details["key"] # fixme This is a key not a title
        self.key: str = self.details["key"]
        self.id: ArticleId = ArticleId(self.details["id"])
        self.content_model: str = self.details["content_model"]
        self.license: dict = self.details["license"]
        self.html_url: str = self.details["html_url"]

        # todo Make latest a Revision object
        latest: dict = self.details["latest"]
        latest["id"] = RevisionId(latest["id"])
        self.latest: dict = latest

    def __repr__(self):
        return f"Article({self.title}, {self.id})"

    def __eq__(self, other):
        return self.id == other.revision_id and self.key == other.article_key

    @overload
    def get_page(self, date: datetime.date, lang: str = consts.LANG): ...
    @overload
    def get_page(self, lang: str = consts.LANG): ...

    def get_page(self, *args, lang: str = consts.LANG):
        if len(args) == 0:
            return Page(self.latest["id"], lang=lang, from_article=self)

        elif len(args) == 1 and type(args[0]) == datetime.date:
            return Page(self.key, args[0], lang=lang, from_article=self)

        else:
            raise AttributeError("Unexpected arguments")


class Page:
    """
    The difference between a wikipls.Page and a wikipls.Article:
    Article - Collection of all versions of all languages of all dates for a single article. A 'collection' of Pages
    Page - One specific version of an article, in a specific date and a specific language
    """

    memory: dict = {}
    @overload
    def __init__(self, key: str, date: datetime.date | str, lang: str = consts.LANG, from_article: Article = None): ...
    @overload
    def __init__(self, page_id: RevisionId, lang: str = consts.LANG, from_article: Article = None): ...

    def __init__(self, *args, lang=consts.LANG, from_article: Article = None):

        # Validate input
        if len(args) == 0:
            raise AttributeError("No arguments were provided")
        elif (len(args) > 2
              or len(args) == 1 and type(args[0]) != RevisionId
              or len(args) == 2 and (type(args[0]) != str or (not isinstance(args[1], datetime.date) and not isinstance(args[1], str)))):
            raise AttributeError(f"Unexpected arguments. Args: {args}")

        by: str = "key" if len(args) == 2 else "id"
        identifier = args[0]

        # Get details
        if by == "key":
            date = args[1] if isinstance(args[1], datetime.date) else from_timestamp(args[1])

            self.article_details: dict[str, Any] = get_article_data(identifier, lang=lang)
            self.page_details: dict[str, Any] = get_page_data(identifier, date, lang=lang)
        else:  # using ID
            self.article_details: dict[str, Any] = get_article_data(identifier, lang=lang)
            self.page_details: dict[str, Any] = get_page_data(identifier, lang=lang)

        self.from_article: Article | None = from_article

        # Map details to class
        self.article_id: ArticleId = ArticleId(self.page_details["pageid"])
        self.revision_id: RevisionId = RevisionId(self.page_details["revid"])
        self.html: str = self.page_details["text"]

        if by == "key":
            # self.date: datetime.date = from_timestamp(self.page_details["timestamp"])
            self.date: datetime.date = date #fixme
        else:
            self.date: datetime.date = get_date(self.revision_id)

        # self.key: str = self.article_details["key"]
        self.title: str = self.page_details["title"]
        self.content_model: str = self.article_details["content_model"]
        self.license: dict[str, ...] = self.article_details["license"]
        self.html_url: str = self.article_details["html_url"]

        self.lang: str = self.html_url.removeprefix("https://")[:2]


    def __repr__(self):
        return f"Page({self.key}, {self.date}, {self.article_id})"

    def __eq__(self, other):
        return self.article_id == other.revision_id and self.key == other.article_key

    # region Properties
    @property
    def key(self) -> str:
        if not "key" in self.memory:
            self.memory["key"] = get_key(self.article_details["key"], old_id=self.revision_id)
        return self.memory["key"]

    # @property
    # def data_parsoid(self):
    #     if not "data-parsoid" in self.memory:
    #         self.memory["data-parsoid"] = get_data_parsoid(self.key, old_id=self.revision_id)
    #     return self.memory["data-parsoid"]

    @property
    def lint(self) -> list[dict]:
         if not "lint" in self.memory:
             self.memory["lint"] = get_lint(self.key, old_id=self.revision_id)
         return self.memory["lint"]

    # FIXME: Fix this. DO NOT DELETE!
    # @property
    # def segments(self) -> str:
    #     if not "segments" in self.memory:
    #         self.memory["segments"] = get_segments(self.key, old_id=self.revision_id)
    #     return self.memory["segments"]
    
    @property
    def mobile_html(self) -> str:
        if not "mobile_html" in self.memory:
            self.memory["mobile_html"] = get_mobile_html(self.key, old_id=self.revision_id)
        return self.memory["mobile_html"]

    @property
    def mobile_html_offline_resources(self) -> str:
        if not "mobile_html_offline_resources" in self.memory:
            self.memory["mobile_html_offline_resources"] = get_mobile_html_offline_resources(self.key, old_id=self.revision_id)
        return self.memory["mobile_html_offline_resources"]

    @property
    def mobile_sections(self) -> str:
        if not "mobile_sections" in self.memory:
            self.memory["mobile_sections"] = get_mobile_sections(self.key, old_id=self.revision_id)
        return self.memory["mobile_sections"]

    @property
    def mobile_sections_lead(self) -> str:
        if not "mobile_sections_lead" in self.memory:
            self.memory["mobile_sections_lead"] = get_mobile_sections_lead(self.key, old_id=self.revision_id)
        return self.memory["mobile_sections_lead"]

    @property
    def mobile_sections_remaining(self) -> str:
        if not "mobile_sections_remaining" in self.memory:
            self.memory["mobile_sections_remaining"] = get_mobile_sections_remaining(self.key, old_id=self.revision_id)
        return self.memory["mobile_sections_remaining"]

    @property
    def discussion(self) -> dict:
        if not "discussion" in self.memory:
            self.memory["discussion"] = get_discussion(self.key, old_id=self.revision_id)
        return self.memory["discussion"]

    @property
    def related(self) -> tuple[dict]:
        if not "related" in self.memory:
            self.memory["related"] = get_related(self.key)
        return self.memory["related"]
    # endregion

    @property
    def raw_text(self) -> str:
        return get_raw_text(self.key, self.revision_id)

    @property
    def views(self) -> int:
        if "views" not in self.memory:
            self.memory["views"]: int = get_views(self.key, self.date, self.lang)
        return self.memory["views"]

    # @property
    # def html(self) -> str:
    #     if "html" not in self.memory:
    #         self.memory["html"]: str = get_html(self.key)
    #     return self.memory["html"]

    @property
    def summary(self) -> dict:
        if "summary" not in self.memory:
            # self.memory["summary"]: str = get_summary(self.key)
            self.memory["summary"]: str = {
                "html": get_summary(self.key, fmt="html"),
                "text": get_summary(self.key, fmt="text")
            }

        return self.memory["summary"]

    @property
    def media(self) -> tuple[dict, ...]:
        if "media" not in self.memory:
            # self.memory["media"]: tuple[dict, ...] = get_media_details(self.key)
            self.memory["media"]: tuple[dict, ...] = (
                json_response(f"https://{self.lang}.wikipedia.org/api/rest_v1/page/media-list/{self.key}/{self.revision_id}")
                )["items"]

        return self.memory["media"]

    @property
    def as_pdf(self) -> bytes:
        if "pdf_code" not in self.memory:
            self.memory["pdf_code"]: bytes = get_pdf(self.key)
        return self.memory["pdf_code"]

    @property
    def data(self) -> dict[str, Any]:
        if "data" not in self.memory:
            self.memory["data"]: dict = get_page_data(self.key)
        return self.memory["data"]

    # endregion

    def get_revision(self):
        return Revision(self.revision_id, lang=self.lang)


class Revision:
    @overload
    def __init__(self, key: str, date: datetime.date, lang: str = consts.LANG): ...
    @overload
    def __init__(self, page_id: RevisionId, lang: str = consts.LANG): ...

    def __init__(self, *args, lang=consts.LANG):
        # Validate input
        if len(args) == 0:
            raise AttributeError("No arguments were provided")
        elif (len(args) > 2
              or len(args) == 1 and type(args[0]) != RevisionId
              or len(args) == 2 and (type(args[0]) != str or type(args[1]) != datetime.date)):
            raise AttributeError(f"Unexpected arguments. Args: {args}")

        by: str = "key" if len(args) == 2 else "id"
        identifier = args[0]

        # Get details
        if by == "key":
            date = args[1]
            self.details: dict[str, Any] = get_revision_data(identifier, date, lang=lang)
        else:  # using ID
            self.details: dict[str, Any] = get_revision_data(identifier, lang=lang)

        # Map details to class
        self.id: RevisionId = RevisionId(self.details["id"])
        self.size: int = self.details["size"]
        self.is_minor: bool = self.details["minor"]
        self.datetime: datetime.datetime = from_timestamp(self.details["timestamp"], out_fmt=datetime.datetime)
        self.content_model: str = self.details["content_model"]
        self.comment: str = self.details["comment"]
        self.delta: int = self.details["delta"]
        self.html_url: str = self.details["html_url"]

        self.lang: str = self.html_url.removeprefix("https://")[:2]

        self.article_title: str = self.details["page"]["key"]
        self.article_key: str = self.details["page"]["key"]
        self.article_id: ArticleId = self.details["page"]["id"]

        self.license: dict[str: str, str: str] = self.details["license"]
        self.user: dict[str: int, str: str] = self.details["user"]


    def __repr__(self):
        return f"Revision({self.article_title}, {self.datetime}, {self.article_id})"

    def __eq__(self, other):
        return (type(other) == Revision
                and self.article_id == other.article_id
                and self.id == other.id)
