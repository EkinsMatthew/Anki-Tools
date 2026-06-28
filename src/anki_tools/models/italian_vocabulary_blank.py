"""
Definition of the "Italian Vocabulary — Blank" Anki note type.

A single-template note type purpose-built for fill-in-the-blank practice.
Each note generates exactly one card: the sentence with the target word
replaced by a blank on the front, and the word + translation revealed on
the back.
"""

MODEL_NAME = "Italian Vocabulary — Blank"

FIELDS = [
    "Italian",
    "English",
    "PartOfSpeech",
    "ExtraInfo",
    "DictionaryLink",
    "WordReferenceLink",
    "Example",
    "ExampleTranslation",
    "ExampleWithBlank",
]

CARD_CSS = """
.card {
    font-family: Georgia, serif;
    text-align: center;
    background: #fafafa;
    color: #222;
    padding: 24px;
    max-width: 520px;
    margin: 0 auto;
}
.sentence {
    font-size: 1.35em;
    font-style: italic;
    color: #1a1a2e;
    line-height: 1.8;
    margin: 20px 0 12px;
}
.blank {
    display: inline-block;
    border-bottom: 2px solid #1a1a2e;
    min-width: 1em;
    padding: 0 4px;
    color: transparent;
    line-height: 1.2;
}
.pos-hint {
    font-size: 0.82em;
    color: #bbb;
    font-style: italic;
    margin-top: 6px;
}
.reveal {
    border-top: 1px solid #ddd;
    margin-top: 20px;
    padding-top: 18px;
}
.answer {
    font-size: 2em;
    font-weight: bold;
    color: #1a1a2e;
    margin-bottom: 6px;
}
.translation {
    font-size: 1.1em;
    color: #555;
    margin-bottom: 12px;
}
.example-en {
    font-size: 0.88em;
    color: #888;
    font-style: italic;
    margin: 10px 0;
}
.badges {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 6px;
    margin-bottom: 12px;
}
.badge {
    display: inline-block;
    background: #e8e8e8;
    color: #444;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 0.78em;
    font-family: monospace;
}
.badge.badge-volgare {
    background: #c0392b;
    color: #fff;
}
.footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    font-size: 0.75em;
    color: #aaa;
    margin-top: 16px;
}
.dict-link {
    color: #aaa;
    text-decoration: none;
}
.dict-link:hover {
    text-decoration: underline;
}
"""

_FRONT = (
    '<div class="card">'
    '<div class="sentence">{{ExampleWithBlank}}</div>'
    '<div class="pos-hint">{{PartOfSpeech}}</div>'
    "</div>"
)

_BACK = (
    '<div class="card">'
    '<div class="sentence">{{Example}}</div>'
    '<div class="pos-hint">{{PartOfSpeech}}</div>'
    '<div class="reveal">'
    '<div class="answer">{{Italian}}</div>'
    '<div class="translation">{{English}}</div>'
    "{{#ExtraInfo}}"
    '<div class="badges">{{ExtraInfo}}</div>'
    "{{/ExtraInfo}}"
    "{{#ExampleTranslation}}"
    '<div class="example-en">{{ExampleTranslation}}</div>'
    "{{/ExampleTranslation}}"
    "</div>"
    '<div class="footer">'
    "{{#DictionaryLink}}"
    '<a class="dict-link" href="{{DictionaryLink}}">Dictionary ↗</a>'
    "{{/DictionaryLink}}"
    "{{#WordReferenceLink}}"
    '<a class="dict-link" href="{{WordReferenceLink}}">WordRef ↗</a>'
    "{{/WordReferenceLink}}"
    "</div>"
    "</div>"
)

TEMPLATES = [
    {
        "name": "Fill in the Blank",
        "qfmt": _FRONT,
        "afmt": _BACK,
    }
]


def get_model_definition() -> dict:
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
