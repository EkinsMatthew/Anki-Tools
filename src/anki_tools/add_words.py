"""
Add a batch of personal vocabulary words to an existing Anki deck.

Usage:
    uv run anki-add words/2026-06-19_143022.json
    uv run anki-add words/2026-06-19_143022.json --deck "Italian Vocabulary :: Personale"
    uv run anki-add words/2026-06-19_143022.json --dry-run
    uv run anki-add words/2026-06-19_143022.json --on-duplicate error

Requires:
    Anki to be open with the AnkiConnect addon installed (code 2055492159).
"""

import argparse
import json
import sys
from pathlib import Path

from anki_tools.card_builder import build_fields, build_tags
from anki_tools.client.ankiconnect import AnkiConnectClient
from anki_tools.client.base import (
    AnkiConnectError,
    AnkiNotRunningError,
    DuplicateNoteError,
)
from anki_tools.models.italian_vocabulary import MODEL_NAME, get_model_definition
from anki_tools.word_entry import WordEntry

DEFAULT_DECK = "Italian Vocabulary :: Personale"


def load_batch(path: Path) -> list[WordEntry]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: {path} is not valid JSON — {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(raw, list):
        print(f"Error: {path} must contain a JSON array of word objects.", file=sys.stderr)
        sys.exit(1)

    entries = []
    for i, item in enumerate(raw):
        try:
            entries.append(WordEntry.from_dict(item))
        except KeyError as exc:
            print(f"Error: entry {i} is missing required field {exc}.", file=sys.stderr)
            sys.exit(1)
    return entries


def ensure_model(client: AnkiConnectClient) -> None:
    if MODEL_NAME not in client.model_names():
        print(f'Note type "{MODEL_NAME}" not found — creating it…')
        client.create_model(get_model_definition())
        print(f'  Created "{MODEL_NAME}".')
    else:
        client.update_model_templates(get_model_definition())


def ensure_deck(client: AnkiConnectClient, deck_name: str) -> None:
    if deck_name not in client.deck_names():
        client.create_deck(deck_name)
        print(f'Created deck "{deck_name}".')


def run(
    batch_file: Path,
    deck_name: str,
    on_duplicate: str,
    dry_run: bool,
) -> None:
    entries = load_batch(batch_file)
    print(f"Loaded {len(entries)} word(s) from {batch_file}.")

    if dry_run:
        print("[dry-run] Would add the following notes:")
        for e in entries:
            fields = build_fields(e)
            tags = build_tags(e)
            print(f"  {e.italian!r} → {e.english!r}  tags={tags}")
        return

    try:
        client = AnkiConnectClient()
        ensure_model(client)
        ensure_deck(client, deck_name)
    except AnkiNotRunningError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    added = skipped = failed = 0
    for entry in entries:
        query = f'Italian:"{entry.italian}" deck:"{deck_name}"'
        try:
            existing = client.find_notes(query)
            if existing:
                if on_duplicate == "error":
                    raise DuplicateNoteError(
                        f'"{entry.italian}" already exists in "{deck_name}".'
                    )
                print(f"  Skipped (duplicate): {entry.italian!r}")
                skipped += 1
                continue
            elif on_duplicate == "update":
                raise NotImplementedError(
                    "--on-duplicate update is not yet implemented."
                )

            client.add_note(
                deck_name=deck_name,
                model_name=MODEL_NAME,
                fields=build_fields(entry),
                tags=build_tags(entry),
            )
            print(f"  Added: {entry.italian!r}")
            added += 1
        except (DuplicateNoteError, NotImplementedError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        except AnkiConnectError as exc:
            print(f"  Failed ({entry.italian!r}): {exc}", file=sys.stderr)
            failed += 1

    print(f"\nDone — Added {added} / Skipped {skipped} (duplicate) / Failed {failed}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add a JSON word batch to an Anki deck via AnkiConnect."
    )
    parser.add_argument("batch_file", type=Path, help="Path to words JSON batch file")
    parser.add_argument(
        "--deck",
        default=DEFAULT_DECK,
        help=f'Target Anki deck name (default: "{DEFAULT_DECK}")',
    )
    parser.add_argument(
        "--on-duplicate",
        choices=["skip", "error", "update"],
        default="skip",
        help="How to handle a word that already exists in the deck (default: skip)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be added without writing to Anki",
    )
    args = parser.parse_args()

    if not args.batch_file.exists():
        print(f"Error: file not found: {args.batch_file}", file=sys.stderr)
        sys.exit(1)

    run(
        batch_file=args.batch_file,
        deck_name=args.deck,
        on_duplicate=args.on_duplicate,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
