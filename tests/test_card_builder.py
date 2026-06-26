import pytest

from anki_tools.card_builder import build_fields, build_tags, pos_tag
from anki_tools.word_entry import ITALIAN_ABBREVS, WordEntry


def _entry(**kwargs) -> WordEntry:
    defaults = dict(italian="sgomberare", english="to clear out", part_of_speech="v.tr.")
    return WordEntry(**{**defaults, **kwargs})


# ---------------------------------------------------------------------------
# build_fields
# ---------------------------------------------------------------------------

def test_tier_is_always_personale():
    assert build_fields(_entry())["Tier"] == "Personale"


def test_tier_class_is_always_empty():
    assert build_fields(_entry())["TierClass"] == ""


def test_wordreference_link_is_auto_generated():
    fields = build_fields(_entry(italian="Sgomberare"))
    assert fields["WordReferenceLink"] == "https://www.wordreference.com/iten/sgomberare"


def test_wordreference_link_strips_whitespace():
    fields = build_fields(_entry(italian="  casa  "))
    assert fields["WordReferenceLink"] == "https://www.wordreference.com/iten/casa"


def test_extra_info_wrapped_in_badge_span_when_present():
    fields = build_fields(_entry(extra_info="Irr PP: mosso"))
    assert fields["ExtraInfo"] == '<span class="badge">Irr PP: mosso</span>'


def test_extra_info_empty_string_when_not_provided():
    fields = build_fields(_entry())
    assert fields["ExtraInfo"] == ""


def test_example_fields_passed_through():
    fields = build_fields(_entry(example_it="Frase.", example_en="Sentence."))
    assert fields["Example"] == "Frase."
    assert fields["ExampleTranslation"] == "Sentence."


def test_empty_example_fields_produce_empty_strings():
    fields = build_fields(_entry())
    assert fields["Example"] == ""
    assert fields["ExampleTranslation"] == ""


def test_dictionary_link_passed_through():
    fields = build_fields(_entry(dictionary_link="https://example.com"))
    assert fields["DictionaryLink"] == "https://example.com"


def test_all_ten_fields_present():
    expected = {
        "Italian", "English", "PartOfSpeech", "ExtraInfo",
        "Tier", "TierClass", "DictionaryLink", "WordReferenceLink",
        "Example", "ExampleTranslation",
    }
    assert set(build_fields(_entry()).keys()) == expected


# ---------------------------------------------------------------------------
# pos_tag
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("abbrev,expected", [
    ("v.tr.", "pos::verb"),
    ("v.intr.", "pos::verb"),
    ("v.pronom.", "pos::verb"),
    ("s.m.", "pos::noun"),
    ("s.f.", "pos::noun"),
    ("s.m.inv.", "pos::noun"),
    ("s.f.inv.", "pos::noun"),
    ("agg.", "pos::adjective"),
    ("avv.", "pos::adverb"),
    ("prep.", "pos::preposition"),
    ("cong.", ""),
    ("pron.", ""),
    ("art.", ""),
    ("inter.", ""),
    ("num.", ""),
])
def test_pos_tag_mapping(abbrev, expected):
    assert pos_tag(abbrev) == expected


# ---------------------------------------------------------------------------
# build_tags
# ---------------------------------------------------------------------------

def test_pos_tag_auto_added():
    tags = build_tags(_entry(part_of_speech="v.tr."))
    assert "pos::verb" in tags


def test_user_tags_included():
    tags = build_tags(_entry(tags=["category::parole_che_ho_incontrato"]))
    assert "category::parole_che_ho_incontrato" in tags


def test_tags_deduplicated():
    tags = build_tags(_entry(part_of_speech="v.tr.", tags=["pos::verb"]))
    assert tags.count("pos::verb") == 1


def test_tags_sorted():
    tags = build_tags(_entry(tags=["z::last", "a::first"]))
    assert tags == sorted(tags)


def test_no_empty_string_tag_when_pos_unknown():
    tags = build_tags(_entry(part_of_speech="cong."))
    assert "" not in tags
