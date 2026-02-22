from __future__ import annotations

from typing import List, Tuple

from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QPlainTextEdit,
    QVBoxLayout, QComboBox
)

from src.core.models import InfoType, CommentKind


class ProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neues Projekt")

        self.name_edit = QLineEdit()
        self.customer_edit = QLineEdit()
        self.leader_edit = QLineEdit()
        self.core_edit = QPlainTextEdit()
        self.employees_edit = QLineEdit()

        form = QFormLayout()
        form.addRow("Projektname", self.name_edit)
        form.addRow("Kunde", self.customer_edit)
        form.addRow("Projektleiter", self.leader_edit)
        form.addRow("Kernanforderungen", self.core_edit)
        form.addRow("Mitarbeitende Namen", self.employees_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def data(self) -> Tuple[str, str, str, str, List[str]]:
        employees_raw = self.employees_edit.text().strip()
        employees = [x.strip() for x in employees_raw.split(",") if x.strip()] if employees_raw else []
        return (
            self.name_edit.text(),
            self.customer_edit.text(),
            self.leader_edit.text(),
            self.core_edit.toPlainText(),
            employees,
        )


class InformationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neue Information")

        self.type_combo = QComboBox()
        self.type_combo.addItem("Text", InfoType.TEXT)
        self.type_combo.addItem("Bild URL", InfoType.IMAGE_URL)
        self.type_combo.addItem("Dokument URL", InfoType.DOC_URL)

        self.title_edit = QLineEdit()
        self.content_edit = QPlainTextEdit()
        self.author_edit = QLineEdit()

        self.tag1 = QLineEdit()
        self.tag2 = QLineEdit()
        self.tag3 = QLineEdit()

        form = QFormLayout()
        form.addRow("Typ", self.type_combo)
        form.addRow("Titel", self.title_edit)
        form.addRow("Inhalt oder URL", self.content_edit)
        form.addRow("Autor", self.author_edit)
        form.addRow("Tag 1", self.tag1)
        form.addRow("Tag 2", self.tag2)
        form.addRow("Tag 3", self.tag3)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def data(self):
        info_type = self.type_combo.currentData()
        # Absicherung falls currentData als str zurückkommt
        if isinstance(info_type, str):
            info_type = InfoType(info_type)

        tags = [self.tag1.text(), self.tag2.text(), self.tag3.text()]
        return (
            info_type,
            self.title_edit.text(),
            self.content_edit.toPlainText(),
            tags,
            self.author_edit.text(),
        )


class CommentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kommentar hinzufügen")

        self.kind_combo = QComboBox()
        self.kind_combo.addItem("Kommentar", CommentKind.COMMENT)
        self.kind_combo.addItem("Ergänzung", CommentKind.ADDITION)
        self.kind_combo.addItem("Korrektur", CommentKind.CORRECTION)

        self.author_edit = QLineEdit()
        self.text_edit = QPlainTextEdit()

        form = QFormLayout()
        form.addRow("Art", self.kind_combo)
        form.addRow("Autor", self.author_edit)
        form.addRow("Text", self.text_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def data(self) -> Tuple[CommentKind, str, str]:
        return (
            self.kind_combo.currentData(),
            self.text_edit.toPlainText(),
            self.author_edit.text(),
        )