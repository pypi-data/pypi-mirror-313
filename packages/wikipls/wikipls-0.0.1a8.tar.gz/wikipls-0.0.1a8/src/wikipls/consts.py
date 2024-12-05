import datetime

from typing import Final

LANG: Final = "en"
TEST_DATE: Final = datetime.date(2024, 11, 1)

# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64"}  # todo Check wiki's docs and change headers
HEADERS: Final = {
    'User-Agent': 'MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)'
}

# todo: Use WikiBlame (https://en.wikipedia.org/wiki/Help:Page_history) to analyze revisions
# todo: Add URL attribute for Article and Page
# todo: Add comparison tools (https://en.wikipedia.org/wiki/Template:Diff)
