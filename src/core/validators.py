from __future__ import annotations

import re
from typing import List
from .models import InfoType, CommentKind


def normalize_tags(tags: List[str]) -> List[str]:
    cleaned = [t.strip() for t in tags if t and t.strip()]
    out: List[str] = []
    seen = set()
    for t in cleaned:
        key = t.lower()
        if key not in seen:
            seen.add(key)
            out.append(t)
    return out


def is_url(value: str) -> bool:
    return bool(re.match(r"^https?://", (value or "").strip(), flags=re.IGNORECASE))


def validate_project_fields(name: str, customer: str, leader: str, core: str) -> None:
    if not name.strip():
        raise ValueError("Projektname ist Pflicht.")
    if not customer.strip():
        raise ValueError("Kunde ist Pflicht.")
    if not leader.strip():
        raise ValueError("Projektleiter ist Pflicht.")
    if not core.strip():
        raise ValueError("Kernanforderungen sind Pflicht.")


def validate_information_fields(info_type: InfoType, title: str, content: str, author: str, tags: List[str]) -> None:
    if not title.strip():
        raise ValueError("Titel ist Pflicht.")
    if not author.strip():
        raise ValueError("Autor ist Pflicht.")
    if info_type == InfoType.TEXT and not content.strip():
        raise ValueError("Text Inhalt ist Pflicht.")
    if info_type in (InfoType.IMAGE_URL, InfoType.DOC_URL) and not is_url(content):
        raise ValueError("Für Bild oder Dokument wird eine URL mit http oder https benötigt.")
    if len(tags) > 3:
        raise ValueError("Maximal drei Tags pro Information sind erlaubt.")


def validate_comment_fields(kind: CommentKind, text: str, author: str) -> None:
    if kind not in (CommentKind.COMMENT, CommentKind.ADDITION, CommentKind.CORRECTION):
        raise ValueError("Ungültige Kommentarart.")
    if not author.strip():
        raise ValueError("Autor ist Pflicht.")
    if not text.strip():
        raise ValueError("Text ist Pflicht.")