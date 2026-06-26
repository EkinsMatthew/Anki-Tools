import requests

from anki_tools.client.base import (
    AnkiClient,
    AnkiConnectError,
    AnkiNotRunningError,
)

ANKICONNECT_URL = "http://127.0.0.1:8765"
ANKICONNECT_VERSION = 6


class AnkiConnectClient(AnkiClient):
    def __init__(self, url: str = ANKICONNECT_URL) -> None:
        self._url = url

    def _invoke(self, action: str, **params) -> object:
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
        return self._invoke("deckNames")

    def model_names(self) -> list[str]:
        return self._invoke("modelNames")

    def create_deck(self, name: str) -> int:
        return self._invoke("createDeck", deck=name)

    def create_model(self, definition: dict) -> None:
        self._invoke("createModel", **definition)

    def update_model_templates(self, definition: dict) -> None:
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
        return self._invoke("findNotes", query=query)

    def add_note(
        self,
        deck_name: str,
        model_name: str,
        fields: dict[str, str],
        tags: list[str],
    ) -> int:
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
        self._invoke("deleteNotes", notes=note_ids)
