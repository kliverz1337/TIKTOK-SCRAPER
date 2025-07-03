import sys
import os
import time


from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLineEdit, QTextEdit,
                               QLabel, QFileDialog, QSplitter, QGroupBox,
                               QStatusBar, QStyle, QFrame, QProgressBar, QMessageBox,
                               QTabWidget, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import QThread, Signal, Qt, QUrl, QTimer, QPoint
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup
from ui.custom_dialog import CustomMessageBox
from constants import MODERN_DARK_THEME
from utils import simpan_hasil_scraping

class TikTokScraperApp(QMainWindow):
    """
    Aplikasi GUI TikTok Scraper dengan browser tersemat.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle("TikTok Scraper")
        self.resize(900, 650)
        self.setMinimumSize(700, 500)

        self.old_pos = None
        self.initial_load = True

        # --- Atribut untuk proses scraping ---
        self.last_height = 0
        self.stable_checks = 0
        self.scroll_timer = QTimer(self)
        self.scroll_timer.setInterval(3000)
        self.scroll_timer.timeout.connect(self.perform_scroll_check)
        
        self.init_ui()
        self.setStyleSheet(MODERN_DARK_THEME)
        self._center_window()
        self._show_initial_tutorial()

    def _show_initial_tutorial(self):
        """Menampilkan halaman HTML default dengan tutorial."""
        tutorial_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Selamat Datang</title>
            <style>
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                body {
                    background-color: #282a36;
                    color: #f8f8f2;
                    font-family: 'Segoe UI', 'Roboto', sans-serif;
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    overflow: hidden; /* Mencegah scrollbar */
                }
                .container {
                    background-color: #44475a;
                    border-radius: 15px;
                    padding: 25px 35px;
                    border: 1px solid #6272a4;
                    max-width: 90%;
                    text-align: left;
                    animation: fadeIn 0.5s ease-out;
                }
                h1 {
                    color: #50fa7b;
                    text-align: center;
                    font-size: 22px;
                    margin-top: 0;
                    margin-bottom: 10px;
                    border-bottom: 1px solid #6272a4;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #bd93f9;
                    font-size: 18px;
                    margin-top: 15px;
                    margin-bottom: 8px;
                }
                p, li {
                    font-size: 14px;
                    line-height: 1.5;
                }
                ol {
                    padding-left: 25px;
                    margin: 0;
                }
                li {
                    margin-bottom: 8px;
                }
                code {
                    background-color: #282a36;
                    padding: 2px 5px;
                    border-radius: 4px;
                    color: #ff79c6;
                    font-size: 13px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Selamat Datang di TikTok Scraper</h1>
                <p>Aplikasi ini membantu Anda mengekstrak semua link video dari profil TikTok.</p>
                
                <h2>Langkah-langkah Penggunaan:</h2>
                <ol>
                    <li><b>URL Profil:</b> Tempel URL profil TikTok di kolom yang tersedia.</li>
                    <li><b>Muat Halaman:</b> Klik tombol <b>Muat Halaman</b> untuk memuat profil di browser.</li>
                    <li><b>Mulai Ekstrak:</b> Setelah halaman dimuat, klik <b>Mulai Ekstrak Link</b>.</li>
                    <li><b>Selesai:</b> Link akan otomatis tersimpan di folder <code>result/</code>.</li>
                </ol>
            </div>
        </body>
        </html>
        """
        self.web_view.setHtml(tutorial_html)

    def init_ui(self):
        """Inisialisasi semua komponen UI dengan tampilan yang disempurnakan."""
        self.container = QFrame()
        self.container.setObjectName("container")
        self.setCentralWidget(self.container)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.title_bar = self._create_custom_title_bar()
        container_layout.addWidget(self.title_bar)

        # --- Layout Utama ---
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        container_layout.addWidget(main_widget)
        
        splitter = QSplitter(Qt.Horizontal)
        
        # --- Panel Kontrol (Kiri) ---
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(15)
        control_layout.setContentsMargins(10, 10, 10, 10)

        # --- Grup Input & Konfigurasi ---
        input_group = QGroupBox("Input & Konfigurasi")
        input_layout = QVBoxLayout(input_group)

        self.url_input = QLineEdit("https://www.tiktok.com/@kliverz")
        input_layout.addWidget(QLabel("URL Profil TikTok:"))
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(QLabel("Hasil akan disimpan di folder 'result' secara otomatis."))
        
        # --- Grup Kontrol & Log ---
        action_group = QGroupBox("Aksi & Log")
        action_layout = QVBoxLayout(action_group)

        self.load_button = QPushButton(" Muat Halaman")
        self.load_button.setObjectName("loadButton")
        self.load_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.load_button.clicked.connect(self.load_page)
        
        self.scrape_button = QPushButton(" Mulai Ekstrak Link")
        self.scrape_button.setObjectName("scrapeButton")
        self.scrape_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.scrape_button.clicked.connect(self.start_scraping)
        self.scrape_button.setDisabled(True)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.scrape_button)

        action_layout.addLayout(button_layout)
        action_layout.addWidget(QLabel("Log Proses:"))
        action_layout.addWidget(self.log_output)

        control_layout.addWidget(input_group)
        control_layout.addWidget(action_group)
        
        # --- Panel Kanan (Browser & Hasil) ---
        self.right_panel = QTabWidget()
        
        # --- Tab Browser ---
        self.web_view = QWebEngineView()
        self.profile = QWebEngineProfile()
        self.page = QWebEnginePage(self.profile, self.web_view)
        self.page.profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.web_view.setPage(self.page)
        self.web_view.page().loadFinished.connect(self.on_page_loaded)
        self.web_view.page().loadProgress.connect(self.update_status_progress)
        
        # --- Tab Hasil ---
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["No.", "Link Video"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.verticalHeader().setVisible(False) # Hide vertical header
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.right_panel.addTab(self.web_view, "Browser")
        self.right_panel.addTab(self.results_table, "Hasil")

        # --- Menggabungkan panel ---
        splitter.addWidget(control_panel)
        splitter.addWidget(self.right_panel)
        splitter.setSizes([450, 750]) # Atur ukuran awal
        
        main_layout.addWidget(splitter)

        # --- Progress Bar ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Aplikasi siap. Masukkan URL dan muat halaman.")
        container_layout.addWidget(self.progress_bar)

    def _center_window(self):
        """Mempusatkan jendela di layar."""
        frame_gm = self.frameGeometry()
        center_pt = self.screen().availableGeometry().center()
        frame_gm.moveCenter(center_pt)
        self.move(frame_gm.topLeft())

    def _create_custom_title_bar(self):
        title_bar = QWidget()
        title_bar.setObjectName("title_bar")
        title_bar.setFixedHeight(45)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(15, 0, 5, 0)

        title = QLabel(self.windowTitle())
        title.setStyleSheet("font-weight: bold; font-size: 16px; background: transparent;")
        title_bar_layout.addWidget(title)

        title_bar_layout.addStretch()

        btn_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5D6D7E;
            }
        """
        self.minimize_button = QPushButton("—")
        self.maximize_button = QPushButton("□")
        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("close_button")
        
        self.close_button.setStyleSheet(btn_style + "QWidget#title_bar QPushButton#close_button:hover { background-color: #ff5555; }")

        for btn in [self.minimize_button, self.maximize_button]:
            btn.setStyleSheet(btn_style)

        for btn in [self.minimize_button, self.maximize_button, self.close_button]:
            btn.setFixedSize(40, 40)

        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.close_button.clicked.connect(self.close)

        title_bar_layout.addWidget(self.minimize_button)
        title_bar_layout.addWidget(self.maximize_button)
        title_bar_layout.addWidget(self.close_button)

        return title_bar

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_button.setText("□")
        else:
            self.showMaximized()
            self.maximize_button.setText("❐")

    def mousePressEvent(self, event):
        if self.title_bar.underMouse() and event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def closeEvent(self, event):
        """Menampilkan dialog konfirmasi kustom sebelum menutup aplikasi."""
        dlg = CustomMessageBox(self, "Konfirmasi Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?")
        if dlg.exec():
            event.accept()
        else:
            event.ignore()

    def load_page(self):
        """Memuat URL ke dalam web view."""
        url = self.url_input.text()
        if url:
            self.right_panel.setCurrentWidget(self.web_view)
            self.web_view.setHtml("") # Hapus tutorial
            self.log_output.clear()
            self.update_log(f"Memuat halaman: {url}...", "ACTION")
            self.update_status("Memuat... %p%", 0)
            self.update_log("Silakan selesaikan CAPTCHA jika muncul di panel browser.", "INFO")
            self.web_view.setUrl(QUrl(url))
            self.load_button.setDisabled(True)

    def on_page_loaded(self, success):
        """Dipanggil saat halaman selesai dimuat di web view."""
        if self.initial_load:
            self.initial_load = False
            self.update_status("Aplikasi siap digunakan.", 0)
            self.load_button.setDisabled(False)
            return

        self.load_button.setDisabled(False)
        if success:
            self.update_log("Halaman berhasil dimuat. Anda sekarang bisa memulai ekstraksi.", "SUCCESS")
            self.update_status("Halaman dimuat. %p%", 100)
            self.scrape_button.setDisabled(False)
        else:
            self.update_log("Gagal memuat halaman.", "ERROR")
            self.update_status("Gagal memuat. %p%", 0)

    def start_scraping(self):
        """Memulai proses scraping non-blocking langsung dari main thread."""
        self.scrape_button.setDisabled(True)
        self.load_button.setDisabled(True)
        
        self.update_log("Memulai scroll halaman...", "ACTION")
        self.update_status("Scroll... %p%", 0)
        self.last_height = 0
        self.stable_checks = 0
        self.scroll_timer.start()

    def perform_scroll_check(self):
        """Mengecek tinggi halaman dan melakukan scroll."""
        self.web_view.page().runJavaScript("document.body.scrollHeight", self.on_height_received)

    def on_height_received(self, current_height):
        """Callback yang dipanggil setelah mendapatkan tinggi halaman."""
        if current_height == self.last_height and current_height > 0:
            self.stable_checks += 1
            progress = int((self.stable_checks / 3) * 100)
            self.update_log(f"Tinggi halaman stabil ({self.stable_checks}/3)...", "INFO")
            self.update_status("Scroll... %p%", progress)
            if self.stable_checks >= 3:
                self.update_log("Telah mencapai bagian bawah halaman.", "SUCCESS")
                self.update_status("Scroll selesai. %p%", 100)
                self.scroll_timer.stop()
                self.get_final_html()
        else:
            self.stable_checks = 0
            self.last_height = current_height
            self.update_log(f"Scroll ke tinggi: {current_height}...", "INFO")
            # Reset progress bar during scroll
            self.update_status("Scroll... %p%", 0)
            self.web_view.page().runJavaScript("window.scrollTo(0, document.body.scrollHeight);")

    def get_final_html(self):
        """Mengambil HTML akhir dan memulai parsing."""
        self.update_log("Mengambil konten HTML final...", "ACTION")
        self.update_status("Mengambil HTML... %p%", 0)
        self.web_view.page().toHtml(self.on_html_received)

    def on_html_received(self, html):
        """Callback yang dipanggil saat HTML diterima dari web view."""
        if not html:
            self.on_scraping_finished("Gagal mengambil konten HTML dari halaman.")
            return
        
        self.update_log("Parsing konten HTML...", "ACTION")
        self.update_status("Parsing... %p%", 50)
        soup = BeautifulSoup(html, "html.parser")
        
        video_tags = soup.select('a[href*="/video/"]')
        self.update_log(f"Menemukan {len(video_tags)} tag video potensial. Memproses...", "INFO")
        
        if not video_tags:
            self.on_scraping_finished("Tidak ada video yang ditemukan. Pastikan URL profil benar dan publik.")
            return

        base_url = "https://www.tiktok.com"
        links = {base_url + tag['href'] if tag['href'].startswith('/') and '/video/' in tag['href'] else tag['href']
                 for tag in video_tags if tag.has_attr('href') and '/video/' in tag['href']}
        
        self.on_scraping_finished(sorted(list(links)))

    def _get_profile_name_from_url(self, url):
        """Mengekstrak nama profil dari URL TikTok."""
        try:
            # Membersihkan URL dari parameter query
            clean_url = url.split('?')[0]
            # Menemukan bagian setelah '@' dan sebelum '/' berikutnya
            profile_part = clean_url.split('@')[1]
            if '/' in profile_part:
                profile_name = profile_part.split('/')[0]
            else:
                profile_name = profile_part
            return profile_name.strip()
        except IndexError:
            # Jika URL tidak valid, gunakan timestamp sebagai fallback
            self.update_log("URL tidak valid, nama file fallback digunakan.", "ERROR")
            return f"profil_{int(time.time())}"

    def on_scraping_finished(self, result):
        """Dipanggil saat proses scraping selesai."""
        if isinstance(result, list):
            self.update_log(f"Ekstraksi selesai. Menampilkan {len(result)} link unik...", "SUCCESS")
            
            # Populate table
            self.results_table.setRowCount(0)
            for i, link in enumerate(result):
                self.results_table.insertRow(i)
                self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.results_table.setItem(i, 1, QTableWidgetItem(link))
            
            self.right_panel.setCurrentWidget(self.results_table)
            
            self.update_log("Menyimpan hasil ke file...", "ACTION")
            self.update_status("Menyimpan hasil... %p%", 50)
            
            profile_url = self.url_input.text()
            profile_name = self._get_profile_name_from_url(profile_url)
            
            # Menggunakan fungsi utilitas baru untuk menyimpan hasil
            simpan_hasil_scraping(profile_name, result)
            
            self.update_log(f"Hasil untuk '{profile_name}' berhasil disimpan.", "SUCCESS")
            self.update_status("Selesai. %p%", 100)
        else:
            self.update_log(f"Proses gagal: {result}", "ERROR")
            self.update_status("Proses gagal. %p%", 0)
        
        self.scrape_button.setDisabled(False)
        self.load_button.setDisabled(False)
        self.update_status("Siap untuk tugas berikutnya.", 0)

    def update_status(self, message, value=None):
        """Memperbarui format teks dan nilai progress bar."""
        self.progress_bar.setFormat(message)
        if value is not None:
            self.progress_bar.setValue(value)
        QApplication.processEvents()

    def update_status_progress(self, progress):
        """Slot untuk sinyal loadProgress untuk memperbarui status."""
        self.update_status("Memuat halaman... %p%", progress)

    def update_log(self, message, level="INFO"):
        """Menambahkan pesan ke log dengan warna."""
        color_map = {
            "INFO": "#8be9fd",    # Cyan
            "SUCCESS": "#50fa7b", # Green
            "ERROR": "#ff5555",   # Red
            "ACTION": "#f1fa8c"   # Yellow
        }
        color = color_map.get(level, "#f8f8f2")
        self.log_output.append(f'<font color="{color}">{message}</font>')