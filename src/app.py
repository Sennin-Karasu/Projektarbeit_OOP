import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor

from src.core.repository import JsonRepository
from src.core.service import KnowledgeService
from src.ui.main_window import MainWindow


def apply_light_palette(app: QApplication) -> None:
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor("#f6f7f9"))
    pal.setColor(QPalette.Base, QColor("#ffffff"))
    pal.setColor(QPalette.AlternateBase, QColor("#f2f4f7"))
    pal.setColor(QPalette.Text, QColor("#101828"))
    pal.setColor(QPalette.WindowText, QColor("#101828"))
    pal.setColor(QPalette.ButtonText, QColor("#101828"))
    pal.setColor(QPalette.PlaceholderText, QColor("#667085"))
    pal.setColor(QPalette.Button, QColor("#ffffff"))
    pal.setColor(QPalette.Highlight, QColor("#2e90fa"))
    pal.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)


def main() -> None:
    app = QApplication(sys.argv)
    apply_light_palette(app)

    qss_path = Path(__file__).parent / "ui" / "style.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    data_path = Path(__file__).resolve().parents[1] / "data.json"
    repo = JsonRepository(data_path)
    service = KnowledgeService(repo)

    w = MainWindow(service)
    w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()