"""
Convert a `WordEntry` into the fields and tags that Anki expects.

This module is the single place that knows how a vocabulary entry maps to the
note type defined in `anki_tools.models.italian_vocabulary`.
It can be used independently of the CLI or the Anki client — useful for
previewing what a card will look like before committing it to Anki.
"""

import re

from anki_tools.word_entry import WordEntry

_VERB_ABBREVS = {"v.tr.", "v.intr.", "v.pronom."}
_NOUN_ABBREVS = {"s.m.", "s.f.", "s.m.inv.", "s.f.inv."}

# Maps register markers (in extra_info) to CSS badge classes.
# Separate multiple markers with ";".  Unknown text gets the default badge.
_REGISTER_BADGES: dict[str, str] = {
    "volg.": "badge badge-volgare",
}


def _render_extra_info(text: str) -> str:
    """Render extra_info as one or more badge spans.

    Semicolons separate multiple items; ``volg.`` (case-insensitive) gets a
    red badge via ``.badge-volgare``; all other text gets the default grey
    ``.badge``.
    """
    parts = [p.strip() for p in text.split(";") if p.strip()]
    return "".join(
        f'<span class="{_REGISTER_BADGES.get(p.lower(), "badge")}">{p}</span>'
        for p in parts
    )


def pos_tag(pos: str) -> str:
    """
    Map an Italian part-of-speech abbreviation to its ``pos::`` Anki tag.

    Returns an empty string for abbreviations that have no corresponding tag
    (conjunctions, pronouns, articles, interjections, numerals).

    Examples:
        >>> pos_tag("v.tr.")
        'pos::verb'
        >>> pos_tag("s.m.")
        'pos::noun'
        >>> pos_tag("cong.")
        ''
    """
    pos = pos.strip()
    if pos in _VERB_ABBREVS:
        return "pos::verb"
    if pos in _NOUN_ABBREVS:
        return "pos::noun"
    if pos == "agg.":
        return "pos::adjective"
    if pos == "avv.":
        return "pos::adverb"
    if pos == "prep.":
        return "pos::preposition"
    if pos == "inter.":
        return "pos::interjection"
    return ""


def make_example_with_blank(italian: str, example_it: str) -> str:
    """
    Replace the target word in an example sentence with ``___``.

    Matches the whole word only (word boundaries), case-insensitively.
    Returns an empty string if the word does not appear verbatim — callers
    should prompt the user for a manual substitution in that case.

    Examples:
        >>> make_example_with_blank("sconto", "Mi fa uno sconto?")
        'Mi fa uno ___?'
        >>> make_example_with_blank("andare", "Dove vai?")
        ''
    """
    pattern = re.compile(re.escape(italian.strip()), re.IGNORECASE)
    result, count = pattern.subn("___", example_it, count=1)
    return result if count else ""


def build_fields(entry: WordEntry) -> dict[str, str]:
    """
    Build the full field dict required by the "Italian Vocabulary" Anki note type.

    Notes receive ``Tier = "Personale"`` and an empty ``TierClass`` (no tier
    colour styling).  The WordReference link is auto-generated from the target
    word; the dictionary link is passed through verbatim.

    ``ExampleWithBlank`` is resolved in this order:

    1. Use ``entry.example_with_blank`` if the user supplied it explicitly.
    2. Otherwise, attempt auto-generation via `make_example_with_blank`.
    3. If the word doesn't appear verbatim in the example, leave the field
       empty — the fill-in-the-blank card template will not be generated.

    Args:
        entry: The vocabulary entry to convert.

    Returns:
        A dict with keys matching every field in
        `anki_tools.models.italian_vocabulary.FIELDS`.
    """
    word = entry.italian.lower().strip()
    extra_info = _render_extra_info(entry.extra_info) if entry.extra_info else ""
    example_with_blank = entry.example_with_blank or make_example_with_blank(
        entry.italian, entry.example_it
    )
    if example_with_blank:
        example_with_blank = example_with_blank.replace(
            "___", '<span class="blank">___</span>'
        )
    return {
        "Italian": entry.italian,
        "English": entry.english,
        "PartOfSpeech": entry.part_of_speech,
        "ExtraInfo": extra_info,
        "Tier": "Personale",
        "TierClass": "",
        "DictionaryLink": entry.dictionary_link,
        "WordReferenceLink": f"https://www.wordreference.com/iten/{word}",
        "Example": entry.example_it,
        "ExampleTranslation": entry.example_en,
        "ExampleWithBlank": example_with_blank,
    }


def build_tags(entry: WordEntry) -> list[str]:
    """
    Build the sorted, deduplicated tag list for an Anki note.

    Automatically derives a ``pos::`` tag from `entry.part_of_speech` via
    `pos_tag` and merges it with any tags the user supplied in `entry.tags`.
    If the abbreviation has no corresponding ``pos::`` tag (e.g. ``cong.``),
    no ``pos::`` tag is added.

    Args:
        entry: The vocabulary entry whose tags to build.

    Returns:
        A sorted list of unique tag strings.
    """
    tags: set[str] = set(entry.tags)
    auto_tag = pos_tag(entry.part_of_speech)
    if auto_tag:
        tags.add(auto_tag)
    return sorted(tags)
