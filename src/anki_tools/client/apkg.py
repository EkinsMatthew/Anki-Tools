from anki_tools.client.base import AnkiClient


class ApkgClient(AnkiClient):
    """
    # TODO: implement direct .apkg file editing without Anki running.
    All methods are stubs — the interface is defined; the implementation is not.
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

    def delete_notes(self, note_ids: list[int]) -> None:
        raise NotImplementedError("# TODO: implement direct .apkg editing")
