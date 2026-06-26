"""
Shared CSS for all "Italian Vocabulary" card templates.

This is the **canonical** stylesheet — both this tool (via AnkiConnect) and
the parent project's ``generate_anki.py`` (via genanki) must use the same
CSS so that personal cards and frequency-list cards look identical in Anki.

When making visual changes, edit `CARD_CSS` here, then:

1. Re-run ``anki-add`` on any batch file — it calls ``update_model_templates``
   which pushes the new CSS to the existing note type in Anki.
2. Regenerate the parent project's ``.apkg`` so the genanki-built model also
   picks up the change.
"""

CARD_CSS = """
.card {
    font-family: Georgia, serif;
    text-align: center;
    background: #fafafa;
    color: #222;
    padding: 20px;
    max-width: 480px;
    margin: 0 auto;
}
.word {
    font-size: 2.2em;
    font-weight: bold;
    margin-bottom: 4px;
}
.pos {
    font-size: 0.85em;
    color: #888;
    font-style: italic;
    margin-bottom: 12px;
}
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 14px 0;
}
.translation {
    font-size: 1.5em;
    margin-bottom: 14px;
    color: #1a1a2e;
}
.badges {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 6px;
    margin-bottom: 14px;
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
.footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75em;
    color: #aaa;
    margin-top: 8px;
}
.tier-fondamentale { color: #b8860b; font-style: italic; }
.tier-alto-uso     { color: #4169e1; font-style: italic; }
.tier-alta-disp    { color: #888;    font-style: italic; }
.dict-link { color: #aaa; text-decoration: none; }
.dict-link:hover { text-decoration: underline; }
.footer-links {
    display: flex;
    gap: 12px;
}
.example {
    margin: 14px 0;
    padding: 10px;
    background: #f5f5f0;
    border-radius: 8px;
    font-size: 0.9em;
}
.example-it {
    font-style: italic;
    color: #333;
    margin-bottom: 4px;
}
.example-en {
    color: #666;
    font-size: 0.85em;
}
"""
