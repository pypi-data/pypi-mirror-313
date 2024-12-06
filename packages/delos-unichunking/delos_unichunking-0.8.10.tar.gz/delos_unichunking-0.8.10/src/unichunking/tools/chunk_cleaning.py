"""Auxiliary functions to clean the text in a chunk."""

import re

from unstructured.nlp.patterns import UNICODE_BULLETS_RE

from unichunking.settings import unisettings
from unichunking.types import Chunk


def _clean_extra_whitespace(text: str) -> str:
    """Cleans extra whitespace characters that appear between words.

    Example:
    -------
    ITEM 1.     BUSINESS -> ITEM 1. BUSINESS
    """
    cleaned_text = re.sub(r"[\xa0\n]", " ", text)
    cleaned_text = re.sub(r"([ ]{2,})", " ", cleaned_text)
    return cleaned_text.strip()


def _clean_bullets(text: str) -> str:
    """Cleans unicode bullets from a section of text.

    Example:
    -------
    ●  This is an excellent point! -> This is an excellent point!
    """
    search = UNICODE_BULLETS_RE.match(text)
    if search is None:
        return text

    cleaned_text = UNICODE_BULLETS_RE.sub("", text, 1)
    return cleaned_text.strip()


def _clean(
    text: str,
) -> str:
    """Cleans text."""
    cleaned_text = _clean_extra_whitespace(text)
    cleaned_text = _clean_bullets(cleaned_text)
    return cleaned_text.strip()


def _clean_ligatures(text: str) -> str:
    """Replaces ligatures with their most likely equivalent characters.

    Example:
    -------
    The beneﬁts -> The benefits
    High quality ﬁnancial -> High quality financial
    """
    cleaned_text: str = text
    for k, v in unisettings.text.LIGATURES.items():
        cleaned_text = cleaned_text.replace(k, v)

    return cleaned_text


def _replace_unicode_quotes(text: str) -> str:
    r"""Replaces unicode bullets in text with the expected character.

    Example:
    -------
    \x93What a lovely quote!\x94 -> “What a lovely quote!”
    """
    for k, v in unisettings.text.UNICODE_QUOTES.items():
        text = text.replace(k, v)
    return text


def _clean_non_utf8_chars(text: str) -> str:
    r"""Cleans characters other than UTF-8 from a string.

    Example:
    -------
    b'\xc2\x88This text contains non-ascii characters!\xc2\x88'
        -> This text contains non-ascii characters!
    """
    utf8_encoded = text.encode("utf-8", "ignore")
    return utf8_encoded.decode("utf-8")


def clean_chunk(chunk: Chunk) -> Chunk:
    """Remove unwanted characters/blanks for better LLM readability."""
    content = chunk.content

    # Invoking Unstructured
    content = _replace_unicode_quotes(content)

    # CRUSHES FRENCH ACCENTS! ↓ :
    content = _clean_non_utf8_chars(content)

    content = _clean(content)
    content = _clean_ligatures(content)

    # Doing stuff my own way
    content = content.replace("\uf0b7", " ")
    content = content.replace("\xe0", "à")
    content = content.replace("\xe7", "ç")
    content = content.replace("\xe8", "è")
    content = content.replace("\xe9", "é")
    content = content.replace("\xf4", "ô")
    content = content.replace("\n", " ")

    chunk.content = content

    return chunk
