from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List
import uuid


def iso_now() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


class InfoType(str, Enum):
    TEXT = "text"
    IMAGE_URL = "image_url"
    DOC_URL = "doc_url"


class CommentKind(str, Enum):
    COMMENT = "comment"
    ADDITION = "addition"
    CORRECTION = "correction"


@dataclass(slots=True)
class Project:
    id: str
    name: str
    customer: str
    leader: str
    core_requirements: str
    employees: List[str] = field(default_factory=list)
    info_ids: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=iso_now)

    @staticmethod
    def create(name: str, customer: str, leader: str, core_requirements: str, employees: List[str] | None = None) -> "Project":
        return Project(
            id=new_id("p"),
            name=name.strip(),
            customer=customer.strip(),
            leader=leader.strip(),
            core_requirements=core_requirements.strip(),
            employees=[e.strip() for e in (employees or []) if e and e.strip()],
        )


@dataclass(slots=True)
class Information:
    id: str
    project_id: str
    type: InfoType
    title: str
    content: str
    tags: List[str]
    author: str
    comment_ids: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=iso_now)

    @staticmethod
    def create(
        project_id: str,
        info_type: InfoType,
        title: str,
        content: str,
        tags: List[str],
        author: str,
    ) -> "Information":
        return Information(
            id=new_id("i"),
            project_id=project_id,
            type=info_type,
            title=title.strip(),
            content=content.strip(),
            tags=tags,
            author=author.strip(),
        )


@dataclass(slots=True)
class Comment:
    id: str
    information_id: str
    kind: CommentKind
    text: str
    author: str
    created_at: str = field(default_factory=iso_now)

    @staticmethod
    def create(information_id: str, kind: CommentKind, text: str, author: str) -> "Comment":
        return Comment(
            id=new_id("c"),
            information_id=information_id,
            kind=kind,
            text=text.strip(),
            author=author.strip(),
        )