# TikTok Profile Scraper

Aplikasi desktop yang dirancang untuk mengotomatiskan proses ekstraksi seluruh tautan video dari profil pengguna TikTok tertentu. Data yang diekstraksi disimpan secara lokal dalam format `.txt` untuk analisis lebih lanjut.

## Galeri Aplikasi
| Tampilan Awal | Proses Scraping | Tampilan Hasil |
| :---: | :---: | :---: |
| ![Tampilan Awal Aplikasi](screenshot/screenshot_108.png) | ![Proses Scraping Sedang Berjalan](screenshot/screenshot_109.png) | ![Hasil Ekstraksi Ditampilkan](screenshot/screenshot_110.png) |

## Fitur Utama
- **Browser Tersemat:** Mengintegrasikan web engine untuk me-render halaman dan menangani elemen interaktif seperti CAPTCHA.
- **Scrolling Otomatis:** Secara cerdas melakukan scroll pada halaman profil untuk memuat konten video yang dinamis secara menyeluruh.
- **Ekstraksi Tautan:** Mem-parsing konten HTML final untuk mengidentifikasi dan mengumpulkan semua URL video yang unik.
- **Tampilan Hasil:** Menyajikan tautan yang diekstraksi dalam format tabel yang jelas di dalam aplikasi.
- **Penyimpanan Otomatis:** Menyimpan daftar tautan yang telah dikumpulkan ke dalam file `.txt` di dalam direktori `result/`.

## Prasyarat dan Instalasi
Untuk menjalankan aplikasi ini, pastikan lingkungan Anda memenuhi prasyarat berikut:

1.  **Python:** Python 3.6 atau versi yang lebih baru harus terinstal.
2.  **Kloning Repositori:**
    ```bash
    git clone https://github.com/kliverz1337/TIKTOK-SCRAPER.git
    cd repo
    ```
3.  **Instalasi Dependensi:**
    Instal semua pustaka yang diperlukan menggunakan pip:
    ```bash
    pip install PySide6 beautifulsoup4
    ```

## Panduan Penggunaan
1.  Jalankan aplikasi dari direktori utama proyek:
    ```bash
    python main.py
    ```
2.  Masukkan URL profil TikTok target pada kolom input yang tersedia.
3.  Klik tombol **Muat Halaman** untuk me-render profil di dalam browser tersemat.
4.  Setelah halaman dimuat sepenuhnya, klik **Mulai Ekstrak Link** untuk memulai proses scraping.
5.  Pantau kemajuan proses melalui panel log aplikasi.
6.  Setelah selesai, hasil akan ditampilkan pada tab "Hasil" dan juga disimpan secara otomatis di direktori `result/`.

## Tumpukan Teknologi (Technology Stack)
- **Python 3:** Bahasa pemrograman inti.
- **PySide6:** Binding Qt for Python yang digunakan untuk membangun antarmuka pengguna grafis (GUI).
- **Qt WebEngine:** Web engine berbasis Chromium untuk rendering halaman web.
- **BeautifulSoup4:** Pustaka untuk parsing dokumen HTML.