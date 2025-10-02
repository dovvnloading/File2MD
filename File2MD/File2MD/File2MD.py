import sys
from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from config import STYLESHEET_MONO

# ==============================================================================
# 5. APPLICATION ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET_MONO)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())