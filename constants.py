MODERN_DARK_THEME = """
QWidget {
    background-color: #282a36;
    color: #f8f8f2;
    font-family: 'Segoe UI';
    font-size: 14px;
}
QMainWindow {
    background-color: #282a36;
}
QFrame#container {
    border: 1px solid #44475a;
    border-radius: 10px;
    background-color: #282a36;
}
QWidget#title_bar {
    background-color: #44475a;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
QPushButton {
    background-color: #6272a4;
    color: #f8f8f2;
    border: 1px solid #bd93f9;
    padding: 8px 16px;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: #7e8ccf;
}
QPushButton:pressed {
    background-color: #5a68a3;
}
QPushButton#loadButton {
    background-color: #50fa7b;
    color: #282a36;
    font-weight: bold;
}
QPushButton#scrapeButton {
    background-color: #bd93f9;
    color: #f8f8f2;
    font-weight: bold;
}
QPushButton#close_button {
    background-color: transparent;
    border: none;
    font-size: 16px;
    font-weight: bold;
    border-radius: 5px;
}
QWidget#title_bar QPushButton#close_button:hover {
    background-color: #ff5555;
}
QLineEdit {
    background-color: #44475a;
    border: 1px solid #6272a4;
    padding: 8px;
    border-radius: 5px;
    color: #f8f8f2;
}
QTextEdit {
    background-color: #44475a;
    border: 1px solid #6272a4;
    border-radius: 5px;
    color: #f8f8f2;
}
QGroupBox {
    font-weight: bold;
    color: #bd93f9;
    border: 1px solid #6272a4;
    border-radius: 8px;
    margin-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    left: 10px;
}
QLabel {
    color: #f8f8f2;
    background: transparent;
}
QStatusBar {
    color: #f8f8f2;
}
QProgressBar {
    border: 1px solid #6272a4;
    border-radius: 5px;
    text-align: center;
    color: #f8f8f2; /* Reverted to white */
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: #00d084;
    border-radius: 4px;
}
QSplitter::handle {
    background-color: #44475a;
}
QSplitter::handle:horizontal {
    width: 5px;
}
QSplitter::handle:vertical {
    height: 5px;
}
QScrollBar:vertical {
    border: none;
    background: #282a36;
    width: 12px;
    margin: 15px 0 15px 0;
    border-radius: 6px;
}
QScrollBar::handle:vertical {
    background-color: #6272a4;
    min-height: 30px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background-color: #7e8ccf;
}
QScrollBar::handle:vertical:pressed {
    background-color: #5a68a3;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: #282a36;
    height: 12px;
    margin: 0 15px 0 15px;
    border-radius: 6px;
}
QScrollBar::handle:horizontal {
    background-color: #6272a4;
    min-width: 30px;
    border-radius: 6px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #7e8ccf;
}
QScrollBar::handle:horizontal:pressed {
    background-color: #5a68a3;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}
/* --- Tab Widget --- */
QTabWidget::pane {
    border: 1px solid #44475a;
    border-top: none;
}
QTabBar::tab {
    background: #282a36;
    border: 1px solid #44475a;
    border-bottom: none;
    padding: 8px 20px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}
QTabBar::tab:selected {
    background: #44475a;
    font-weight: bold;
}
QTabBar::tab:!selected:hover {
    background: #3a3c4e;
}

/* --- Table Widget --- */
QTableWidget {
    background-color: #44475a;
    gridline-color: #6272a4;
    border: 1px solid #6272a4;
}
QHeaderView::section {
    background-color: #282a36;
    color: #bd93f9;
    padding: 4px;
    border: 1px solid #6272a4;
    font-weight: bold;
}
QTableWidget::item {
    padding: 5px;
}
QTableWidget::item:selected {
    background-color: #6272a4;
    color: #f8f8f2;
}
"""