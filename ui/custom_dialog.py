from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton,
                               QHBoxLayout, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

class CustomMessageBox(QDialog):
    """
    A custom, modern-styled message box.
    """
    def __init__(self, parent=None, title="Message", message=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.old_pos = None

        # --- Main Layout ---
        self.container = QWidget(self)
        self.container.setObjectName("messageBoxContainer")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(1, 1, 1, 1)

        # --- Title Bar ---
        self.title_bar = QWidget()
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 5, 0)
        
        icon_label = QLabel()
        # Menggunakan ikon standar window untuk konsistensi
        icon = self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxQuestion)
        icon_label.setPixmap(icon.pixmap(20, 20))
        
        title_label = QLabel(title)
        title_label.setObjectName("titleLabel")
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # --- Message Area ---
        message_area = QWidget()
        message_layout = QHBoxLayout(message_area)
        message_layout.setContentsMargins(20, 20, 20, 20)
        
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        message_layout.addWidget(self.message_label)

        # --- Button Layout ---
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 0, 20, 20)
        button_layout.setSpacing(10)
        button_layout.addStretch()

        self.ok_button = QPushButton("Ya")
        self.ok_button.setObjectName("okButton")
        self.ok_button.setMinimumWidth(80)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Tidak")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.setMinimumWidth(80)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()

        layout.addWidget(self.title_bar)
        layout.addWidget(message_area)
        layout.addLayout(button_layout)

        self.set_stylesheet()

    def set_stylesheet(self):
        self.setStyleSheet("""
            QWidget#messageBoxContainer {
                background-color: #282a36; /* Dracula Background */
                border: 1px solid #bd93f9; /* Dracula Purple */
                border-radius: 10px;
            }
            QWidget#titleBar {
                background-color: #44475a; /* Dracula Current Line */
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid #6272a4;
            }
            QLabel#titleLabel {
                color: #f8f8f2; /* Dracula Foreground */
                font-weight: bold;
                font-size: 14px;
            }
            QLabel {
                color: #f8f8f2;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton#okButton {
                background-color: #50fa7b; /* Dracula Green */
                color: #282a36;
                border: 1px solid #50fa7b;
            }
            QPushButton#okButton:hover {
                background-color: #61ff8c;
            }
            QPushButton#cancelButton {
                background-color: #ff5555; /* Dracula Red */
                color: #f8f8f2;
                border: 1px solid #ff5555;
            }
            QPushButton#cancelButton:hover {
                background-color: #ff6e6e;
            }
        """)

    def mousePressEvent(self, event):
        if self.title_bar.underMouse() and event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None