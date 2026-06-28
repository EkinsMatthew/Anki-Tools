"""
Shared CSS for all "Italian Vocabulary" card templates.

This is the **canonical** stylesheet for the note type defined in
``models.italian_vocabulary``.  Any other tool that builds an ``.apkg``
containing the same note type (e.g. via genanki) should import this constant
rather than duplicating it.

When making visual changes, edit `CARD_CSS` here, then re-run ``anki-add``
on any batch file — ``update_model_templates`` will push the updated CSS to
the live note type in Anki automatically.
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
.badge.badge-volgare {
    background: #c0392b;
    color: #fff;
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
.blank {
    display: inline-block;
    border-bottom: 2px solid #1a1a2e;
    padding: 0 6px;
    font-style: normal;
    font-weight: 600;
    letter-spacing: 2px;
    color: #1a1a2e;
    min-width: 2.5em;
    text-align: center;
}
"""
