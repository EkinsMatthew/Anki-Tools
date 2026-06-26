import re

import pytest

from anki_tools.word_entry import ITALIAN_ABBREVS, TAG_PATTERN


# ---------------------------------------------------------------------------
# Tag validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tag", [
    "category::parole_che_ho_incontrato",
    "pos::verb",
    "tier::fondamentale",
    "group::colors",
    "source::duolingo",
])
def test_valid_tags_match_pattern(tag):
    assert re.match(TAG_PATTERN, tag)


@pytest.mark.parametrize("tag", [
    "NoColon",
    "category:missing_second_colon",
    "UPPERCASE::tag",
    "::empty_prefix",
    "category::",
    "category::Has Spaces",
    "category::Has-Hyphen",
])
def test_invalid_tags_do_not_match_pattern(tag):
    assert not re.match(TAG_PATTERN, tag)


# ---------------------------------------------------------------------------
# POS input parsing (number or abbreviation)
# ---------------------------------------------------------------------------

def _parse_pos_input(raw: str) -> str | None:
    """Mirror the logic that cli.py will use to resolve POS input."""
    raw = raw.strip()
    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(ITALIAN_ABBREVS):
            return ITALIAN_ABBREVS[idx]
        return None
    if raw in ITALIAN_ABBREVS:
        return raw
    return None


@pytest.mark.parametrize("raw,expected", [
    ("1", "v.tr."),
    ("3", "v.pronom."),
    (str(len(ITALIAN_ABBREVS)), ITALIAN_ABBREVS[-1]),
    ("v.tr.", "v.tr."),
    ("s.m.", "s.m."),
    ("agg.", "agg."),
])
def test_valid_pos_inputs(raw, expected):
    assert _parse_pos_input(raw) == expected


@pytest.mark.parametrize("raw", [
    "0",
    str(len(ITALIAN_ABBREVS) + 1),
    "99",
    "verb",
    "noun",
    "",
    "V.TR.",
])
def test_invalid_pos_inputs_return_none(raw):
    assert _parse_pos_input(raw) is None


def test_pos_number_input_is_1_indexed():
    assert _parse_pos_input("1") == ITALIAN_ABBREVS[0]
    assert _parse_pos_input(str(len(ITALIAN_ABBREVS))) == ITALIAN_ABBREVS[-1]
