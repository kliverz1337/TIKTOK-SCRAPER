from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_youtube_trending():
    """
    Fetches trending YouTube videos and saves them to an HTML file.
    """
    url = "https://www.youtube.com/feed/trending"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver initialized successfully.")
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return

    try:
        driver.get(url)
        print(f"Navigated to {url}")
        
        # Wait for the page to load
        time.sleep(5)

        video_elements = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
        
        found_urls = set()
        if not video_elements:
            print("No video elements found.")
        else:
            print(f"Found {len(video_elements)} potential video elements.")
            for element in video_elements:
                href = element.get_attribute("href")
                if href:
                    found_urls.add(href)

        html_content = ""
        if found_urls:
            html_content += "<h1>YouTube Trending Videos</h1>\n"
            html_content += "<ul>\n"
            for video_url in sorted(list(found_urls)):
                html_content += f"<li><a href='{video_url}'>{video_url}</a></li>\n"
            html_content += "</ul>\n"
        else:
            html_content += "<h1>No YouTube Trending Videos Found</h1>\n"

        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Output saved to output.html")

    except Exception as e:
        print(f"An error occurred during Selenium operations: {e}")
    finally:
        if 'driver' in locals() and driver:
            driver.quit()
            print("WebDriver closed.")

if __name__ == "__main__":
    get_youtube_trending()
