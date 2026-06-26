"""
Abstract base class and exceptions for Anki client implementations.

Two concrete implementations exist:

- `AnkiConnectClient` — talks to a running Anki instance via the AnkiConnect
  addon's HTTP API (the primary implementation).
- `ApkgClient` — future direct ``.apkg`` file editing without Anki running
  (currently a stub).
"""

from abc import ABC, abstractmethod


class AnkiNotRunningError(RuntimeError):
    """Raised when AnkiConnect cannot be reached (Anki not open or addon not installed)."""


class AnkiConnectError(RuntimeError):
    """Raised when AnkiConnect returns an API-level error."""


class DuplicateNoteError(ValueError):
    """Raised when a note already exists in the target deck."""


class AnkiClient(ABC):
    """
    Abstract interface for interacting with an Anki collection.

    All methods map 1-to-1 with AnkiConnect actions so that a future
    `ApkgClient` (direct file editing) can be swapped in without changing
    any calling code.
    """

    @abstractmethod
    def deck_names(self) -> list[str]:
        """Return the names of all decks in the collection."""

    @abstractmethod
    def model_names(self) -> list[str]:
        """Return the names of all note types (models) in the collection."""

    @abstractmethod
    def create_deck(self, name: str) -> int:
        """
        Create a deck and return its ID.

        Uses ``::`` as a hierarchy separator, so ``"A :: B"`` creates ``B``
        as a sub-deck of ``A``.  If the deck already exists, returns its
        existing ID without error.
        """

    @abstractmethod
    def create_model(self, definition: dict) -> None:
        """
        Create a note type from a definition dict.

        The dict must match the shape returned by
        `anki_tools.models.italian_vocabulary.get_model_definition`.
        """

    @abstractmethod
    def update_model_templates(self, definition: dict) -> None:
        """
        Sync card templates on an existing note type to match `definition`.

        Use this after adding a new template to `TEMPLATES` in
        `anki_tools.models.italian_vocabulary` to push the change to Anki
        without recreating the note type.
        """

    @abstractmethod
    def find_notes(self, query: str) -> list[int]:
        """
        Search for notes using Anki's search syntax and return their IDs.

        Example query: ``'Italian:"sconto" deck:"Italian Vocabulary :: Personale"'``
        """

    @abstractmethod
    def add_note(
        self,
        deck_name: str,
        model_name: str,
        fields: dict[str, str],
        tags: list[str],
    ) -> int:
        """
        Add a note to `deck_name` and return the new note ID.

        Args:
            deck_name: Target deck (created if it does not exist).
            model_name: Note type name (must already exist in the collection).
            fields: Field values keyed by field name.
            tags: List of tag strings to attach to the note.

        Raises:
            AnkiConnectError: if Anki rejects the note (e.g. duplicate on
                first field when ``allowDuplicate`` is False).
        """

    @abstractmethod
    def delete_notes(self, note_ids: list[int]) -> None:
        """Delete notes by ID. Used primarily by test cleanup fixtures."""
