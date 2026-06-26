"""
Definition of the "Italian Vocabulary" Anki note type.

This module is the **canonical source of truth** for the card format used
across this project.  Both the `anki-add` tool (which creates/updates the note
type via AnkiConnect) and the parent project's ``generate_anki.py`` script
(which creates ``.apkg`` files) must stay consistent with the field names and
CSS defined here.

Adding a new card template
--------------------------
Append a new entry to `TEMPLATES`.  On the next `anki-add` run,
`AnkiConnectClient.update_model_templates` will push the change to Anki
automatically — no manual steps required.

Example of a planned fill-in-the-blank template::

    {
        "name": "Fill in the Blank",
        "qfmt": '<div class="card"><div class="example-it">{{Example with blank}}</div></div>',
        "afmt": '<div class="card"><div class="example-it">{{Example}}</div> ... </div>',
    }
"""

from anki_tools.models.css import CARD_CSS

MODEL_NAME = "Italian Vocabulary"
"""Name of the Anki note type.  Must match exactly what is registered in Anki."""

FIELDS = [
    "Italian",
    "English",
    "PartOfSpeech",
    "ExtraInfo",
    "Tier",
    "TierClass",
    "DictionaryLink",
    "WordReferenceLink",
    "Example",
    "ExampleTranslation",
]
"""
Ordered list of field names for the note type.

| Field | Description |
|---|---|
| ``Italian`` | The word as it appears on the card front |
| ``English`` | Translation shown on the card back |
| ``PartOfSpeech`` | Abbreviation e.g. ``v.tr.``, ``s.m.`` |
| ``ExtraInfo`` | Pre-rendered HTML badge ``<span>`` elements |
| ``Tier`` | Frequency tier label e.g. ``Fondamentale``, ``Personale`` |
| ``TierClass`` | CSS class for tier colour; empty for personal words |
| ``DictionaryLink`` | Optional URL rendered as "Dictionary ↗" |
| ``WordReferenceLink`` | Auto-generated WordReference URL |
| ``Example`` | Italian example sentence |
| ``ExampleTranslation`` | English translation of the example |
"""

TEMPLATES = [
    {
        "name": "Italian → English",
        "qfmt": (
            '<div class="card">'
            '<div class="word">{{Italian}}</div>'
            '<div class="pos">{{PartOfSpeech}}</div>'
            "</div>"
        ),
        "afmt": (
            '<div class="card">'
            '<div class="word">{{Italian}}</div>'
            '<div class="pos">{{PartOfSpeech}}</div>'
            "<hr>"
            '<div class="translation">{{English}}</div>'
            "{{#ExtraInfo}}"
            '<div class="badges">{{ExtraInfo}}</div>'
            "{{/ExtraInfo}}"
            "{{#Example}}"
            '<div class="example">'
            '<div class="example-it">{{Example}}</div>'
            '<div class="example-en">{{ExampleTranslation}}</div>'
            "</div>"
            "{{/Example}}"
            '<div class="footer">'
            '<span class="{{TierClass}}">{{Tier}}</span>'
            '<div class="footer-links">'
            "{{#DictionaryLink}}"
            '<a class="dict-link" href="{{DictionaryLink}}">Dictionary ↗</a>'
            "{{/DictionaryLink}}"
            "{{#WordReferenceLink}}"
            '<a class="dict-link" href="{{WordReferenceLink}}">WordRef ↗</a>'
            "{{/WordReferenceLink}}"
            "</div>"
            "</div>"
            "</div>"
        ),
    },
]
"""
Card templates for this note type.  Each entry generates one Anki card per note.
Append to this list to add new card types without recreating the note type.
"""


def get_model_definition() -> dict:
    """
    Return the full AnkiConnect ``createModel`` / ``updateModelTemplates`` payload.

    The returned dict can be passed directly to `AnkiClient.create_model` or
    `AnkiClient.update_model_templates`.
    """
    return {
        "modelName": MODEL_NAME,
        "inOrderFields": FIELDS,
        "css": CARD_CSS,
        "isCloze": False,
        "cardTemplates": [
            {"Name": t["name"], "Front": t["qfmt"], "Back": t["afmt"]}
            for t in TEMPLATES
        ],
    }
