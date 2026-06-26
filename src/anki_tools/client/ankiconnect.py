"""
Concrete `AnkiClient` implementation that talks to a running Anki instance
via the AnkiConnect addon's local HTTP API.

AnkiConnect must be installed in Anki (addon code **2055492159**) and Anki
must be open before any method on this client can be called.  All requests
are sent to ``http://127.0.0.1:8765`` using protocol version 6.
"""

import requests

from anki_tools.client.base import (
    AnkiClient,
    AnkiConnectError,
    AnkiNotRunningError,
)

ANKICONNECT_URL = "http://127.0.0.1:8765"
ANKICONNECT_VERSION = 6


class AnkiConnectClient(AnkiClient):
    """
    Send commands to Anki via the AnkiConnect HTTP API.

    Args:
        url: Base URL of the AnkiConnect addon. Defaults to
            ``http://127.0.0.1:8765``.  Override in tests to point at a
            non-existent port and exercise the error path without Anki running.
    """

    def __init__(self, url: str = ANKICONNECT_URL) -> None:
        self._url = url

    def _invoke(self, action: str, **params) -> object:
        """
        Send a single AnkiConnect action and return its ``result`` value.

        Raises:
            AnkiNotRunningError: if Anki is not reachable or the response is
                not valid JSON.
            AnkiConnectError: if AnkiConnect returns a non-null ``error`` field.
        """
        payload = {"action": action, "version": ANKICONNECT_VERSION, "params": params}
        try:
            response = requests.post(self._url, json=payload, timeout=10)
            data = response.json()
        except requests.ConnectionError as exc:
            raise AnkiNotRunningError(
                "Cannot reach Anki. Make sure Anki is open and the AnkiConnect "
                "addon (code 2055492159) is installed."
            ) from exc
        except Exception as exc:
            raise AnkiNotRunningError(
                f"Unexpected response from AnkiConnect: {exc}"
            ) from exc

        if data.get("error"):
            raise AnkiConnectError(data["error"])
        return data["result"]

    def deck_names(self) -> list[str]:
        """Return the names of all decks in the Anki collection."""
        return self._invoke("deckNames")

    def model_names(self) -> list[str]:
        """Return the names of all note types in the Anki collection."""
        return self._invoke("modelNames")

    def create_deck(self, name: str) -> int:
        """Create a deck and return its ID (no-op if it already exists)."""
        return self._invoke("createDeck", deck=name)

    def create_model(self, definition: dict) -> None:
        """Create a note type from a definition dict (see `get_model_definition`)."""
        self._invoke("createModel", **definition)

    def update_model_templates(self, definition: dict) -> None:
        """Push updated card templates to an existing note type in Anki."""
        # AnkiConnect expects templates as a dict keyed by template name
        templates = {
            t["Name"]: {"Front": t["Front"], "Back": t["Back"]}
            for t in definition["cardTemplates"]
        }
        self._invoke(
            "updateModelTemplates",
            model={"name": definition["modelName"], "templates": templates},
        )

    def find_notes(self, query: str) -> list[int]:
        """Search using Anki's query syntax and return matching note IDs."""
        return self._invoke("findNotes", query=query)

    def add_note(
        self,
        deck_name: str,
        model_name: str,
        fields: dict[str, str],
        tags: list[str],
    ) -> int:
        """Add a note and return the new note ID."""
        return self._invoke(
            "addNote",
            note={
                "deckName": deck_name,
                "modelName": model_name,
                "fields": fields,
                "tags": tags,
                "options": {"allowDuplicate": False},
            },
        )

    def delete_notes(self, note_ids: list[int]) -> None:
        """Permanently delete notes by ID."""
        self._invoke("deleteNotes", notes=note_ids)
