import typing as t
from dataclasses import dataclass


@dataclass
class ImageFlagging:
    votecount: int
    sexual_avg: t.Optional[int] = None
    violence_avg: t.Optional[int] = None


@dataclass
class Anime:
    id: int
    ann_id: t.Optional[int] = None
    nfo_id: t.Optional[str] = None
    title_romaji: t.Optional[str] = None
    title_kanji: t.Optional[str] = None
    year: t.Optional[int] = None
    type: t.Optional[str] = None


@dataclass
class Staff:
    sid: int
    aid: int
    name: str
    role: str
    original: t.Optional[str] = None
    note: t.Optional[str] = None


@dataclass
class Screens:
    image: t.Optional[str] = None
    rid: t.Optional[int] = None
    flagging: t.Optional[ImageFlagging] = None
    height: t.Optional[int] = None
    width: t.Optional[int] = None
