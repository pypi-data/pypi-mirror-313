"""
Functions for general use.
"""

import requests
import json
import datetime
import wikipls.consts as consts

from typing import overload

from wikipls.type_obj import RevisionId, ArticleId


def to_timestamp(date: datetime.date | str) -> str:
    # From yyyymmdd
    if type(date) == datetime.date:
        return date.strftime("%Y%m%d")

    # From yyyy-mm-ddThh:mm:ssZ
    else:
        return date.split('T')[0].replace('-', '')


def from_timestamp(timestamp: str, out_fmt: type[datetime.date] | type[datetime.datetime] = datetime.date) \
        -> datetime.date | datetime.datetime:
    # From yyyy-mm-ddThh:mm:ssZ
    if "T" in timestamp:
        date_only: str = timestamp.split('T')[0]
        date_info: tuple[int, ...] = tuple(int(info) for info in date_only.split('-'))

        time_only: str = timestamp.split('T')[1].removesuffix('Z')
        time_info: tuple[int, ...] = tuple(int(info) for info in time_only.split(':'))

        if out_fmt == datetime.date:
            return datetime.date(date_info[0], date_info[1], date_info[2])
        elif out_fmt == datetime.datetime:
            return datetime.datetime(date_info[0], date_info[1], date_info[2], time_info[0], time_info[1], time_info[2])

    # From yyyymmdd
    else:
        if out_fmt == datetime.date:
            return datetime.date(int(timestamp[:5]), int(timestamp[5:7]), int(timestamp[7:9]))
        elif out_fmt == datetime.datetime:
            return datetime.datetime(int(timestamp[:5]), int(timestamp[5:7]), int(timestamp[7:9]))


@overload
def id_of_page(key: str, lang: str = consts.LANG) -> RevisionId: ...
@overload
def id_of_page(key: str, date: str | datetime.date, lang: str = consts.LANG) -> RevisionId: ...


def id_of_page(*args, lang: str = consts.LANG) -> RevisionId:
    # Validate input
    if len(args) != 1 and len(args) != 2:
        raise AttributeError("Expected 1 or 2 arguments")
    elif type(args[0]) != str:
        raise AttributeError("key argument must be a string")
    elif len(args) == 2 and (type(args[1]) != str and type(args[1]) != datetime.date):
        raise AttributeError("date argument must be a string or a datetime.date object")
    elif type(lang) != str:
        raise AttributeError("lang key-argument must be a string")

    # Set-up arguments
    key = args[0]
    is_date: bool = len(args) == 2

    # Get ID from args
    if is_date:
        date = args[1]
        if type(date) == datetime.date:
            date = to_timestamp(date)

        url = f"https://{lang}.wikipedia.org/w/rest.php/v1/page/{key}/history"
        response = json_response(url)["revisions"]

        while True:
            # Check timestamps
            for revision in response:
                formatted_timestamp = revision["timestamp"].split('T')[0].replace('-', '')

                if formatted_timestamp <= date:
                    return revision["id"]

            # If no revision found: Search older versions
            response = json_response(url, params={"older_than": response[-1]["id"]})["revisions"]

    else:
        response = json_response(f"https://api.wikimedia.org/core/v1/wikipedia/{lang}/page/{key}/bare")

        return response["id"]


def key_of_page(id: ArticleId | RevisionId, lang=consts.LANG) -> str:
    if type(id) == ArticleId:
        id_details = json_response(f"http://{lang}.wikipedia.org/w/api.php",
                                   params={"action": "query", "pageids": id, "format": "json"})

        if "key" in id_details["query"]["pages"][str(id)]:
            title = id_details["query"]["pages"][str(id)]["key"]
            page_details = json_response(f"https://{lang}.wikipedia.org/w/rest.php/v1/page/{title}/bare")
            return page_details["key"]
        else:
            raise Exception("Page not found")
            # raise TypeError(f"No key found. \nType of argument id ({type(id)}) is probably incorrect.")

    elif type(id) == RevisionId :
        revision_details = json_response(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")
        return revision_details["page"]["key"]


def response_for(url: str, params: dict = None) -> str:
    try:
        response = requests.get(url, headers=consts.HEADERS, params=params)

    except requests.exceptions.ConnectionError as err:
        if "Max retries exceeded with url" in str(err):
            raise requests.exceptions.ConnectionError("No internet connection")
        else:
            raise requests.exceptions.ConnectionError(err)

    result = response.text
    if isinstance(result, bytes):
        result = result.decode("utf-8")

    return result


def json_response(url: str, params: dict = None) -> dict:
    try:
        response = requests.get(url, headers=consts.HEADERS, params=params)

    except requests.exceptions.ConnectionError as err:
        if "Max retries exceeded with url" in str(err):
            raise requests.exceptions.ConnectionError("No internet connection")
        else:
            raise requests.exceptions.ConnectionError(err)

    # print(f"{response.url = }")

    try:
        result = json.loads(response.text)

    # If response is not JSON
    except json.decoder.JSONDecodeError:
        raise ValueError("Response is not JSON. Did you mean to use 'response_for()'?")


    # Handle response errors
    match response.status_code:
        case 200:
            return result

        case 400:
            if "key" in result and "detail" in result:
                err = (f"One or more of the arguments given is invalid. "
                       f"\n{result['key']}: {result['detail']}")
            else:
                err = f"One or more of the arguments given is invalid. "
            raise AttributeError(err)

        case 404:
            if 'key' in result and 'detail' in result:
                raise Exception(f"No page was found for {url}. \n{result['key']}: {result['detail']}")
            elif 'messageTranslations' in result and 'en' in result['messageTranslations']:
                raise Exception(result["messageTranslations"]["en"])

        case _:
            result = json.loads(response.text)
            print(f"New error: {response.status_code}, {result['key']}: {result['detail']}")
