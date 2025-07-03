#!/usr/bin/env python3
"""
Template Dasar PySide6 - Aplikasi GUI Desktop Sederhana
Membutuhkan: pip install PySide6
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QTextEdit, QStatusBar, QMenuBar, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi PySide6 - Template Dasar")
        self.setGeometry(100, 100, 800, 600)
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        
    def setup_ui(self):
        """Setup komponen UI utama"""
        # Widget utama
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout utama
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("Selamat Datang di Aplikasi PySide6")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Input section
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Masukkan nama Anda...")
        input_layout.addWidget(QLabel("Nama:"))
        input_layout.addWidget(self.name_input)
        
        self.greet_button = QPushButton("Sapa")
        self.greet_button.clicked.connect(self.greet_user)
        input_layout.addWidget(self.greet_button)
        
        main_layout.addLayout(input_layout)
        
        # Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Output akan muncul di sini...")
        main_layout.addWidget(self.output_text)
        
        # Button section
        button_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("Bersihkan")
        self.clear_button.clicked.connect(self.clear_output)
        button_layout.addWidget(self.clear_button)
        
        self.exit_button = QPushButton("Keluar")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)
        
        main_layout.addLayout(button_layout)
        
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = file_menu.addAction("Baru")
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Keluar")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Bantuan")
        about_action = help_menu.addAction("Tentang")
        about_action.triggered.connect(self.show_about)
        
    def setup_statusbar(self):
        """Setup status bar"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Siap")
        
    def greet_user(self):
        """Fungsi untuk menyapa pengguna"""
        name = self.name_input.text().strip()
        if name:
            greeting = f"Halo {name}! Selamat datang di aplikasi PySide6.\n"
            self.output_text.append(greeting)
            self.statusbar.showMessage(f"Menyapa {name}")
            self.name_input.clear()
        else:
            QMessageBox.warning(self, "Peringatan", "Silakan masukkan nama terlebih dahulu!")
            
    def clear_output(self):
        """Bersihkan area output"""
        self.output_text.clear()
        self.statusbar.showMessage("Output dibersihkan")
        
    def new_file(self):
        """Fungsi untuk file baru"""
        self.output_text.clear()
        self.name_input.clear()
        self.statusbar.showMessage("File baru dibuat")
        
    def show_about(self):
        """Tampilkan dialog tentang aplikasi"""
        QMessageBox.about(self, "Tentang", 
                         "Template PySide6\n\n"
                         "Aplikasi GUI desktop sederhana\n"
                         "dibuat dengan PySide6")

def main():
    """Fungsi utama aplikasi"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Template PySide6")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Developer")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()