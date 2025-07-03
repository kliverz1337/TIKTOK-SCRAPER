import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class TikTokScraper:
    """
    Sebuah kelas untuk membungkus logika scraping TikTok, 
    membuatnya dapat dikontrol oleh aplikasi eksternal seperti GUI.
    """
    def __init__(self, progress_callback=print):
        self.driver = None
        self.progress_callback = progress_callback

    def open_browser_and_navigate(self, url):
        """Membuka browser Chrome dan menavigasi ke URL yang diberikan."""
        try:
            self.progress_callback("Membuka browser Chrome...")
            options = webdriver.ChromeOptions()
            options.add_argument('--log-level=3')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            self.progress_callback(f"Menavigasi ke: {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            self.progress_callback(f"[ERROR] Gagal membuka browser: {e}")
            return False

    def scrape_links_after_captcha(self):
        """
        Menggulir halaman dan mengekstrak link setelah CAPTCHA diselesaikan secara manual.
        Mengembalikan daftar link video.
        """
        if not self.driver:
            self.progress_callback("[ERROR] Driver tidak diinisialisasi.")
            return []

        try:
            self.progress_callback("Menggulir halaman untuk memuat semua video...")
            self._scroll_page()

            self.progress_callback("Mengekstrak semua link video...")
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            video_tags = soup.find_all("div", {"class": "css-1uqux2o-DivItemContainerV2"})

            if not video_tags:
                self.progress_callback("[PERINGATAN] Tidak ada video yang ditemukan.")
                return []

            # Menggunakan set untuk secara otomatis menangani duplikat
            video_links = set()
            for tag in video_tags:
                if tag.a and tag.a.has_attr('href'):
                    video_links.add(tag.a['href'])
            
            self.progress_callback(f"Ditemukan {len(video_links)} link unik.")
            return list(video_links) # Mengembalikan sebagai list
        except Exception as e:
            self.progress_callback(f"[ERROR] Gagal melakukan scraping: {e}")
            return []

    def _scroll_page(self):
        """Metode internal untuk menggulir halaman."""
        scroll_pause_time = 1.5
        screen_height = self.driver.execute_script("return window.screen.height;")
        i = 1
        while True:
            self.driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
            if (screen_height * i) > scroll_height:
                self.progress_callback("Telah mencapai bagian bawah halaman.")
                break
    
    def close_browser(self):
        """Menutup browser Selenium jika sedang berjalan."""
        if self.driver:
            self.progress_callback("Menutup browser.")
            self.driver.quit()
            self.driver = None

# Blok di bawah ini hanya untuk pengujian mandiri, tidak digunakan oleh GUI.
if __name__ == '__main__':
    scraper = TikTokScraper()
    scraper.open_browser_and_navigate("https://www.tiktok.com/@football_world_01_?_t=8pMSDghcYwN&_r=1")
    input("Selesaikan CAPTCHA di browser, lalu tekan Enter di sini...")
    links = scraper.scrape_links_after_captcha()
    if links:
        print("\n--- Link yang Ditemukan ---")
        for link in links:
            print(link)
    scraper.close_browser()