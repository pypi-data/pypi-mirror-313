README updated for version: 0.0.1a8

# What is this?
Wikipls is a Python package meant to easily scrape data out of Wikipedia, using its REST API.
This package is still in early development, but it has basic functionality all set.

# Why does it exist?
The REST API for wikimedia, isn't the most intuitive and requires some learning.
When writing code, it also requires setting up a few functions to make it more manageable and readable.
So essentially I made these functions and packaged them so that you (and I) won't have to rewrite them every time.
While I'm at it I made them more intuitive and easy to use without needing to figure out how this API even works.

# Installation
The `requests` library MUST be installed before downloading wikipls.\
This is a known issue that will be resolved as soon as possible.

1. Install *requests*:\
   `pip install requests`

2. Install *wikipls*:\
  `pip install wikipls`

3. Import in your code:\
  `import wikipls`

# How to use
I haven't made any documentation page yet, so for now the below will have to do.\
If anything is unclear don't hesitate to open an issue in [Issues](https://github.com/SpanishCat/py-wikipls/issues) or bring it up in [Discussions](https://github.com/SpanishCat/py-wikipls/discussions).\

  ## Key
  Many functions in this package require the name of the Wiki page you want to check in a URL-friendly format.
  The REST documentation refers to that as a the "key" of an article.
  For example: 
  - The key of the article titled "Water" is: "Water"
  - The key of the article titled "Faded (Alan Walker song)" is: "Faded_(Alan_Walker_song)"
  - The key of the Article titled "Georgia (U.S. state)" is: "Georgia_(U.S._state)"

  That key is what you enter in the *name* parameter of functions. **The key is case-sensitive.**

  To get the key of an article you can:
  1. Take a look at the url of the article.\
    The URL for "Faded" for example is "https://en.wikipedia.org/wiki/Faded_(Alan_Walker_song)".
    Notice it ends with "wiki/" followed by the key of the article.
  2. Take the title of the article and replace all spaces with "_", it'll probably work just fine.
  3. In the future there will be a function to get the key of a title.

  ## GET functions
  These functions can be used without needing to create an object. 
  
  Many of them require the key of an article as a string,
  and an optional a date (datetime.date) object to get results for a specific date.\
  Otherwise they require a revision ID (RevisionId) number.\
  Many functions are compatible with both options.

  ### `get_summary(key: str, fmt: str = "text") -> str`
  Returns a summary of the page.\
  `fmt` can be either `"text"` or `"html"`

  `>>> get_summary("Faded_(Alan_Walker_song)")[:120]`\
  `'"Faded" is a song by Norwegian record producer and DJ Alan Walker with vocals provided by Norwegian singer Iselin Solhei'`

  This examples returns the first 120 letters of the summary of the Faded page

  ### `get_raw_text(key: str, id: RevisionId) -> str`
  Returns the raw text of a page.\
  **This function temporarily doesn't support date arguments. If you want the raw text of an old page, please use a revision ID**
  
  ### `get_html(key: str, old_id: RevisionId = None) -> str`
  Returns the HTML of the page as a string. 
  This can be later parsed using tools like BeautifulSoup.
  
  If an old_id value is given then the HTML will be of an older version of the page,
  taken from the revision that has this ID.

  `>>> get_html("Faded_(Alan_Walker_song)")[:40]`\
  `'<!DOCTYPE html>\n<html prefix="dc: http:/'`

  This example returns the beginning of the html of the "Faded" page.

  ### `get_key(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str`
  Returns the key (URL-friendly name) of an old page.
  
  ### `get_date(id: RevisionId, lang: str = consts.LANG) -> datetime.date`
  Returns the date of a revision, given its ID.
  
  ### `get_lint(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> dict`
  See https://en.wikipedia.org/api/rest_v1/#/Page%20content/get_page_lint__title___revision_.
  
  ### `get_mobile_html(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str`
  See https://en.wikipedia.org/api/rest_v1/#/Page%20content/getContentWithRevision-mobile-html.
  
  ### `get_mobile_html_offline_resources(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str`
  See https://en.wikipedia.org/api/rest_v1/#/Page%20content/get_page_mobile_html_offline_resources__title___revision_.

  ### `get_mobile_sections(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str`
  See https://en.wikipedia.org/api/rest_v1/#/Mobile/getSectionsWithRevision.
  
  ### `get_mobile_sections_lead(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str`
  See https://en.wikipedia.org/api/rest_v1/#/Mobile/getSectionsLeadWithRevision.
  
  ### `get_mobile_sections_remaining(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> str`
  See https://en.wikipedia.org/api/rest_v1/#/Mobile/getSectionsRemainingWithRevision.
  
  ### `get_discussion(key: str, old_id: RevisionId = None, lang: str = consts.LANG) -> dict`
  Returns info about the discussion tab of a page.
  
  ### `get_related(key: str, lang: str = consts.LANG) -> tuple[dict]`
  Returns articles that are related to the one given.
  
  ### `get_views(name: str, date: str | datetime.date, lang: str = LANG) -> int`
  Returns the number of times people visited an article on a given date.

  The date given can be either a datetime.date object or a string formatted *yyyymmdd* (So *March 31th 2024* will be *"20240331"*).

  `>>> get_views("Faded_(Alan_Walker_song)", "20240331")`\
  `1144`
  
  The Faded page on Wikipedia was visited 1,144 on March 31st 2024.

  ### `get_pdf(key: str) -> bytes`
  Returns the PDF version of the page in byte-form.

  `>>> with open("faded_wiki.pdf", 'wb') as f:`\
  `      f.write(get_pdf("Faded_(Alan_Walker_song)"))`

  This example imports the Faded page in PDF form as a new file named "faded_wiki.pdf".

  ---

  ### `get_media_details(key: str, old_id: RevisionId = None) -> tuple[dict, ...]`
  Returns all media present in the article, each media file represented as a JSON.

`>>> get_media_details("Faded_(Alan_Walker_song)")[0]`\
  `{'title': 'File:Alan_Walker_-_Faded.png', 'leadImage': False, 'section_id': 0, 'type': 'image', 'showInGallery': True, 'srcset': [{'src': '//upload.wikimedia.org/wikipedia/en/thumb/d/da/Alan_Walker_-_Faded.png/220px-Alan_Walker_-_Faded.png', 'scale': '1x'}, {'src': '//upload.wikimedia.org/wikipedia/en/d/da/Alan_Walker_-_Faded.png', 'scale': '1.5x'}, {'src': '//upload.wikimedia.org/wikipedia/en/d/da/Alan_Walker_-_Faded.png', 'scale': '2x'}]}`

  This example returns the first media file in the Faded article, which is a PNG image.

  ### `get_image(details: dict[str, ...]) -> bytes`
  Retrives the actual byte-code of an image on a an article, using a JSON representing the image.
  You can get that JSON using `get_media_details()`.

  `>>> get_image({'title': 'File:Alan_Walker_-_Faded.png', 'leadImage': False, 'section_id': 0, 'type': 'image', 'showInGallery': True, 'srcset': [{'src': '//upload.wikimedia.org/wikipedia/en/thumb/d/da/Alan_Walker_-_Faded.png/220px-Alan_Walker_-_Faded.png', 'scale': '1x'}, {'src': '//upload.wikimedia.org/wikipedia/en/d/da/Alan_Walker_-_Faded.png', 'scale': '1.5x'}, {'src': '//upload.wikimedia.org/wikipedia/en/d/da/Alan_Walker_-_Faded.png', 'scale': '2x'}]})`\
  `b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01,\x00\x00\x01,\x08\x03\x00\x00\x00N\xa3~G\x00\x00\x03\x00PLTE\xff\xff\xff\x01\x01\x01\xfe\xfd\xfe'`

  This examples returns the first bytes of the image we got in the `get_media_details()` example.

  ### `get_all_images(key: str, details: Iterable[dict[str, ...]], strict: bool = False) -> tuple[bytes]`
  Returns all images of an article or a provided list of image-JSONs, in bytes form.
  You can only enter either a `key` or `details` value, no need for both.


  ---

  ## Data functions
  Data functions return a dictionary containing many details about the object.
  they can be used without needing to create an object. 

  These functions require either a key with an optional date or an ID.

  ### `get_article_data(identifier: str | ArticleId, lang: str = consts.LANG) -> dict[str, ...]`
  Returns details about an article in JSON form.\
  Identifier can be either the article's name or its ID.
  
  ### `get_page_data(*args, lang: str = consts.LANG) -> dict[str, ...]`
  Returns details and the content of a page (i.e specific version of an Article).
  
  Arguments:
  1. **`get_page_data(id: RevisionId)`**: Get page by using ID of revision.
  2. **`get_page_data(key: str)`**: Get page by using its name. Since no date argument is given wikipls will return the most up-to-date page.
  3. **`get_page_data(key: str, date: str | datetime.date)`**: Get page by using its name and a date.

  ### `get_revision_data(*args, lang: str = consts.LANG) -> dict[str, ...]`
  Returns details about the latest revision to the page in JSON form.\
  If date is provided, returns the latest revision details as of that date.

  Arguments:
  1. **`get_revision_data(id: RevisionId)`**: Get revision using its ID. 
  2. **`get_revision_data(key: str)`**: Get revision by using its name. Since no date argument is given wikipls will return the latest revision. 
  3. **`get_revision_data(key: str, date: str | datetime.date)`**: Get revision by using its name and a date.

  ---
  ## Utility functions
  Functions that make life easier
  
  ### `to_timestamp(date: datetime.date | str) -> str`
  Converts a datetime.date object or a string in format yyyy-mm-ddThh:mm:ssZ to a URL-friendly string format (yyyymmdd)

  `>>> date = datetime.date(2024, 3, 31)`\
  `>>> to_timestamp(date)`\
  `20240331`

  This example converts the date of March 31th 2024 to URL-friendly string form.

  ### `from_timestamp(timestamp: str, out_fmt: type[datetime.date] | type[datetime.datetime] = datetime.date) -> datetime.date | datetime.datetime`
  Converts a timestamp to a datetime.date or datetime.datetime object.\
  The timestamp is a string which is written in one of the following formats:
  - yyyymmdd
  - yyyy-mm-ddThh:mm:ssZ

  ### `id_of_page(*args, lang: str = consts.LANG) -> RevisionId`
  Returns an id of a page, given a key.\
  Date argument is optional: If date is provided, returns the ID of latest revision as of that date.

  Arguments:
  1. **`id_of_page(key: str, lang: str = consts.LANG)`**: Get id using the page key. Since no date argument is given wikipls will return the ID of latest page. 
  2. **`id_of_page(key: str, date: str | datetime.date, lang: str = consts.LANG)`**: Get id using the page key.

  ### `key_of_page(id: ArticleId | RevisionId, lang=consts.LANG) -> str`
  Returns the key of an article given its (or one of its revisions's) ID.

  ### `response_for(url: str, params: dict = None) -> str`
  For internal use mainly.
  ### `json_response(url: str, params: dict = None) -> dict`
  For interal use mainly

  ---


  ### ID classes
  It's very easy to confuse revision IDs for article IDs and vice versa.\
  To combat that IDs are only accepted as either of these:
  - `ArticleId(int)`
  - `RevisionId(int)`
  
  These function just like a regular `int`.
  For example: To make a revision ID 314141, we do `RevisionId(314141)`.

  ---

  ## Wiki objects  
  If you intend on repeatedly getting info about some page, it is preferred that you make an object for that page.\
  This is for reasons of performance as well as readability and organization.
  
  ### `wikipls.Article(key: str)`
  An "Article" is a wikipedia article in all of its versions, revisions and languages.

  #### Properties
  `.key` (str): Article key (URL-friendly name).\
  `.id` (ArticleId): Article ID. Doesn't change across revisions.\
  `.content_model` (str): Type of wiki project this article is a part of (e.g. "wikitext", "wikionary").\
  `.license` (dict): Details about the copyright license of the article.\
  `.html_url` (str): URL to an html version of the current revision of the article.\
  `.latest` (dict): Details about the latest revision done to the article.\
  `.details` (dict[str, Any]): All the above properties in JSON form.\
  
  `.get_page(date: datetime.date, lang: str = "en")` (wikipls.Page): Get a Page object of this article, from a specified date and in a specified translation.

  #### Example properties
  -- TODO

  
  ### `wikipls.Page(*args, lang=consts.LANG, from_article: Article = None)`
  A "Page" is a version of an article in a specific date and a specific language.
  
  from_article is for pages that were created using `wikipls.Article().get_page()`. Don't worry about it:)

  Arguments:
  1. **`(key: str, date: datetime.date | str)`**
  2. **`(page_id: RevisionId)`**

  #### Properties
  `.from_article` (str): Article object of origin, if there is one.\
  `.title` (str): Page title.\
  `.key` (str): The key of the page (URL-friendly name).).\
  `.raw_text` (str): Raw text of this page.\
  `.article_id` (ArticleId): ID of the article this page is derived from.\
  `.revision_id` (RevisionId): ID of the current revision of the article.\
  `.date` (datetime.date): The date of the page.\
  `.lang` (str): The language of the page as an ISO 639 code (e.g. "en" for English).\
  `.content_model` (str): Type of wiki project this page is a part of (e.g. "wikitext", "wikionary").\
  `.license` (dict): Details about the copyright license of the page.\
  `.views` (int): Number of vists this page has received during its specified date.\
  `.html` (str): Page HTML.\
  `.summary` (dict): Summary of the page. `.summary["html"]` is the HTML version and the `.summary["text"]` is the plain-text version.\
  `.media` (tuple[dict, ...]): All media files in the page represented as JSONs.\
  `.as_pdf` (bytes): The PDF version of the page in bytes-code.\
  `.data` (dict[str, Any]): General details about the page in JSON format.\
  `.lint` (?)\
  `.mobile_html` (str)\
  `.mobile_html_offline_resources` (str)\
  `.mobile_sections` (str)\
  `.mobile_sections_lead` (str)\
  `.mobile_sections_remaining` (str)\
  `.discussion` (dict): Info about the behind-the-scenes discussion of this page.\
  `.related` (tuple[dict]): Articles that are related to this one.\
  `.article_details` (dict): Details related to the article the page is derived from.\
  `.page_details` (dict): Details related to the page.\

  `.get_revision()`: Get the relevant revision of this page.
  
  #### Example properties
  -- TODO


  ### `Revision(*args, lang=consts.LANG)`
  A revision is a change made to an article by the Wikipedia editors.\
  So if you scrumble an entire paragraph of the *Moon* article then submit it to the wiki,
  then that scrumble is a **Revision**. The scrumbled result is a **Page**, and so is the article before you scrumbled it.\
  All of this was presumebly done in the *Moon* **Article**.
  
  Arguments:
  1. **`Revision(key: str, date: datetime.date)`**
  1. **`Revision(page_id: RevisionId)`**

  #### Properties
  `.id` (RevisionId): Revision ID.\
  `.lang` (str): Page language code.\
  `.datetime` (datetime.datetime): Time this revision was published on Wikipedia.\
  `.content_model` (str): Type of wiki project this page is a part of (e.g. "wikitext", "wikionary").\
  `.license` (dict): Details about the copyright license of the page.\
  `.html_url` (str): URL to an html version of the current revision of the article.\
  `.comment` (str): Comment of revision.\
  `.user` (dict): Data about the user who published the revision.\
  `.size` (int): \
  `.is_minor` (bool):\
  `.delta` (int):\
  `.details` (dict): Details related to the current revision of the page.\

  `.article_title` (str): Article title.\
  `.article_key` (str): Article key (URL-friendly name).\
  `.article_id` (ArticleId): Article ID. Doesn't change across revisions.\
  
---

# What does the name mean?
Wiki = Wikipedia\
Pls = Please, because you make requests

# Versions
This version of the package is written in Python. I plan to eventually make a copy of this one written in Rust (using PyO3 and maturin).
Why Rust? It's an exercise for me, and it will be way faster and less error-prone

# Plans
- Support for more languages (Currently supports only English Wikipedia)
- Dictionary
- Citations
  
# Bug reports
This package is in early development and I'm looking for community feedback on bugs.\
If you encounter a problem, please report it in [Issues](https://github.com/SpanishCat/py-wikipls/issues).
