import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GitHub Secrets'dan ma'lumotlarni olish
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=payload)

def check():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://certiport.uz/uz/register")
        wait = WebDriverWait(driver, 20)

        # Dropdown'larni tanlash
        wait.until(EC.element_to_be_clickable((By.NAME, "exam_id"))).send_keys("IC3 Digital Literacy GS6")
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.NAME, "language"))).send_keys("English")
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.NAME, "module_id"))).send_keys("Level 1")
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.NAME, "location_id"))).send_keys("Toshkent / Ташкент")
        time.sleep(5)

        # Kalendarni tekshirish
        days = driver.find_elements(By.CLASS_NAME, "day")
        found = False
        for day in days:
            class_info = day.get_attribute("class")
            if "red" not in class_info and day.text.isdigit():
                send_telegram(f"🔥 BO'SH JOY! {day.text}-sana ochiq! Ro'yxatdan o'ting: https://certiport.uz/uz/register")
                found = True
                break
        
        if not found:
            print("Hozircha bo'sh joy yo'q.")
            
    except Exception as e:
        print(f"Xatolik: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check()
