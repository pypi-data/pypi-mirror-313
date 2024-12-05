"""
Get data JSONs of an object - Article, Page or Revision
"""

from wikipls.func.utils import *
# from wikipls.type_obj import ArticleId, RevisionId

# region data
# @overload
# def old_get_page_data(key: str, lang: str = consts.LANG) -> dict[str, ...]: ...
# @overload
# def old_get_page_data(key: str, date: str | datetime.date, lang: str = consts.LANG) -> dict[str, ...]: ...
# @overload
# def old_get_page_data(id: RevisionId, lang: str = consts.LANG) -> dict[str, ...]: ...
#
#
# def old_get_page_data(*args, lang: str = consts.LANG) -> dict[str, ...]:
#     # Validate arguments
#     # You should read it as the rules for valid input (and avoid the "not"s in the beginning)
#     if not (len(args) == 1 or len(args) == 2):
#         raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")
#     elif not (type(args[0]) == str or type(args[0]) == RevisionId):
#         raise AttributeError(f"key argument must be string or RevisionId. Got type {type(args[0])} instead")
#     elif len(args) == 2 and not (type(args[1]) == datetime.date or type(args[1]) == str):
#         raise AttributeError(f"date argument must be either string or datetime.date")
#
#     is_date: bool = len(args) == 2
#     by: str = "key" if type(args[0]) == str else "id"
#
#     if by == "id":
#         id = args[0]
#
#     else:  # By key
#         key = args[0]
#
#         if is_date:
#             date = args[1]
#             id = id_of_page(key, date)
#         else:
#             id = id_of_page(key)
#
#     revision_res = json_response(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")
#     revision_res.pop("page")
#     revision_res.pop("user")
#     return revision_res


@overload
def get_page_data(key: str, lang: str = consts.LANG) -> dict[str, ...]: ...
@overload
def get_page_data(key: str, date: str | datetime.date, lang: str = consts.LANG) -> dict[str, ...]: ...
@overload
def get_page_data(id: RevisionId, lang: str = consts.LANG) -> dict[str, ...]: ...


def get_page_data(*args, lang: str = consts.LANG) -> dict[str, ...]:
    # Validate arguments
    # You should read it as the rules for valid input (and avoid the "not"s in the beginning)
    if not (len(args) == 1 or len(args) == 2):
        raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")
    elif not isinstance(args[0], (str, RevisionId)):
        raise AttributeError(f"key argument must be string or RevisionId. Got type {type(args[0])} instead")
    elif len(args) == 2 and not isinstance(args[1], (datetime.date, str)):
        raise AttributeError(f"date argument must be either string or datetime.date")

    is_date: bool = len(args) == 2
    by: str = "key" if type(args[0]) == str else "id"

    if by == "id":
        id: RevisionId = args[0]
        # key: str = key_of_page(id)

    else:  # By key
        key: str = args[0]

        if is_date:
            date: datetime.date = args[1]
            id: RevisionId = id_of_page(key, date)
        else:
            id: RevisionId = id_of_page(key)

    # revision_res = requests.get(f"https://{lang}.wikipedia.org/w/index.php",
    #                             params={"key": key, "oldid": id})



    # Taken from Method 2: https://www.mediawiki.org/wiki/API:Get_the_contents_of_a_page
    revision_res = requests.get(f"https://{lang}.wikipedia.org/w/api.php",
                                params={"action": "parse",
                                        "oldid": id,
                                        "format": "json",
                                        "prop": "text",
                                        "formatversion": 2
                                        })
    print(revision_res.url)

    revision_res = json_response(revision_res.url) # This madness is for being able to get the URL

    # print(f"https://{lang}.wikipedia.org/w/index.php?key={key}&oldid={id}")
    return revision_res["parse"] # todo sort the JSON data


def get_article_data(identifier: str | ArticleId, lang: str = consts.LANG) -> dict[str, ...]:
    if type(identifier) == str:
        by = "key"
    else:
        by = "id"

    if by == "id":
        # Get article key using ID
        id_details = json_response(f"http://en.wikipedia.org/w/api.php",
                                   params={"action": "query", "pageids": identifier, "format": "json"})

        # fixme: Needs to get key not key
        if "key" in id_details["query"]["pages"][str(identifier)]:
            key = id_details["query"]["pages"][str(identifier)]["key"]
        else:
            key = key_of_page(identifier)

    else:
        key = identifier

    response = json_response(f"https://{lang}.wikipedia.org/w/rest.php/v1/page/{key}/bare")

    out_details: dict[str, ...] = {
        "key": response["key"],
        "id": response["id"],
        "latest": response["latest"],
        "content_model": response["content_model"],
        "license": response["license"],
        "html_url": response["html_url"]
    }

    return out_details


@overload
def get_revision_data(key: str, lang: str = consts.LANG) -> dict[str, ...]: ...
@overload
def get_revision_data(key: str, date: str | datetime.date, lang: str = consts.LANG) -> dict[str, ...]: ...
@overload
def get_revision_data(id: RevisionId, lang: str = consts.LANG) -> dict[str, ...]: ...


def get_revision_data(*args, lang: str = consts.LANG) -> dict[str, ...]:
    # Validate arguments
    # You should read it as the rules for valid input (and avoid the "not"s in the beginning)
    if not (len(args) == 1 or len(args) == 2):
        raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")
    elif not (type(args[0]) == str or type(args[0]) == RevisionId):
        raise AttributeError(f"key argument must be string or int. Got type {type(args[0])} instead")
    elif len(args) == 2 and not (type(args[1]) == datetime.date or type(args[1]) == str):
        raise AttributeError(f"date argument must be either string or datetime.date")

    if type(args[0]) == str:
        by = "key"
    else:
        by = "id"

    is_date: bool = len(args) == 2
    # if type(args[0] == str):
    #     name = args[0]
    # else:
    #     id = args[0]

    if by == "id":
        id = args[0]

    else:   # By key
        key = args[0]

        if is_date:
            date = args[1]
            id = id_of_page(key, date)

        else:
            id = id_of_page(key)

    response = json_response(f"https://{lang}.wikipedia.org/w/rest.php/v1/revision/{id}/bare")
    return response

    # if is_date:
    #     date = args[1]
    #     if type(date) == str:
    #
    #         pass
    #         # response = json_response()
