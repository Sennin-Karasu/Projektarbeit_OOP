import sys
from PySide6.QtWidgets import QApplication
from pathlib import Path

from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # optional: QSS laden
    qss_path = Path(__file__).parent / "ui" / "style.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
