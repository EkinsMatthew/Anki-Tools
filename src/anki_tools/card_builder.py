from anki_tools.word_entry import WordEntry


_VERB_ABBREVS = {"v.tr.", "v.intr.", "v.pronom."}
_NOUN_ABBREVS = {"s.m.", "s.f.", "s.m.inv.", "s.f.inv."}


def pos_tag(pos: str) -> str:
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
    tags: set[str] = set(entry.tags)
    auto_tag = pos_tag(entry.part_of_speech)
    if auto_tag:
        tags.add(auto_tag)
    return sorted(tags)
