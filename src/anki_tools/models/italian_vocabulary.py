from anki_tools.models.css import CARD_CSS

MODEL_NAME = "Italian Vocabulary"

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

# Each entry here generates one Anki card per note. Add new templates to this
# list to introduce new card types (e.g. fill-in-the-blank).
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


def get_model_definition() -> dict:
    """Return the full AnkiConnect createModel payload for this note type."""
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
