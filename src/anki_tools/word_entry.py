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

TAG_PATTERN = r"^[a-z_]+::[a-z0-9_]+$"


@dataclass
class WordEntry:
    italian: str
    english: str
    part_of_speech: str
    tags: list[str] = field(default_factory=list)
    example_it: str = ""
    example_en: str = ""
    dictionary_link: str = ""
    extra_info: str = ""

    def to_dict(self) -> dict:
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
