"""
Request a specific piece of data from the wikipedia API
"""
import urllib.parse
from argparse import ArgumentError

from typing import Iterable

from .utils import *


# region Text
def get_summary(key: str, fmt: str = "text") -> str:
    # fixme Check what's up with the revision support for summary in API

    response = json_response(f"https://en.wikipedia.org/api/rest_v1/page/summary/{key}")

    if fmt == "text":
        return response["extract"]
    elif fmt == "html":
        return response["extract_html"]
    else:
        raise ArgumentError(None, f"'fmt' was assigned an invalid value ({fmt}). Valid values are 'text' or 'html'")



# todo This needs to be argument-flexible
def get_raw_text(key: str, id: RevisionId) -> str:
    response = response_for(
        "https://en.wikipedia.org/w/index.php",
        params={"key": key, "oldid": id, "action": "raw"}
    )

    return response


def get_html(key: str, old_id: RevisionId = None) -> str:
    if old_id:
        response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/html/{key}/{old_id}")
    else:
        response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/html/{key}")

    if response.status_code == 200:
        return response.content.decode("utf-8")


def get_pdf(key: str) -> bytes:
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/pdf/{key}")

    if response.status_code == 200:
        return response.content
# endregion


# region Misc
# todo Use all of the data in the URLs
def get_key(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str:
    if old_id:
        response = json_response(f"https://{lang}.wikipedia.org/api/rest_v1/page/title/{key}/{old_id}")
    else:
        response = json_response(f"https://{lang}.wikipedia.org/api/rest_v1/page/title/{key}")

    return response["items"][0]["title"]

# def get_data_parsoid(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str:
#     if old_id:
#         return requests.get(f"https://{lang}.wikipedia.org/api/rest_v1/page/data-parsoid/{key}/{old_id}").content
#     else:
#         return requests.get(f"https://{lang}.wikipedia.org/api/rest_v1/page/data-parsoid/{key}").content

def get_lint(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> dict:
    if old_id:
        return json_response(f"https://{lang}.wikipedia.org/api/rest_v1/page/lint/{key}/{old_id}")
    else:
        return json_response(f"https://{lang}.wikipedia.org/api/rest_v1/page/lint/{key}")

# DO NOT DELETE!
# def get_segments(key: str, old_id: RevisionId = None) -> str:
#     # todo Add strict=False option that'll raise an error if response is None
#     if old_id:
#         response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/segments/{key}/{old_id}")
#     else:
#         response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/segments/{key}")
#
#     print(f"{response.url=}")
#
#     if response:
#         return response["segmentedContent"]

def get_mobile_html(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str:
    if old_id:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-html/{key}/{old_id}")
    else:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-html/{key}")

def get_mobile_html_offline_resources(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str:
    if old_id:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-html-offline-resources/{key}/{old_id}")
    else:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-html-offline-resources/{key}")

def get_mobile_sections(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str:
    if old_id:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-sections/{key}/{old_id}")
    else:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-sections/{key}")

def get_mobile_sections_lead(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str:
    if old_id:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-sections-lead/{key}/{old_id}")
    else:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-sections-lead/{key}")

def get_mobile_sections_remaining(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str:
    if old_id:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-sections-remaining/{key}/{old_id}")
    else:
        return response_for(f"https://{lang}.wikipedia.org/api/rest_v1/page/mobile-sections-remaining/{key}")

def get_discussion(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> dict:
    if old_id:
        return json_response(
            f"https://{lang}.wikipedia.org/api/rest_v1/page/talk/{key}/{old_id}")
    else:
        return json_response(
            f"https://{lang}.wikipedia.org/api/rest_v1/page/talk/{key}")

def get_related(key: str, lang: str = consts.LANG) -> tuple[dict]:
        return tuple(json_response(f"https://{lang}.wikipedia.org/api/rest_v1/page/related/{key}")["pages"])

# endregion


@overload
def get_views(key: str, date: datetime.date, lang: str = consts.LANG) -> int: ...
@overload
def get_views(key: str, date: str, lang: str = consts.LANG) -> int: ...


def get_views(key: str, date: str | datetime.date, lang: str = consts.LANG) -> int:
    if isinstance(date, datetime.date):
        date = to_timestamp(date)
    elif not isinstance(date, str):
        raise AttributeError("date must be a string or a datetime.date object")

    url = u"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
          u"{}.wikipedia.org/all-access/all-agents/{}/daily/{}/{}" \
        .format(lang.lower(), urllib.parse.quote(key), date, date)

    response = json_response(url)

    return response["items"][0]["views"]


# region media
def get_media_details(key: str, old_id: RevisionId = None) -> tuple[dict, ...]:
    if old_id:
        response = json_response(f"https://en.wikipedia.org/api/rest_v1/page/media-list/{key}/{old_id}")
    else:
        response = json_response(f"https://en.wikipedia.org/api/rest_v1/page/media-list/{key}")

    if response:
        return tuple(response["items"])


def get_image(details: dict[str, ...]) -> bytes:
    src_url = details["srcset"][-1]["src"]
    response = requests.get(f"https:{src_url}", headers=consts.HEADERS)
    return response.content


@overload
def get_all_images(key: str, strict: bool = False) -> tuple[bytes]: ...
@overload
def get_all_images(details: Iterable[dict[str, ...]], strict: bool = False) -> tuple[bytes]: ...


def get_all_images(image_info: str | Iterable[dict[str, ...]], strict: bool = True) -> tuple[bytes]:
    if type(image_info) == "str":
        details: Iterable[dict[str, ...]] = get_media_details(image_info)
    else:
        details = image_info

    # Check for non-image media
    if strict:
        for media in details:
            if media["type"] != "image":
                raise AttributeError("Media list cannot contain media objects that are not images.")
    else:
        details = tuple(media for media in details if media["type"] == "image")

    all_images = tuple(get_image(image) for image in details)
    return all_images

# endregion

def get_date(id: RevisionId, lang: str = consts.LANG) -> datetime.date:
    response = json_response(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")

    return from_timestamp(response["timestamp"])
