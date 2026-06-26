"""
Convert a `WordEntry` into the fields and tags that Anki expects.

This module is the single place that knows how personal vocabulary maps to the
"Italian Vocabulary" note type defined in `anki_tools.models.italian_vocabulary`.
It can be used independently of the CLI or the Anki client — useful for
previewing what a card will look like before committing it to Anki.
"""

from anki_tools.word_entry import WordEntry

_VERB_ABBREVS = {"v.tr.", "v.intr.", "v.pronom."}
_NOUN_ABBREVS = {"s.m.", "s.f.", "s.m.inv.", "s.f.inv."}


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
    return ""


def build_fields(entry: WordEntry) -> dict[str, str]:
    """
    Build the 10-field dict required by the "Italian Vocabulary" Anki note type.

    All personal words receive ``Tier = "Personale"`` and an empty
    ``TierClass`` (no tier colour styling).  The WordReference link is
    auto-generated from the Italian word; the dictionary link is passed
    through verbatim and may be an empty string.

    Args:
        entry: The vocabulary entry to convert.

    Returns:
        A dict with exactly these keys: ``Italian``, ``English``,
        ``PartOfSpeech``, ``ExtraInfo``, ``Tier``, ``TierClass``,
        ``DictionaryLink``, ``WordReferenceLink``, ``Example``,
        ``ExampleTranslation``.
    """
    word = entry.italian.lower().strip()
    extra_info = (
        f'<span class="badge">{entry.extra_info}</span>' if entry.extra_info else ""
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
