import json

import pytest

from anki_tools.word_entry import ITALIAN_ABBREVS, WordEntry


def test_required_fields():
    entry = WordEntry(italian="sgomberare", english="to clear out", part_of_speech="v.tr.")
    assert entry.italian == "sgomberare"
    assert entry.english == "to clear out"
    assert entry.part_of_speech == "v.tr."


def test_optional_fields_default_to_empty():
    entry = WordEntry(italian="casa", english="house", part_of_speech="s.f.")
    assert entry.tags == []
    assert entry.example_it == ""
    assert entry.example_en == ""
    assert entry.dictionary_link == ""
    assert entry.extra_info == ""


def test_tags_are_independent_per_instance():
    a = WordEntry(italian="a", english="a", part_of_speech="prep.")
    b = WordEntry(italian="b", english="b", part_of_speech="prep.")
    a.tags.append("category::test")
    assert b.tags == [], "tags list must not be shared between instances"


def test_round_trip_serialization():
    entry = WordEntry(
        italian="sgomberare",
        english="to clear out, to vacate",
        part_of_speech="v.tr.",
        tags=["category::parole_che_ho_incontrato"],
        example_it="Dobbiamo sgomberare la stanza.",
        example_en="We have to clear out the room.",
        dictionary_link="https://example.com",
        extra_info="some note",
    )
    restored = WordEntry.from_dict(entry.to_dict())
    assert restored == entry


def test_from_dict_with_missing_optional_keys():
    data = {"italian": "via", "english": "street", "part_of_speech": "s.f."}
    entry = WordEntry.from_dict(data)
    assert entry.tags == []
    assert entry.example_it == ""


def test_italian_abbrevs_is_nonempty_list_of_strings():
    assert len(ITALIAN_ABBREVS) > 0
    assert all(isinstance(a, str) for a in ITALIAN_ABBREVS)


@pytest.mark.parametrize("abbrev", ITALIAN_ABBREVS)
def test_each_abbreviation_ends_with_period(abbrev):
    assert abbrev.endswith("."), f"{abbrev!r} should end with a period"
