"""
Interactive CLI to build a JSON word batch file for anki-add.

Usage:
    uv run anki-cli
    uv run anki-cli --output words/my-batch.json
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from anki_tools.card_builder import pos_tag as compute_pos_tag
from anki_tools.word_entry import ITALIAN_ABBREVS, TAG_PATTERN, WordEntry

_COLS = 3
_COL_WIDTH = 12


def _display_pos_menu() -> None:
    print("\nParts of speech:")
    for i, abbrev in enumerate(ITALIAN_ABBREVS):
        num = f"{i + 1:>2}. {abbrev}"
        print(f"  {num:<{_COL_WIDTH}}", end="")
        if (i + 1) % _COLS == 0 or i == len(ITALIAN_ABBREVS) - 1:
            print()
    print()


def _parse_pos_input(raw: str) -> str | None:
    raw = raw.strip()
    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(ITALIAN_ABBREVS):
            return ITALIAN_ABBREVS[idx]
        return None
    if raw in ITALIAN_ABBREVS:
        return raw
    return None


def _prompt(label: str, required: bool = True, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    suffix += ": "
    while True:
        value = input(f"{label}{suffix}").strip()
        if not value and default:
            return default
        if value or not required:
            return value
        print(f"  (required — please enter a value)")


def _prompt_pos() -> str:
    _display_pos_menu()
    while True:
        raw = input("Enter number or abbreviation: ").strip()
        result = _parse_pos_input(raw)
        if result:
            return result
        print(
            f"  Invalid — enter a number 1–{len(ITALIAN_ABBREVS)} "
            f"or an abbreviation like v.tr., s.m., agg."
        )


def _prompt_tags(session_tags: set[str], pos_tag: str) -> list[str]:
    print(f"  (pos tag auto-added: {pos_tag})" if pos_tag else "  (no pos tag for this abbreviation)")
    non_pos_suggestions = sorted(t for t in session_tags if not t.startswith("pos::"))
    if non_pos_suggestions:
        print("  Suggestions: " + "  ".join(non_pos_suggestions))
    while True:
        raw = input("Tags (space-separated, or press Enter to skip): ").strip()
        if not raw:
            return []
        parts = raw.split()
        pos_filtered = [t for t in parts if t.startswith("pos::")]
        if pos_filtered:
            print(f"  Note: pos:: tags are auto-generated — removing {pos_filtered}")
            parts = [t for t in parts if not t.startswith("pos::")]
        invalid = [t for t in parts if not re.match(TAG_PATTERN, t)]
        if invalid:
            print(f"  Invalid tag(s): {invalid}")
            print(f"  Format: namespace::value  (lowercase letters/underscores only)")
            continue
        return parts


def _collect_word(session_tags: set[str]) -> WordEntry:
    print()
    italian = _prompt("Italian word")
    english = _prompt("English definition")
    pos = _prompt_pos()
    example_it = _prompt("Example sentence (Italian)", required=False)
    example_en = _prompt("Example translation", required=False) if example_it else ""
    extra_info = _prompt("Extra info / badge text", required=False)
    dictionary_link = _prompt("Dictionary link", required=False)
    tags = _prompt_tags(session_tags, compute_pos_tag(pos))
    session_tags.update(tags)
    return WordEntry(
        italian=italian,
        english=english,
        part_of_speech=pos,
        tags=tags,
        example_it=example_it,
        example_en=example_en,
        extra_info=extra_info,
        dictionary_link=dictionary_link,
    )


def _default_output_path() -> Path:
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return Path("words") / f"{ts}.json"


def _save(entries: list[WordEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict] = []
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    all_entries = existing + [e.to_dict() for e in entries]
    path.write_text(json.dumps(all_entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved {len(entries)} word(s) to {path}  ({len(all_entries)} total in file)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactively build a word batch JSON file for anki-add."
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output JSON file path (default: words/YYYY-MM-DD_HHmmss.json)",
    )
    args = parser.parse_args()

    print("Italian Vocabulary — Add Words")
    print("Press Ctrl-C to cancel at any time.\n")

    entries: list[WordEntry] = []
    session_tags: set[str] = set()

    try:
        while True:
            entry = _collect_word(session_tags)
            entries.append(entry)
            print(f"  ✓ Added: {entry.italian!r}")
            again = input("\nAdd another word? [Y/n]: ").strip().lower()
            if again in ("n", "no"):
                break
    except KeyboardInterrupt:
        print("\nCancelled.")
        if not entries:
            sys.exit(0)

    if not entries:
        print("No words collected.")
        sys.exit(0)

    default_path = args.output or _default_output_path()
    raw = input(f"\nSave to [{default_path}]: ").strip()
    output_path = Path(raw) if raw else default_path

    _save(entries, output_path)
    print(f"\nRun:  uv run anki-add {output_path}")


if __name__ == "__main__":
    main()
