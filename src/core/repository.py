from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import Project, Information, Comment, InfoType, CommentKind


class JsonRepository:
    def __init__(self, path: Path):
        self.path = path
        self._db: Dict[str, Any] = {"projects": {}, "informations": {}, "comments": {}}
        self.load()

    def load(self) -> None:
        if self.path.exists():
            try:
                self._db = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self._db = {"projects": {}, "informations": {}, "comments": {}}
        else:
            self.save()

    def save(self) -> None:
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self._db, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.path)

    def add_project(self, p: Project) -> None:
        self._db["projects"][p.id] = {
            "id": p.id,
            "name": p.name,
            "customer": p.customer,
            "leader": p.leader,
            "core_requirements": p.core_requirements,
            "employees": list(p.employees),
            "info_ids": list(p.info_ids),
            "created_at": p.created_at,
        }
        self.save()

    def list_projects(self) -> List[Project]:
        items = list(self._db["projects"].values())
        items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return [Project(**x) for x in items]

    def get_project(self, project_id: str) -> Optional[Project]:
        raw = self._db["projects"].get(project_id)
        return Project(**raw) if raw else None

    def update_project(self, p: Project) -> None:
        if p.id not in self._db["projects"]:
            raise KeyError("Projekt nicht gefunden.")
        self._db["projects"][p.id] = {
            "id": p.id,
            "name": p.name,
            "customer": p.customer,
            "leader": p.leader,
            "core_requirements": p.core_requirements,
            "employees": list(p.employees),
            "info_ids": list(p.info_ids),
            "created_at": p.created_at,
        }
        self.save()

    def add_information(self, info: Information) -> None:
        if info.project_id not in self._db["projects"]:
            raise KeyError("Projekt nicht gefunden.")

        self._db["informations"][info.id] = {
            "id": info.id,
            "project_id": info.project_id,
            "type": info.type.value,
            "title": info.title,
            "content": info.content,
            "tags": list(info.tags),
            "author": info.author,
            "comment_ids": list(info.comment_ids),
            "created_at": info.created_at,
        }

        proj = self._db["projects"][info.project_id]
        proj.setdefault("info_ids", [])
        proj["info_ids"].append(info.id)

        self.save()

    def get_information(self, info_id: str) -> Optional[Information]:
        raw = self._db["informations"].get(info_id)
        if not raw:
            return None
        raw = dict(raw)
        raw["type"] = InfoType(raw["type"])
        return Information(**raw)

    def list_informations_for_project(self, project_id: str) -> List[Information]:
        proj = self._db["projects"].get(project_id)
        if not proj:
            return []
        infos: List[Information] = []
        for iid in proj.get("info_ids", []):
            it = self.get_information(iid)
            if it:
                infos.append(it)
        infos.sort(key=lambda x: x.created_at, reverse=True)
        return infos

    def update_information(self, info: Information) -> None:
        if info.id not in self._db["informations"]:
            raise KeyError("Information nicht gefunden.")
        self._db["informations"][info.id] = {
            "id": info.id,
            "project_id": info.project_id,
            "type": info.type.value,
            "title": info.title,
            "content": info.content,
            "tags": list(info.tags),
            "author": info.author,
            "comment_ids": list(info.comment_ids),
            "created_at": info.created_at,
        }
        self.save()

    def add_comment(self, c: Comment) -> None:
        if c.information_id not in self._db["informations"]:
            raise KeyError("Information nicht gefunden.")

        self._db["comments"][c.id] = {
            "id": c.id,
            "information_id": c.information_id,
            "kind": c.kind.value,
            "text": c.text,
            "author": c.author,
            "created_at": c.created_at,
        }

        info = self._db["informations"][c.information_id]
        info.setdefault("comment_ids", [])
        info["comment_ids"].append(c.id)

        self.save()

    def list_comments_for_information(self, info_id: str) -> List[Comment]:
        info = self._db["informations"].get(info_id)
        if not info:
            return []
        out: List[Comment] = []
        for cid in info.get("comment_ids", []):
            raw = self._db["comments"].get(cid)
            if raw:
                raw = dict(raw)
                raw["kind"] = CommentKind(raw["kind"])
                out.append(Comment(**raw))
        out.sort(key=lambda x: x.created_at)
        return out