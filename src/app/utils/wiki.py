import logging
import wikipedia
import urllib.parse
from src.app.services.requests.aiohttp_singleton import SingletonAiohttp

logger = logging.getLogger(__name__)

NO_ARTICLE_MESSAGES = {
    "en": "Wikipedia does not have an article with this exact name",
    "de": "Diese Seite existiert nicht",
}


async def wiki_has_lemma(lemma: str, language: str = "en") -> bool:
    if language not in NO_ARTICLE_MESSAGES:
        raise ValueError(
            f"language must be one of {NO_ARTICLE_MESSAGES.keys()}")
    url = f"https://{language}.wikipedia.org/wiki/{urllib.parse.quote(lemma)}"
    try:
        response = NO_ARTICLE_MESSAGES[language] not in str(
            await SingletonAiohttp.get(url))
    except Exception as e:
        logger.warning(f"{e} exception occured")
        response = False
    return response


def is_disambiguation(word: str):
    try:
        _ = wikipedia.summary(word)
        return True
    except wikipedia.exceptions.DisambiguationError:
        return False
    except wikipedia.exceptions.PageError:
        return False
