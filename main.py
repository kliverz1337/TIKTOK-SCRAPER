import sys
import os

# --- Fix Import Path ---
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Konfigurasi Qt WebEngine ---
# Tetap gunakan flag dasar untuk praktik terbaik.
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu'

from PySide6.QtWidgets import QApplication
from ui.main_window import TikTokScraperApp

if __name__ == "__main__":
    # --- SOLUSI FINAL: Pengalihan File Descriptor ---
    # Metode sebelumnya gagal karena error dicetak oleh subproses Chromium
    # yang tidak menghormati flag atau sistem logging Qt/Python.
    # Solusi ini mengalihkan stderr di level OS, yang akan diwarisi
    # oleh semua subproses, secara efektif membungkam outputnya.
    
    original_stderr_fd = sys.stderr.fileno()
    saved_stderr_fd = os.dup(original_stderr_fd)
    
    try:
        # Alihkan stderr ke devnull
        devnull_fd = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull_fd, original_stderr_fd)
        os.close(devnull_fd)

        app = QApplication(sys.argv)
        window = TikTokScraperApp()
        window.show()
        sys.exit(app.exec())
        
    except Exception as e:
        # Jika terjadi crash, pulihkan stderr untuk menampilkan pesan error.
        os.dup2(saved_stderr_fd, original_stderr_fd)
        print(f"Aplikasi crash dengan error tak terduga: {e}", file=sys.stderr)
        
    finally:
        # Pastikan stderr dipulihkan saat aplikasi ditutup secara normal.
        os.dup2(saved_stderr_fd, original_stderr_fd)
        os.close(saved_stderr_fd)