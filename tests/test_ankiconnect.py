"""
Integration tests for AnkiConnectClient.

These tests require Anki to be running with the AnkiConnect addon installed.
They are automatically skipped when Anki is not reachable.

Run only integration tests:
    uv run pytest -m integration

Skip integration tests:
    uv run pytest -m "not integration"
"""

import pytest

from anki_tools.card_builder import build_fields, build_tags
from anki_tools.client.ankiconnect import AnkiConnectClient
from anki_tools.client.base import AnkiNotRunningError
from anki_tools.models.italian_vocabulary import MODEL_NAME, get_model_definition
from tests.conftest import requires_anki

TEST_DECK = "anki_tools_integration_test"


@pytest.fixture
def client():
    return AnkiConnectClient()


@pytest.fixture(autouse=True)
def cleanup_test_deck(client):
    """Remove test notes after each integration test."""
    yield
    try:
        note_ids = client.find_notes(f'deck:"{TEST_DECK}"')
        if note_ids:
            client.delete_notes(note_ids)
    except Exception:
        pass


@requires_anki
@pytest.mark.integration
def test_deck_names_returns_list(client):
    names = client.deck_names()
    assert isinstance(names, list)
    assert len(names) > 0


@requires_anki
@pytest.mark.integration
def test_model_names_returns_list(client):
    names = client.model_names()
    assert isinstance(names, list)


@requires_anki
@pytest.mark.integration
def test_create_deck(client):
    deck_id = client.create_deck(TEST_DECK)
    assert isinstance(deck_id, int)
    assert TEST_DECK in client.deck_names()


@requires_anki
@pytest.mark.integration
def test_create_model_if_missing(client):
    model_names_before = client.model_names()
    if MODEL_NAME not in model_names_before:
        client.create_model(get_model_definition())
        assert MODEL_NAME in client.model_names()
    else:
        pytest.skip(f'Model "{MODEL_NAME}" already exists — skipping creation test')


@requires_anki
@pytest.mark.integration
def test_add_note_and_find_it(client, sample_entry):
    client.create_deck(TEST_DECK)
    if MODEL_NAME not in client.model_names():
        client.create_model(get_model_definition())

    note_id = client.add_note(
        deck_name=TEST_DECK,
        model_name=MODEL_NAME,
        fields=build_fields(sample_entry),
        tags=build_tags(sample_entry),
    )
    assert isinstance(note_id, int)

    found = client.find_notes(f'Italian:"{sample_entry.italian}" deck:"{TEST_DECK}"')
    assert note_id in found


@requires_anki
@pytest.mark.integration
def test_find_notes_returns_empty_for_nonexistent(client):
    client.create_deck(TEST_DECK)
    found = client.find_notes(f'Italian:"zzz_nonexistent_word_xyz" deck:"{TEST_DECK}"')
    assert found == []


@requires_anki
@pytest.mark.integration
def test_update_model_templates_does_not_raise(client):
    if MODEL_NAME not in client.model_names():
        client.create_model(get_model_definition())
    client.update_model_templates(get_model_definition())


def test_ankiconnect_raises_when_anki_not_running():
    bad_client = AnkiConnectClient(url="http://127.0.0.1:19999")
    with pytest.raises(AnkiNotRunningError):
        bad_client.deck_names()
