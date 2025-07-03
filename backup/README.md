# TikTok Profile Link Scraper

Proyek ini menggunakan Selenium untuk mengambil semua link video dari halaman profil TikTok tertentu dan menyimpannya ke dalam file teks.

## Fitur

-   Membuka halaman profil TikTok menggunakan Selenium.
-   Menggulir halaman secara otomatis untuk memuat semua video.
-   Mengekstrak semua link video individual.
-   Menyimpan link ke dalam file `tiktok_video_links.txt`.

## Persyaratan

-   Python 3.6+
-   Google Chrome terpasang di sistem Anda.

## Instalasi

1.  **Instal dependensi Python:**
    ```bash
    pip install selenium webdriver-manager beautifulsoup4
    ```

## Cara Penggunaan

1.  **Jalankan skrip:**
    ```bash
    python tiktok.py
    ```

2.  **Selesaikan reCAPTCHA:**
    -   Jendela Chrome akan terbuka. Skrip akan berhenti sejenak dan meminta Anda untuk menyelesaikan reCAPTCHA di halaman TikTok.
    -   Setelah Anda menyelesaikannya, kembali ke terminal dan tekan `Enter`.

3.  **Biarkan skrip berjalan:**
    -   Skrip sekarang akan secara otomatis menggulir halaman ke bawah untuk memuat semua video. Ini mungkin memakan waktu tergantung pada jumlah video di profil.

4.  **Periksa hasilnya:**
    -   Setelah selesai, Anda akan menemukan file bernama `tiktok_video_links.txt` di direktori yang sama, yang berisi semua URL video.

## Struktur File

-   `tiktok.py`: Skrip utama Python.
-   `tiktok_video_links.txt`: File output yang berisi link video.
-   `README.md`: File dokumentasi ini.
