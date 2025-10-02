from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

# ==============================================================================
# 4. UI IMPLEMENTATION (Components)
# ==============================================================================

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setObjectName("TitleBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_label = QLabel("File2MD")
        self.title_label.setObjectName("TitleLabel")
        layout.addWidget(self.title_label)

        layout.addStretch()

        self.minimize_button = QPushButton("0")
        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        self.maximize_button = QPushButton("1")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.close_button = QPushButton("r")
        self.close_button.setObjectName("CloseButton")
        self.close_button.clicked.connect(self.parent_window.close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

    def toggle_maximize_restore(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.maximize_button.setText("1")
        else:
            self.parent_window.showMaximized()
            self.maximize_button.setText("2")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_window.start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.parent_window.start_pos is not None:
            if not self.parent_window.isMaximized():
                delta = event.globalPosition().toPoint() - self.parent_window.start_pos
                self.parent_window.move(self.parent_window.x() + delta.x(), self.parent_window.y() + delta.y())
                self.parent_window.start_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        self.parent_window.start_pos = None