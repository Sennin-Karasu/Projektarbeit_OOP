from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from .models import Project, Information, Comment, InfoType, CommentKind
from .repository import JsonRepository
from .validators import (
    normalize_tags,
    validate_project_fields,
    validate_information_fields,
    validate_comment_fields,
)

class KnowledgeService:
    def __init__(self, repo: JsonRepository):
        self.repo = repo

    def create_project(
        self,
        name: str,
        customer: str,
        leader: str,
        core_requirements: str,
        employees: List[str] | None = None,
    ) -> Project:
        validate_project_fields(name, customer, leader, core_requirements)
        p = Project.create(name, customer, leader, core_requirements, employees=employees)
        self.repo.add_project(p)
        return p

    def list_projects(self) -> List[Project]:
        return self.repo.list_projects()

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.repo.get_project(project_id)

    def create_information(
            self,
            project_id: str,
            info_type: InfoType,
            title: str,
            content: str,
            tags: List[str],
            author: str,
    ) -> Information:
        if isinstance(info_type, str):
            info_type = InfoType(info_type)

        tags_norm = normalize_tags(tags)
        validate_information_fields(info_type, title, content, author, tags_norm)
        info = Information.create(project_id, info_type, title, content, tags_norm, author)
        self.repo.add_information(info)
        return info

    def list_informations(self, project_id: str) -> List[Information]:
        return self.repo.list_informations_for_project(project_id)

    def add_comment(
            self,
            information_id: str,
            kind: CommentKind,
            text: str,
            author: str,
    ) -> Comment:
        if isinstance(kind, str):
            kind = CommentKind(kind)

        validate_comment_fields(kind, text, author)
        c = Comment.create(information_id, kind, text, author)
        self.repo.add_comment(c)
        return c

    def list_comments(self, information_id: str) -> List[Comment]:
        return self.repo.list_comments_for_information(information_id)

    def search_informations_by_tags_loose(self, project_id: str, tags: List[str]) -> List[Information]:
        tags_norm = normalize_tags(tags)
        wanted = {t.lower() for t in tags_norm}
        infos = self.repo.list_informations_for_project(project_id)
        if not wanted:
            return infos

        result: List[Information] = []
        for info in infos:
            itags = {t.lower() for t in info.tags}
            if itags.intersection(wanted):
                result.append(info)
        return result

    def delete_project(self, project_id: str) -> None:
        project = self.repo.get_project(project_id)
        if not project:
            raise ValueError("Projekt nicht gefunden.")

        infos = self.repo.list_informations_for_project(project_id)
        for info in infos:
            for c in self.repo.list_comments_for_information(info.id):
                self.repo.remove_comment(c.id)
            self.repo.remove_information(info.id)

        self.repo.remove_project(project_id)
        self.repo.save()