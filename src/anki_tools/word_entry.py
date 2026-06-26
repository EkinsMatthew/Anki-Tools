"""
Core data model for a single vocabulary entry.

A `WordEntry` represents one Italian word and all the information needed to
create an Anki card for it. Entries are serialized to / deserialized from the
JSON batch files that `anki-cli` produces and `anki-add` consumes.
"""

from dataclasses import dataclass, field

ITALIAN_ABBREVS: list[str] = [
    "v.tr.",
    "v.intr.",
    "v.pronom.",
    "s.m.",
    "s.f.",
    "s.m.inv.",
    "s.f.inv.",
    "agg.",
    "avv.",
    "prep.",
    "cong.",
    "pron.",
    "art.",
    "inter.",
    "num.",
]
"""
Recognised Italian part-of-speech abbreviations, in the order they are
displayed by `anki-cli`.  The `part_of_speech` field of a `WordEntry` must
be one of these values.
"""

TAG_PATTERN = r"^[a-z_]+::[a-z0-9_]+$"
"""
Regex that every user-supplied Anki tag must match.

Tags follow the ``namespace::value`` convention already used by the main
vocabulary deck (e.g. ``tier::fondamentale``, ``group::colors``).  Both
segments are restricted to lowercase ASCII letters, digits, and underscores
so that tags survive round-trips through Anki's tag normalisation.
"""


@dataclass
class WordEntry:
    """
    A single Italian vocabulary word and all data needed to build its Anki card.

    Required fields must be supplied at construction time; optional fields
    default to empty strings or an empty list and are omitted from the card
    template when blank.

    Attributes:
        italian: The Italian word exactly as it should appear on the card front.
        english: English translation shown on the card back.
        part_of_speech: Grammatical category; must be a value from
            `ITALIAN_ABBREVS` (e.g. ``"v.tr."``, ``"s.m."``).
        tags: Extra Anki tags to attach to the note, beyond the ``pos::*`` tag
            that `card_builder.build_tags` adds automatically.  Use
            ``category::`` tags to group personal words
            (e.g. ``category::parole_che_ho_incontrato``).
        example_it: Example sentence in Italian (optional).
        example_en: English translation of `example_it` (optional).
        dictionary_link: Direct URL to an online dictionary entry (optional).
            Rendered as a "Dictionary ↗" link on the card back.
        extra_info: Free-form grammatical note rendered as a badge on the card
            back (optional).  Use sparingly — e.g. ``"Irr PP: visto"``.
    """

    italian: str
    english: str
    part_of_speech: str
    tags: list[str] = field(default_factory=list)
    example_it: str = ""
    example_en: str = ""
    dictionary_link: str = ""
    extra_info: str = ""

    def to_dict(self) -> dict:
        """Serialize to a plain dict suitable for JSON output."""
        return {
            "italian": self.italian,
            "english": self.english,
            "part_of_speech": self.part_of_speech,
            "tags": self.tags,
            "example_it": self.example_it,
            "example_en": self.example_en,
            "dictionary_link": self.dictionary_link,
            "extra_info": self.extra_info,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WordEntry":
        """
        Deserialize from a plain dict (e.g. one entry in a JSON batch file).

        `italian`, `english`, and `part_of_speech` are required keys.
        All other keys are optional and default to empty values when absent.

        Raises:
            KeyError: if a required key is missing from `data`.
        """
        return cls(
            italian=data["italian"],
            english=data["english"],
            part_of_speech=data["part_of_speech"],
            tags=data.get("tags", []),
            example_it=data.get("example_it", ""),
            example_en=data.get("example_en", ""),
            dictionary_link=data.get("dictionary_link", ""),
            extra_info=data.get("extra_info", ""),
        )
