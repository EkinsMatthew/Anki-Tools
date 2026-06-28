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
import re
import sys
from pathlib import Path

from anki_tools.card_builder import build_fields, build_tags
from anki_tools.client.ankiconnect import AnkiConnectClient
from anki_tools.client.base import (
    AnkiConnectError,
    AnkiNotRunningError,
    DuplicateNoteError,
)
from anki_tools.models.italian_vocabulary import (
    MODEL_NAME as STANDARD_MODEL_NAME,
    get_model_definition as get_standard_model_definition,
)
from anki_tools.models.italian_vocabulary_blank import (
    MODEL_NAME as BLANK_MODEL_NAME,
    get_model_definition as get_blank_model_definition,
)
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


def ensure_model(client: AnkiConnectClient, model_definition: dict) -> None:
    model_name = model_definition["modelName"]
    if model_name not in client.model_names():
        print(f'Note type "{model_name}" not found — creating it…')
        client.create_model(model_definition)
        print(f'  Created "{model_name}".')
    else:
        client.update_model_templates(model_definition)
        client.update_model_styling(model_definition)
        client.update_model_fields(model_definition)


def ensure_deck(client: AnkiConnectClient, deck_name: str) -> None:
    if deck_name not in client.deck_names():
        client.create_deck(deck_name)
        print(f'Created deck "{deck_name}".')


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def run(
    batch_file: Path,
    deck_name: str,
    on_duplicate: str,
    dry_run: bool,
    blank: bool = False,
) -> None:
    model_name = BLANK_MODEL_NAME if blank else STANDARD_MODEL_NAME
    model_definition = get_blank_model_definition() if blank else get_standard_model_definition()

    entries = load_batch(batch_file)
    print(f"Loaded {len(entries)} word(s) from {batch_file}.")

    if dry_run:
        print(f"[dry-run] Deck: '{deck_name}'  |  Note type: '{model_name}'")
        print()
        for e in entries:
            fields = build_fields(e)
            tags = build_tags(e)
            blank_plain = _strip_html(fields.get("ExampleWithBlank", ""))
            print(f"  {e.italian!r} → {e.english!r}  tags={tags}")
            if blank_plain:
                print(f"      blank: {blank_plain!r}")
        print()
        print(f"  {len(entries)} notes")
        return

    try:
        client = AnkiConnectClient()
        ensure_model(client, model_definition)
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

            fields = build_fields(entry)
            client.add_note(
                deck_name=deck_name,
                model_name=model_name,
                fields=fields,
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
    parser.add_argument(
        "--blank",
        action="store_true",
        help=(
            f'Use the fill-in-the-blank-only note type ("{BLANK_MODEL_NAME}") '
            "instead of the standard note type. Use this when adding to a dedicated blank-practice deck."
        ),
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
        blank=args.blank,
    )


if __name__ == "__main__":
    main()
