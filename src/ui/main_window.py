from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSplitter, QTableWidget, QTableWidgetItem,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget, QComboBox, QPlainTextEdit
)


# -------------------------
# Fake data just for GUI preview
# -------------------------
@dataclass(slots=True)
class FakeProject:
    name: str
    customer: str
    leader: str
    core: str


@dataclass(slots=True)
class FakeInfo:
    title: str
    type_label: str
    tags: str
    created_by: str
    date: str
    detail_html: str


def demo_projects() -> List[FakeProject]:
    return [
        FakeProject("Intranet Relaunch", "Muster AG", "Max Muster", "Login, Rollen, Suche, CMS"),
        FakeProject("Mobile App", "Beispiel GmbH", "Lisa Example", "Offline-Mode, Push, Analytics"),
        FakeProject("ERP Schnittstelle", "Contoso", "Tom Test", "CSV Import, Validierung, Logs"),
    ]


def demo_infos_for(project_index: int) -> List[FakeInfo]:
    if project_index == 0:
        return [
            FakeInfo(
                "Kickoff-Protokoll", "Text", "Analyse, Anforderung",
                "Max", "2026-02-02",
                "<h2>Kickoff-Protokoll</h2>"
                "<p><b>Original:</b> Scope, Stakeholder, Zeitplan …</p>"
                "<hr><h3>Kommentare</h3>"
                "<div style='padding:10px;border-radius:10px;background:#f5f5f5;'>"
                "<b>Kommentar</b> — Lisa (2026-02-02)<br>Bitte SSO berücksichtigen."
                "</div>"
                "<div style='margin-top:10px;padding:10px;border-radius:10px;background:#e7f5ff;border-left:5px solid #0d6efd;'>"
                "<b>Ergänzung</b> — Tom (2026-02-03)<br>SSO via Azure AD möglich."
                "</div>"
            ),
            FakeInfo(
                "Design-Entwurf", "Bild-URL", "Design",
                "Lisa", "2026-02-05",
                "<h2>Design-Entwurf</h2><p><b>Link:</b> https://example.com/mockup.png</p>"
            ),
        ]
    if project_index == 1:
        return [
            FakeInfo(
                "Anforderungen v1", "Text", "Anforderung",
                "Lisa", "2026-01-12",
                "<h2>Anforderungen v1</h2><p>Offline Mode, Push Notifications …</p>"
                "<hr><h3>Korrekturen</h3>"
                "<div style='padding:10px;border-radius:10px;background:#fff3cd;border-left:5px solid #ffc107;'>"
                "<b>Korrektur</b> — Max (2026-01-13)<br>Push nur für Android in Phase 1."
                "</div>"
            ),
        ]
    return [
        FakeInfo(
            "Spezifikation", "Dok-URL", "Analyse, Design",
            "Tom", "2026-01-20",
            "<h2>Spezifikation</h2><p><b>Link:</b> https://example.com/spec.pdf</p>"
        )
    ]


# -------------------------
# Main Window (GUI only)
# -------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wissensmanagement – GUI Prototyp")
        self.resize(1200, 750)

        self._projects = demo_projects()
        self._current_project_index: Optional[int] = None
        self._current_infos: List[FakeInfo] = []

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(14, 14, 14, 14)
        root_layout.setSpacing(12)
        self.setCentralWidget(root)

        # Split: sidebar + content
        splitter = QSplitter()
        splitter.setHandleWidth(8)
        root_layout.addWidget(splitter)

        # Sidebar frame
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

        btn_row = QHBoxLayout()
        self.btn_new_project = QPushButton("Neues Projekt")
        self.btn_edit_project = QPushButton("Bearbeiten")
        btn_row.addWidget(self.btn_new_project)
        btn_row.addWidget(self.btn_edit_project)
        sidebar_layout.addLayout(btn_row)

        splitter.addWidget(sidebar)

        # Content frame
        content = QFrame()
        content.setObjectName("Content")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(10)

        # Tabs
        self.tabs = QTabWidget()
        content_layout.addWidget(self.tabs, 1)

        # ----- Tab: Informationen -----
        tab_infos = QWidget()
        infos_layout = QVBoxLayout(tab_infos)
        infos_layout.setContentsMargins(0, 0, 0, 0)
        infos_layout.setSpacing(10)

        # Tag filter row (loose tags)
        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        filter_row.addWidget(QLabel("Tag 1"))
        self.tag1 = QComboBox(); self.tag1.setEditable(True)
        filter_row.addWidget(self.tag1)

        filter_row.addWidget(QLabel("Tag 2"))
        self.tag2 = QComboBox(); self.tag2.setEditable(True)
        filter_row.addWidget(self.tag2)

        filter_row.addWidget(QLabel("Tag 3"))
        self.tag3 = QComboBox(); self.tag3.setEditable(True)
        filter_row.addWidget(self.tag3)

        self.btn_search = QPushButton("Suchen")
        filter_row.addWidget(self.btn_search)

        filter_row.addStretch(1)
        infos_layout.addLayout(filter_row)

        # Action buttons
        action_row = QHBoxLayout()
        self.btn_new_info = QPushButton("Neue Info")
        self.btn_add_comment = QPushButton("Kommentar hinzufügen")
        action_row.addWidget(self.btn_new_info)
        action_row.addWidget(self.btn_add_comment)
        action_row.addStretch(1)
        infos_layout.addLayout(action_row)

        # Table + detail
        self.info_table = QTableWidget(0, 5)
        self.info_table.setHorizontalHeaderLabels(["Titel", "Typ", "Tags", "Erstellt von", "Datum"])
        self.info_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.info_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.info_table.horizontalHeader().setStretchLastSection(True)
        infos_layout.addWidget(self.info_table, 2)

        infos_layout.addWidget(QLabel("Detailansicht"))
        self.detail = QTextBrowser()
        self.detail.setOpenExternalLinks(True)
        self.detail.setHtml("<i>Wähle links ein Projekt aus…</i>")
        infos_layout.addWidget(self.detail, 2)

        self.tabs.addTab(tab_infos, "Informationen")

        # ----- Tab: Projekt-Details -----
        tab_details = QWidget()
        details_layout = QVBoxLayout(tab_details)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(10)

        self.lbl_p_name = QLabel("Projekt: –")
        self.lbl_p_customer = QLabel("Kunde: –")
        self.lbl_p_leader = QLabel("Projektleiter: –")
        self.txt_core = QPlainTextEdit()
        self.txt_core.setReadOnly(True)
        self.txt_core.setPlaceholderText("Kernanforderungen…")

        details_layout.addWidget(self.lbl_p_name)
        details_layout.addWidget(self.lbl_p_customer)
        details_layout.addWidget(self.lbl_p_leader)
        details_layout.addWidget(QLabel("Kernanforderungen"))
        details_layout.addWidget(self.txt_core, 1)

        self.tabs.addTab(tab_details, "Projekt-Details")

        splitter.addWidget(content)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        # Wire signals (nur GUI-Demo)
        self.project_list.currentItemChanged.connect(self._on_project_changed)
        self.info_table.itemSelectionChanged.connect(self._on_info_selected)

        # Buttons do nothing yet – only placeholders
        self.btn_new_project.clicked.connect(lambda: self._toast("GUI only", "Projekt-Dialog kommt später (wenn Layout passt)."))
        self.btn_edit_project.clicked.connect(lambda: self._toast("GUI only", "Bearbeiten kommt später."))
        self.btn_new_info.clicked.connect(lambda: self._toast("GUI only", "Info-Dialog kommt später (wenn Layout passt)."))
        self.btn_add_comment.clicked.connect(lambda: self._toast("GUI only", "Kommentar-Dialog kommt später."))
        self.btn_search.clicked.connect(lambda: self._toast("GUI only", "Suche wird später angebunden."))

        # Fill project list (demo)
        self._populate_projects()

    def _toast(self, title: str, msg: str) -> None:
        # bewusst simpel, damit UI nicht nervt
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, title, msg)

    def _populate_projects(self) -> None:
        self.project_list.clear()
        for idx, p in enumerate(self._projects):
            item = QListWidgetItem(f"{p.name} — {p.customer}")
            item.setData(Qt.UserRole, idx)
            self.project_list.addItem(item)

        if self._projects:
            self.project_list.setCurrentRow(0)

    def _on_project_changed(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        if not current:
            return
        idx = current.data(Qt.UserRole)
        self._current_project_index = int(idx)

        p = self._projects[self._current_project_index]
        self.lbl_p_name.setText(f"Projekt: {p.name}")
        self.lbl_p_customer.setText(f"Kunde: {p.customer}")
        self.lbl_p_leader.setText(f"Projektleiter: {p.leader}")
        self.txt_core.setPlainText(p.core)

        # load demo infos
        self._current_infos = demo_infos_for(self._current_project_index)
        self._populate_infos_table()

    def _populate_infos_table(self) -> None:
        self.info_table.setRowCount(0)
        for info in self._current_infos:
            r = self.info_table.rowCount()
            self.info_table.insertRow(r)
            values = [info.title, info.type_label, info.tags, info.created_by, info.date]
            for c, v in enumerate(values):
                it = QTableWidgetItem(v)
                if c == 0:
                    it.setData(Qt.UserRole, r)  # index in _current_infos
                self.info_table.setItem(r, c, it)

        if self.info_table.rowCount() > 0:
            self.info_table.selectRow(0)
        else:
            self.detail.setHtml("<i>Keine Infos (Demo).</i>")

    def _on_info_selected(self) -> None:
        row = self.info_table.currentRow()
        if row < 0:
            return
        first = self.info_table.item(row, 0)
        if not first:
            return
        idx = int(first.data(Qt.UserRole))
        info = self._current_infos[idx]
        self.detail.setHtml(info.detail_html)
