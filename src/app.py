from __future__ import annotations

from pathlib import Path

from src.core.repository import JsonRepository
from src.core.service import KnowledgeService
from src.core.models import InfoType, CommentKind


def main() -> None:
    data_path = Path(__file__).resolve().parents[1] / "data.json"
    repo = JsonRepository(data_path)
    service = KnowledgeService(repo)

    if not service.list_projects():
        p = service.create_project(
            name="Demo Projekt",
            customer="Xarelto",
            leader="Projektleiter",
            core_requirements="Kernanforderungen Demo",
            employees=["Max", "Lisa"],
        )
        info = service.create_information(
            project_id=p.id,
            info_type=InfoType.TEXT,
            title="Erste Information",
            content="Das ist ein Demo Text.",
            tags=["Analyse", "Anforderung"],
            author="Max",
        )
        service.add_comment(
            information_id=info.id,
            kind=CommentKind.ADDITION,
            text="Ergänzung zum Originaltext.",
            author="Lisa",
        )

    projects = service.list_projects()
    print(f"Projekte: {len(projects)}")
    first = projects[0]
    infos = service.list_informations(first.id)
    print(f"Erstes Projekt: {first.name}")
    print(f"Informationen: {len(infos)}")
    if infos:
        comments = service.list_comments(infos[0].id)
        print(f"Kommentare zur ersten Information: {len(comments)}")


if __name__ == "__main__":
    main()