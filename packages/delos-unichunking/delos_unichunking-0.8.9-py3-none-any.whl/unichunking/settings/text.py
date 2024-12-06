"""Text processing settings."""

from pydantic_settings import BaseSettings


class TextSettings(BaseSettings):
    """Notable chains of characters to identify for text processing."""

    TABLE_MARKERS: list[str] = [
        "|---",
        "| ---",
        "--- |",
        "---|",
        "|:---",
        "| :---",
        ":--- |",
        ":---|",
        "|---:",
        "| ---:",
        "---: |",
        "---:|",
        "|:---:",
        "| :---:",
        ":---: |",
        ":---:|",
    ]

    LIGATURES: dict[str, str] = {
        "æ": "ae",
        "Æ": "AE",
        "ﬀ": "ff",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ʪ": "ls",
        "œ": "oe",
        "Œ": "OE",
        "ȹ": "qp",
        "ﬆ": "st",
        "ʦ": "ts",
    }

    UNICODE_QUOTES: dict[str, str] = {
        "\x91": "‘",  # noqa: RUF001
        "\x92": "’",  # noqa: RUF001
        "\x93": "“",
        "\x94": "”",
        "&apos;": "'",
        "â\x80\x99": "'",
        "â\x80“": "—",
        "â\x80”": "–",  # noqa: RUF001
        "â\x80˜": "‘",  # noqa: RUF001
        "â\x80¦": "…",
        "â\x80™": "’",  # noqa: RUF001
        "â\x80œ": "“",
        "â\x80?": "”",
        "â\x80ť": "”",
        "â\x80ś": "“",
        "â\x80¨": "—",
        "â\x80ł": "″",
        "â\x80Ž": "",
        "â\x80‚": "",  # noqa: RUF001
        "â\x80‰": "",
        "â\x80‹": "",  # noqa: RUF001
        "â\x80": "",
        "â\x80s'": "",
    }
