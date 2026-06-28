"""Tests for anki_tools.prioritize."""

import pytest

from tests.conftest import requires_anki


# ---------------------------------------------------------------------------
# Unit tests (no Anki required)
# ---------------------------------------------------------------------------

def test_prioritize_calls_add_tags_when_word_exists(mocker):
    mock_client = mocker.MagicMock()
    mock_client.model_names.return_value = ["Italian Vocabulary"]
    mock_client.find_notes.return_value = [12345]

    mocker.patch("anki_tools.prioritize.AnkiConnectClient", return_value=mock_client)
    mocker.patch("anki_tools.prioritize.ensure_model")

    from anki_tools.prioritize import prioritize

    prioritize(word="sconto", tag="priority::encountered", deck_name="Italian Vocabulary :: Personale")

    mock_client.add_tags.assert_called_once_with([12345], ["priority::encountered"])


def test_prioritize_does_not_create_word_when_word_exists(mocker):
    mock_client = mocker.MagicMock()
    mock_client.find_notes.return_value = [99]

    mocker.patch("anki_tools.prioritize.AnkiConnectClient", return_value=mock_client)
    mocker.patch("anki_tools.prioritize.ensure_model")
    mock_collect = mocker.patch("anki_tools.prioritize._collect_word")

    from anki_tools.prioritize import prioritize

    prioritize(word="sconto", tag="priority::encountered", deck_name="Italian Vocabulary :: Personale")

    mock_collect.assert_not_called()


def test_prioritize_launches_word_creator_when_word_missing(mocker, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "words").mkdir()

    mock_client = mocker.MagicMock()
    mock_client.find_notes.return_value = []

    mocker.patch("anki_tools.prioritize.AnkiConnectClient", return_value=mock_client)
    mocker.patch("anki_tools.prioritize.ensure_model")

    from anki_tools.word_entry import WordEntry

    fake_entry = WordEntry(
        italian="zzz_new",
        english="test",
        part_of_speech="s.m.",
    )
    mock_collect = mocker.patch("anki_tools.prioritize._collect_word", return_value=fake_entry)
    mock_add_run = mocker.patch("anki_tools.prioritize.add_run")

    from anki_tools.prioritize import prioritize

    prioritize(word="zzz_new", tag="priority::encountered", deck_name="Italian Vocabulary :: Personale")

    mock_collect.assert_called_once()
    mock_add_run.assert_called_once()


def test_prioritize_injects_priority_tag_into_new_entry(mocker, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "words").mkdir()

    mock_client = mocker.MagicMock()
    mock_client.find_notes.return_value = []

    mocker.patch("anki_tools.prioritize.AnkiConnectClient", return_value=mock_client)
    mocker.patch("anki_tools.prioritize.ensure_model")

    from anki_tools.word_entry import WordEntry

    fake_entry = WordEntry(
        italian="zzz_new",
        english="test",
        part_of_speech="s.m.",
    )
    mocker.patch("anki_tools.prioritize._collect_word", return_value=fake_entry)
    mock_add_run = mocker.patch("anki_tools.prioritize.add_run")

    from anki_tools.prioritize import prioritize

    prioritize(word="zzz_new", tag="priority::encountered", deck_name="Italian Vocabulary :: Personale")

    assert "priority::encountered" in fake_entry.tags


# ---------------------------------------------------------------------------
# Integration tests (require Anki)
# ---------------------------------------------------------------------------

@requires_anki
def test_add_tags_integration():
    """Add a temporary note, tag it via prioritize(), then clean up."""
    import json
    from pathlib import Path
    from anki_tools.client.ankiconnect import AnkiConnectClient
    from anki_tools.add_words import DEFAULT_DECK, ensure_model, ensure_deck
    from anki_tools.card_builder import build_fields, build_tags
    from anki_tools.models.italian_vocabulary import MODEL_NAME
    from anki_tools.word_entry import WordEntry
    from anki_tools.prioritize import prioritize

    client = AnkiConnectClient()
    ensure_model(client)
    ensure_deck(client, DEFAULT_DECK)

    entry = WordEntry(italian="zzz_test_prioritize", english="test", part_of_speech="s.m.")
    note_id = client.add_note(
        deck_name=DEFAULT_DECK,
        model_name=MODEL_NAME,
        fields=build_fields(entry),
        tags=build_tags(entry),
    )

    try:
        prioritize(
            word="zzz_test_prioritize",
            tag="priority::test_tag",
            deck_name=DEFAULT_DECK,
        )
        ids = client.find_notes(f'Italian:"zzz_test_prioritize" tag:priority::test_tag')
        assert note_id in ids
    finally:
        client.delete_notes([note_id])
