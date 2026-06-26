import socket

import pytest

from anki_tools.word_entry import WordEntry


def _anki_is_running() -> bool:
    """Return True if AnkiConnect appears to be listening on localhost:8765."""
    try:
        with socket.create_connection(("127.0.0.1", 8765), timeout=1):
            return True
    except OSError:
        return False


# Marker that skips a test unless Anki is actually running.
requires_anki = pytest.mark.skipif(
    not _anki_is_running(),
    reason="Anki is not running (start Anki with AnkiConnect addon to run integration tests)",
)


@pytest.fixture
def sample_entry() -> WordEntry:
    return WordEntry(
        italian="sgomberare",
        english="to clear out, to vacate",
        part_of_speech="v.tr.",
        tags=["category::parole_che_ho_incontrato"],
        example_it="Dobbiamo sgomberare la stanza entro domani.",
        example_en="We have to clear out the room by tomorrow.",
    )
