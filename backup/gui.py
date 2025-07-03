import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLineEdit, QTextEdit, 
                               QLabel, QFileDialog)
from PySide6.QtCore import QThread, Signal, Qt

# Add the script's directory to the path to ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mengimpor kelas scraper dari file tiktok.py
from tiktok import TikTokScraper

# --- Modern Dark Theme Stylesheet (QSS) ---
MODERN_DARK_THEME = """
    QWidget {
        background-color: #1E1E1E;
        color: #F2F2F2;
        font-family: 'Segoe UI', 'Roboto', 'Open Sans', sans-serif;
        font-size: 14px;
    }
    QMainWindow {
        border: 1px solid #34495E;
    }
    QLabel {
        font-size: 16px;
        font-weight: bold;
    }
    QLineEdit {
        background-color: #2C3E50;
        border: 1px solid #34495E;
        padding: 8px;
        border-radius: 4px;
        font-size: 14px;
    }
    QTextEdit {
        background-color: #2C3E50;
        border: 1px solid #34495E;
        padding: 8px;
        border-radius: 4px;
    }
    QPushButton {
        background-color: #3498DB;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #2980B9;
    }
    QPushButton:pressed {
        background-color: #2ECC71;
    }
    QPushButton:disabled {
        background-color: #7F8C8D;
        color: #BDC3C7;
    }
"""

class WorkerThread(QThread):
    """
    Worker thread generik untuk menjalankan fungsi di latar belakang.
    """
    finished = Signal(object) # Mengirimkan hasil dari fungsi target
    
    def __init__(self, target_func, *args, **kwargs):
        super().__init__()
        self.target_func = target_func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Menjalankan fungsi target dan mengirimkan hasilnya."""
        try:
            result = self.target_func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(e)


class TikTokScraperApp(QMainWindow):
    """
    Kelas utama untuk aplikasi GUI TikTok Scraper.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TikTok Profile Scraper")
        self.setGeometry(100, 100, 700, 500)
        
        self.scraper = TikTokScraper(progress_callback=self.update_log)
        self.worker_thread = None

        self.init_ui()
        self.setStyleSheet(MODERN_DARK_THEME)

    def init_ui(self):
        """Menginisialisasi komponen UI."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Input & Output Section ---
        self.url_input = QLineEdit("https://www.tiktok.com/@football_world_01_?_t=8pMSDghcYwN&_r=1")
        self.output_path_input = QLineEdit(os.path.join(os.getcwd(), "tiktok_video_links.txt"))
        
        browse_button = QPushButton("...")
        browse_button.setFixedWidth(40)
        browse_button.clicked.connect(self.browse_output_file)
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("URL Profil:"))
        input_layout.addWidget(self.url_input)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Simpan ke:"))
        output_layout.addWidget(self.output_path_input)
        output_layout.addWidget(browse_button)

        # --- Tombol Aksi ---
        self.action_buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("1. Buka Browser & Selesaikan CAPTCHA")
        self.start_button.clicked.connect(self.start_step1_open_browser)
        
        self.continue_button = QPushButton("2. Lanjutkan & Ekstrak Link")
        self.continue_button.clicked.connect(self.start_step2_scrape_links)
        self.continue_button.setDisabled(True)
        
        self.action_buttons_layout.addWidget(self.start_button)
        self.action_buttons_layout.addWidget(self.continue_button)

        # --- Log/Output Console ---
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        # --- Menambahkan widget ke layout utama ---
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(self.action_buttons_layout)
        main_layout.addWidget(QLabel("Log Proses:"))
        main_layout.addWidget(self.log_output)

    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Simpan File Link", "", "Text Files (*.txt)")
        if file_path:
            self.output_path_input.setText(file_path)

    def start_step1_open_browser(self):
        """Langkah 1: Membuka browser di thread terpisah."""
        profile_url = self.url_input.text()
        if not profile_url:
            self.update_log("URL Profil tidak boleh kosong.")
            return

        self.set_ui_for_running(True)
        self.log_output.clear()
        
        self.worker_thread = WorkerThread(self.scraper.open_browser_and_navigate, profile_url)
        self.worker_thread.finished.connect(self.on_browser_opened)
        self.worker_thread.start()

    def on_browser_opened(self, success):
        """Dipanggil setelah browser selesai dibuka."""
        if success:
            self.update_log("\nBrowser terbuka. Silakan selesaikan CAPTCHA di jendela browser, lalu klik tombol 'Lanjutkan'.")
            self.start_button.setDisabled(True)
            self.continue_button.setDisabled(False)
        else:
            self.update_log("\n[GAGAL] Gagal membuka browser. Periksa log di atas.")
            self.set_ui_for_running(False)

    def start_step2_scrape_links(self):
        """Langkah 2: Memulai proses scraping di thread terpisah."""
        self.continue_button.setDisabled(True)
        self.update_log("\nMelanjutkan proses scraping...")
        
        self.worker_thread = WorkerThread(self.scraper.scrape_links_after_captcha)
        self.worker_thread.finished.connect(self.on_scraping_finished)
        self.worker_thread.start()

    def on_scraping_finished(self, result):
        """Dipanggil ketika thread scraping selesai."""
        if isinstance(result, list):
            self.update_log(f"\nScraping selesai. Menulis {len(result)} link ke file...")
            try:
                output_file = self.output_path_input.text()
                with open(output_file, 'w', encoding='utf-8') as f:
                    for link in result:
                        f.write(f"{link}\n")
                self.update_log(f"[BERHASIL] File disimpan di: {output_file}")
            except Exception as e:
                self.update_log(f"[ERROR] Gagal menyimpan file: {e}")
        else: # Jika terjadi error
            self.update_log(f"[ERROR] Proses scraping gagal: {result}")
        
        self.scraper.close_browser()
        self.set_ui_for_running(False)

    def update_log(self, message):
        self.log_output.append(str(message))

    def set_ui_for_running(self, is_running):
        """Mengatur status UI (aktif/nonaktif) selama proses berjalan."""
        self.start_button.setDisabled(is_running)
        self.continue_button.setDisabled(True) # Selalu nonaktif di awal
        self.url_input.setDisabled(is_running)
        self.output_path_input.setDisabled(is_running)

    def closeEvent(self, event):
        """Memastikan browser ditutup saat aplikasi ditutup."""
        self.scraper.close_browser()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TikTokScraperApp()
    window.show()
    sys.exit(app.exec())