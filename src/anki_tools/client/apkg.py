"""
Stub implementation of `AnkiClient` for direct ``.apkg`` file editing.

All methods raise `NotImplementedError`.  This module exists to define the
interface contract that a future implementation must fulfil — allowing callers
to be written against `AnkiClient` today without depending on Anki being open.
"""

from anki_tools.client.base import AnkiClient


class ApkgClient(AnkiClient):
    """
    Future `AnkiClient` that edits ``.apkg`` files directly without Anki running.

    An ``.apkg`` file is a ZIP archive containing a SQLite database.  Once
    implemented, this client will allow adding notes to an offline collection
    file, which can then be imported into Anki.

    All methods currently raise `NotImplementedError`.
    """

    def deck_names(self) -> list[str]:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def model_names(self) -> list[str]:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def create_deck(self, name: str) -> int:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def create_model(self, definition: dict) -> None:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def update_model_templates(self, definition: dict) -> None:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def update_model_styling(self, definition: dict) -> None:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def find_notes(self, query: str) -> list[int]:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def add_note(
        self,
        deck_name: str,
        model_name: str,
        fields: dict[str, str],
        tags: list[str],
    ) -> int:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def update_model_fields(self, definition: dict) -> None:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def find_cards(self, query: str) -> list[int]:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def change_card_deck(self, card_ids: list[int], deck_name: str) -> None:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def add_tags(self, note_ids: list[int], tags: list[str]) -> None:
        raise NotImplementedError("# TODO: implement direct .apkg editing")

    def delete_notes(self, note_ids: list[int]) -> None:
        raise NotImplementedError("# TODO: implement direct .apkg editing")
