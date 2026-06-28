"""
Bump a word's priority in Anki by tagging it for focused review.

Usage:
    uv run anki-prioritize sconto
    uv run anki-prioritize sconto --tag priority::encountered
    uv run anki-prioritize sconto --deck "Italian Vocabulary :: Personale"

If the word exists in Anki it receives the priority tag immediately.
If it doesn't exist, the interactive word-creation flow runs first, then
the word is added and tagged in one step.

**Studying priority words:**
Create a filtered deck in Anki with the search query
``tag:priority::encountered`` to review these words in a focused session
without disturbing your main deck's spaced-repetition schedule.  Remove
the tag from a note (Anki Browser → Edit Tags) when you no longer need
the extra exposure.

Requires:
    Anki to be open with the AnkiConnect addon installed (code 2055492159).
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from anki_tools.add_words import DEFAULT_DECK, ensure_deck, ensure_model, run as add_run
from anki_tools.cli import _collect_word
from anki_tools.client.ankiconnect import AnkiConnectClient
from anki_tools.client.base import AnkiNotRunningError

DEFAULT_PRIORITY_TAG = "priority::encountered"


def _write_temp_batch(entry, tag: str) -> Path:
    """Write a single-entry batch JSON and return its path."""
    entry.tags = sorted(set(entry.tags) | {tag})
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = Path("words") / f"priority_{ts}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([entry.to_dict()], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path


def prioritize(word: str, tag: str, deck_name: str) -> None:
    """
    Add `tag` to an existing note for `word`, or create the word first.

    Args:
        word: The target word to look up in Anki (case-insensitive search).
        tag: Priority tag to add (e.g. ``"priority::encountered"``).
        deck_name: Deck to search in and, if creating a new word, add it to.
    """
    try:
        client = AnkiConnectClient()
        ensure_model(client)
    except AnkiNotRunningError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    query = f'Italian:"{word}" deck:"{deck_name}"'
    note_ids = client.find_notes(query)

    if note_ids:
        client.add_tags(note_ids, [tag])
        print(
            f"'{word}' tagged {tag}.\n"
            f"Study it in Anki with the filter: tag:{tag}"
        )
        return

    print(f"'{word}' not found in '{deck_name}' — launching word creator.")
    print("Fill in the details for this word:\n")

    try:
        entry = _collect_word(session_tags=set())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)

    batch_path = _write_temp_batch(entry, tag)
    print(f"\nSaved to {batch_path}. Adding to Anki…")

    add_run(
        batch_file=batch_path,
        deck_name=deck_name,
        on_duplicate="skip",
        dry_run=False,
    )
    print(
        f"\n'{entry.italian}' added and tagged {tag}.\n"
        f"Study it in Anki with the filter: tag:{tag}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Tag a word as priority in Anki. "
            "Creates the word first if it doesn't exist."
        )
    )
    parser.add_argument("word", help="The word to prioritize (must match the Italian field exactly)")
    parser.add_argument(
        "--tag",
        default=DEFAULT_PRIORITY_TAG,
        help=f"Priority tag to add (default: {DEFAULT_PRIORITY_TAG!r})",
    )
    parser.add_argument(
        "--deck",
        default=DEFAULT_DECK,
        help=f'Deck to search in (default: "{DEFAULT_DECK}")',
    )
    args = parser.parse_args()
    prioritize(word=args.word, tag=args.tag, deck_name=args.deck)


if __name__ == "__main__":
    main()
