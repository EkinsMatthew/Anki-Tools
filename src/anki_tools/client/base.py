from abc import ABC, abstractmethod


class AnkiNotRunningError(RuntimeError):
    """Raised when AnkiConnect cannot be reached (Anki not open or addon not installed)."""


class AnkiConnectError(RuntimeError):
    """Raised when AnkiConnect returns an API-level error."""


class DuplicateNoteError(ValueError):
    """Raised when a note already exists in the target deck."""


class AnkiClient(ABC):
    @abstractmethod
    def deck_names(self) -> list[str]: ...

    @abstractmethod
    def model_names(self) -> list[str]: ...

    @abstractmethod
    def create_deck(self, name: str) -> int: ...

    @abstractmethod
    def create_model(self, definition: dict) -> None:
        """Create a note type from the dict returned by get_model_definition()."""

    @abstractmethod
    def update_model_templates(self, definition: dict) -> None:
        """Sync card templates on an existing note type to match definition."""

    @abstractmethod
    def find_notes(self, query: str) -> list[int]: ...

    @abstractmethod
    def add_note(
        self,
        deck_name: str,
        model_name: str,
        fields: dict[str, str],
        tags: list[str],
    ) -> int:
        """Add a note and return the new note ID."""

    @abstractmethod
    def delete_notes(self, note_ids: list[int]) -> None:
        """Delete notes by ID (used by test cleanup fixtures)."""
