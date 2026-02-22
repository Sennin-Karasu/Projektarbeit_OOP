from __future__ import annotations

from typing import Optional, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMessageBox, QPushButton, QSplitter, QTableWidget,
    QTableWidgetItem, QTabWidget, QTextBrowser, QVBoxLayout, QWidget,
    QComboBox, QPlainTextEdit
)

from src.core.service import KnowledgeService
from src.core.models import InfoType, CommentKind, Project, Information, Comment
from src.ui.dialogs import ProjectDialog, InformationDialog, CommentDialog


def esc_html(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")


class MainWindow(QMainWindow):
    def __init__(self, service: KnowledgeService):
        super().__init__()
        self.service = service

        self.setWindowTitle("Wissensmanagement")
        self.resize(1200, 760)

        self.current_project_id: Optional[str] = None
        self.current_information_id: Optional[str] = None

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(14, 14, 14, 14)
        root_layout.setSpacing(12)
        self.setCentralWidget(root)

        splitter = QSplitter()
        splitter.setHandleWidth(8)
        root_layout.addWidget(splitter)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 12, 12, 12)
        sidebar_layout.setSpacing(10)

        title = QLabel("Projekte")
        title.setObjectName("SidebarTitle")
        sidebar_layout.addWidget(title)

        self.project_list = QListWidget()
        self.project_list.setSpacing(4)
        sidebar_layout.addWidget(self.project_list, 1)

        side_btn_row = QHBoxLayout()
        self.btn_new_project = QPushButton("Neues Projekt")
        side_btn_row.addWidget(self.btn_new_project)
        sidebar_layout.addLayout(side_btn_row)

        splitter.addWidget(sidebar)

        content = QFrame()
        content.setObjectName("Content")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(10)

        self.tabs = QTabWidget()
        content_layout.addWidget(self.tabs, 1)

        tab_infos = QWidget()
        infos_layout = QVBoxLayout(tab_infos)
        infos_layout.setContentsMargins(0, 0, 0, 0)
        infos_layout.setSpacing(10)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        filter_row.addWidget(QLabel("Tag 1"))
        self.tag1 = QComboBox()
        self.tag1.setEditable(True)
        filter_row.addWidget(self.tag1)

        filter_row.addWidget(QLabel("Tag 2"))
        self.tag2 = QComboBox()
        self.tag2.setEditable(True)
        filter_row.addWidget(self.tag2)

        filter_row.addWidget(QLabel("Tag 3"))
        self.tag3 = QComboBox()
        self.tag3.setEditable(True)
        filter_row.addWidget(self.tag3)

        self.btn_search = QPushButton("Suchen")
        filter_row.addWidget(self.btn_search)

        filter_row.addStretch(1)
        infos_layout.addLayout(filter_row)

        action_row = QHBoxLayout()
        self.btn_new_info = QPushButton("Neue Information")
        self.btn_add_comment = QPushButton("Kommentar hinzufügen")
        action_row.addWidget(self.btn_new_info)
        action_row.addWidget(self.btn_add_comment)
        action_row.addStretch(1)
        infos_layout.addLayout(action_row)

        self.info_table = QTableWidget(0, 5)
        self.info_table.setHorizontalHeaderLabels(["Titel", "Typ", "Tags", "Autor", "Datum"])
        self.info_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.info_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.info_table.horizontalHeader().setStretchLastSection(True)
        infos_layout.addWidget(self.info_table, 2)

        infos_layout.addWidget(QLabel("Detailansicht"))
        self.detail = QTextBrowser()
        self.detail.setOpenExternalLinks(True)
        infos_layout.addWidget(self.detail, 2)

        self.tabs.addTab(tab_infos, "Informationen")

        tab_details = QWidget()
        details_layout = QVBoxLayout(tab_details)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(10)

        self.lbl_p_name = QLabel("Projekt: ")
        self.lbl_p_customer = QLabel("Kunde: ")
        self.lbl_p_leader = QLabel("Projektleiter: ")
        self.txt_core = QPlainTextEdit()
        self.txt_core.setReadOnly(True)

        details_layout.addWidget(self.lbl_p_name)
        details_layout.addWidget(self.lbl_p_customer)
        details_layout.addWidget(self.lbl_p_leader)
        details_layout.addWidget(QLabel("Kernanforderungen"))
        details_layout.addWidget(self.txt_core, 1)

        self.tabs.addTab(tab_details, "Projekt Details")

        splitter.addWidget(content)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        self.btn_new_project.clicked.connect(self.on_new_project)
        self.project_list.currentItemChanged.connect(self.on_project_changed)
        self.btn_new_info.clicked.connect(self.on_new_information)
        self.btn_add_comment.clicked.connect(self.on_add_comment)
        self.btn_search.clicked.connect(self.on_search)
        self.info_table.itemSelectionChanged.connect(self.on_information_selected)

        self.load_projects()

    def error(self, msg: str) -> None:
        QMessageBox.critical(self, "Fehler", msg)

    def info(self, msg: str) -> None:
        QMessageBox.information(self, "Info", msg)

    def load_projects(self) -> None:
        self.project_list.blockSignals(True)
        self.project_list.clear()
        projects = self.service.list_projects()
        for p in projects:
            item = QListWidgetItem(f"{p.name}  {p.customer}")
            item.setData(Qt.UserRole, p.id)
            self.project_list.addItem(item)
        self.project_list.blockSignals(False)

        if projects:
            self.project_list.setCurrentRow(0)
        else:
            self.current_project_id = None
            self.current_information_id = None
            self.info_table.setRowCount(0)
            self.detail.setHtml("<i>Noch keine Projekte. Bitte ein Projekt anlegen.</i>")

    def on_new_project(self) -> None:
        dlg = ProjectDialog(self)
        from PySide6.QtWidgets import QDialog
        if dlg.exec() != QDialog.Accepted:
            return
        name, customer, leader, core, employees = dlg.data()
        try:
            self.service.create_project(name, customer, leader, core, employees)
            self.load_projects()
        except Exception as e:
            self.error(str(e))

    def on_project_changed(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        if not current:
            return
        self.current_project_id = current.data(Qt.UserRole)
        self.current_information_id = None
        self.refresh_project_details()
        self.refresh_information_list()

    def refresh_project_details(self) -> None:
        if not self.current_project_id:
            return
        p = self.service.get_project(self.current_project_id)
        if not p:
            return
        self.lbl_p_name.setText(f"Projekt: {p.name}")
        self.lbl_p_customer.setText(f"Kunde: {p.customer}")
        self.lbl_p_leader.setText(f"Projektleiter: {p.leader}")
        self.txt_core.setPlainText(p.core_requirements)

    def refresh_information_list(self, infos: Optional[List[Information]] = None) -> None:
        if not self.current_project_id:
            return
        if infos is None:
            infos = self.service.list_informations(self.current_project_id)

        tmap = {
            InfoType.TEXT: "Text",
            InfoType.IMAGE_URL: "Bild URL",
            InfoType.DOC_URL: "Dokument URL",
        }

        self.info_table.setRowCount(0)
        for info in infos:
            r = self.info_table.rowCount()
            self.info_table.insertRow(r)

            tags_str = ", ".join(info.tags)
            values = [info.title, tmap.get(info.type, info.type.value), tags_str, info.author, info.created_at]
            for c, v in enumerate(values):
                it = QTableWidgetItem(v)
                if c == 0:
                    it.setData(Qt.UserRole, info.id)
                self.info_table.setItem(r, c, it)

        if self.info_table.rowCount() > 0:
            self.info_table.selectRow(0)
        else:
            self.detail.setHtml("<i>Keine Informationen gefunden.</i>")

    def on_new_information(self) -> None:
        if not self.current_project_id:
            self.info("Bitte zuerst ein Projekt auswählen.")
            return
        dlg = InformationDialog(self)
        from PySide6.QtWidgets import QDialog
        if dlg.exec() != QDialog.Accepted:
            return
        info_type, title, content, tags, author = dlg.data()
        try:
            self.service.create_information(self.current_project_id, info_type, title, content, tags, author)
            self.refresh_information_list()
        except Exception as e:
            self.error(str(e))

    def on_add_comment(self) -> None:
        if not self.current_information_id:
            self.info("Bitte zuerst eine Information auswählen.")
            return
        dlg = CommentDialog(self)
        from PySide6.QtWidgets import QDialog
        from PySide6.QtWidgets import QDialog
        if dlg.exec() != QDialog.Accepted:
            return
        kind, text, author = dlg.data()
        try:
            self.service.add_comment(self.current_information_id, kind, text, author)
            self.render_detail()
        except Exception as e:
            self.error(str(e))

    def on_search(self) -> None:
        if not self.current_project_id:
            return
        tags = [self.tag1.currentText(), self.tag2.currentText(), self.tag3.currentText()]
        try:
            infos = self.service.search_informations_by_tags_loose(self.current_project_id, tags)
            self.refresh_information_list(infos)
        except Exception as e:
            self.error(str(e))

    def on_information_selected(self) -> None:
        row = self.info_table.currentRow()
        if row < 0:
            return
        first = self.info_table.item(row, 0)
        if not first:
            return
        self.current_information_id = first.data(Qt.UserRole)
        self.render_detail()

    def render_detail(self) -> None:
        if not self.current_information_id:
            return
        info = self.service.repo.get_information(self.current_information_id)
        if not info:
            return
        comments = self.service.list_comments(self.current_information_id)

        tmap = {
            InfoType.TEXT: "Text",
            InfoType.IMAGE_URL: "Bild URL",
            InfoType.DOC_URL: "Dokument URL",
        }

        tags_str = ", ".join(info.tags)
        html: List[str] = []
        html.append(f"<h2 style='margin-bottom:4px;'>{esc_html(info.title)}</h2>")
        html.append(
            "<div style='color:#444;'>"
            f"<b>Typ:</b> {esc_html(tmap.get(info.type, info.type.value))} "
            f"<b>Tags:</b> {esc_html(tags_str)}<br>"
            f"<b>Autor:</b> {esc_html(info.author)} "
            f"<b>Datum:</b> {esc_html(info.created_at)}"
            "</div><hr>"
        )

        if info.type == InfoType.TEXT:
            html.append(
                "<div style='padding:10px;border:1px solid #ddd;border-radius:10px;'>"
                f"{esc_html(info.content)}"
                "</div>"
            )
        else:
            url = info.content.strip()
            html.append(
                "<div style='padding:10px;border:1px solid #ddd;border-radius:10px;'>"
                f"<b>Link:</b> <a href='{esc_html(url)}'>{esc_html(url)}</a>"
                "</div>"
            )

        html.append("<hr><h3>Kommentare, Ergänzungen, Korrekturen</h3>")

        if not comments:
            html.append("<i>Noch keine Kommentare.</i>")
        else:
            for c in comments:
                label = {
                    CommentKind.COMMENT: "Kommentar",
                    CommentKind.ADDITION: "Ergänzung",
                    CommentKind.CORRECTION: "Korrektur",
                }[c.kind]

                style = {
                    CommentKind.COMMENT: "background:#f5f5f5;",
                    CommentKind.ADDITION: "background:#e7f5ff;border-left:5px solid #2e90fa;",
                    CommentKind.CORRECTION: "background:#fff3cd;border-left:5px solid #fdb022;",
                }[c.kind]

                html.append(
                    f"<div style='margin:10px 0;padding:10px;border-radius:10px;{style}'>"
                    f"<b>{label}</b>  {esc_html(c.author)} "
                    f"<span style='color:#666;'>({esc_html(c.created_at)})</span><br>"
                    f"{esc_html(c.text)}"
                    "</div>"
                )

        self.detail.setHtml("\n".join(html))