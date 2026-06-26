"""
# anki-tools

A maintenance tool for adding personal Italian vocabulary to an existing Anki
deck — complementing the parent project's `generate_anki.py`, which builds the
main frequency-list deck from scratch.  Where that script regenerates the
entire `.apkg` file and requires a manual import, `anki-tools` talks directly
to a running Anki instance via the
[AnkiConnect](https://foosoft.net/projects/anki-connect/) addon, so new cards
appear immediately without any import step.

---

## Package map

| Module | Purpose |
|---|---|
| `anki_tools.word_entry` | `WordEntry` dataclass — the data model for one vocabulary entry; serializes to/from the JSON batch files |
| `anki_tools.card_builder` | Converts a `WordEntry` into the 10 Anki field values and a sorted tag list |
| `anki_tools.models` | Canonical CSS stylesheet (`models.css`) and the "Italian Vocabulary" note type definition (`models.italian_vocabulary`) |
| `anki_tools.client` | `AnkiClient` abstract interface, `AnkiConnectClient` (HTTP implementation), and `ApkgClient` (future stub) |
| `anki_tools.cli` | Interactive command-line prompt (`anki-cli`) that collects word data and writes JSON batch files |
| `anki_tools.add_words` | Ingest script (`anki-add`) that reads a JSON batch file and pushes every entry to Anki |

---

## Walkthrough: adding a card

Here is what happens end-to-end when you add the word *sconto* (discount):

**Step 1 — Collect the data (`anki-cli`)**

```
$ uv run anki-cli
Italian word: sconto
English definition: discount
Parts of speech: [menu shown] → 4  (s.m.)
Example sentence (Italian): Mi fa uno sconto?
Example translation: Can you give me a discount?
Tags: category::parole_che_ho_incontrato
Save to [words/2026-06-19_204248.json]:
```

`cli.py` constructs a `WordEntry` and appends it — as a plain dict — to a
timestamped JSON file in `words/`.  The file is gitignored so personal
vocabulary stays private.

**Step 2 — Deserialize (`add_words.py`)**

```
$ uv run anki-add words/2026-06-19_204248.json
```

`add_words.load_batch()` reads the JSON array and calls
`WordEntry.from_dict()` on each item, validating that the required fields
(`italian`, `english`, `part_of_speech`) are present.

**Step 3 — Build fields (`card_builder.build_fields`)**

The `WordEntry` is mapped to the 10 fields the "Italian Vocabulary" note type
expects:

| Anki field | Value for *sconto* |
|---|---|
| `Italian` | `sconto` |
| `English` | `discount` |
| `PartOfSpeech` | `s.m.` |
| `ExtraInfo` | `""` (none supplied) |
| `Tier` | `Personale` |
| `TierClass` | `""` (no colour styling) |
| `DictionaryLink` | `""` (none supplied) |
| `WordReferenceLink` | `https://www.wordreference.com/iten/sconto` (auto-generated) |
| `Example` | `Mi fa uno sconto?` |
| `ExampleTranslation` | `Can you give me a discount?` |

**Step 4 — Build tags (`card_builder.build_tags`)**

`pos_tag("s.m.")` returns `"pos::noun"`.  This is merged with the user's
`category::parole_che_ho_incontrato` tag and the result is sorted:

```python
["category::parole_che_ho_incontrato", "pos::noun"]
```

**Step 5 — Send to Anki (`AnkiConnectClient.add_note`)**

`add_words.py` calls `client.add_note(deck_name, model_name, fields, tags)`,
which POSTs to `http://127.0.0.1:8765` (the AnkiConnect addon).  Anki creates
the note, assigns it a stable ID, and returns that ID.  The card is
immediately visible in the `Italian Vocabulary :: Personale` sub-deck.

---

## Walkthrough: how card styling works

All visual styling lives in a single place: `CARD_CSS` in `models.css`.  This
is the **canonical stylesheet** — editing it here is the only change needed to
update the look of every card.

**How it reaches Anki:**

1. `models.italian_vocabulary.get_model_definition()` bundles `CARD_CSS`
   together with the field list and card templates into a single dict.
2. On the first `anki-add` run, if the "Italian Vocabulary" note type does not
   yet exist in Anki, `AnkiConnectClient.create_model()` registers it —
   including the CSS — via AnkiConnect.
3. If the note type already exists (the normal case after the initial import),
   `AnkiConnectClient.update_model_templates()` syncs any template or CSS
   changes to Anki automatically on every `anki-add` run.

**How personal cards look:**

Personal words use `Tier = "Personale"` and an empty `TierClass`.  The card
template renders `<span class="{{TierClass}}">{{Tier}}</span>` — with no CSS
class applied, the tier label appears as plain unstyled text.  Every other
element (word, translation, example box, dictionary links, badges) is styled
identically to the main frequency-list cards.
"""
