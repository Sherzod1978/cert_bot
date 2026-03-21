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
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram xatolik: {e}")

def check():
    chrome_options = Options()
    # GitHub serverlari uchun zaruriy sozlamalar
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Avtomatik drayver o'rnatish
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get("https://certiport.uz/uz/register")
        wait = WebDriverWait(driver, 30)

        # Dropdown elementlarini tanlash
        wait.until(EC.presence_of_element_located((By.NAME, "exam_id"))).send_keys("IC3 Digital Literacy GS6")
        time.sleep(2)
        
        wait.until(EC.presence_of_element_located((By.NAME, "language"))).send_keys("English")
        time.sleep(2)
        
        wait.until(EC.presence_of_element_located((By.NAME, "module_id"))).send_keys("Level 1")
        time.sleep(2)
        
        wait.until(EC.presence_of_element_located((By.NAME, "location_id"))).send_keys("Toshkent / Ташкент")
        
        # Kalendar yuklanishi uchun biroz kutish
        time.sleep(10)

        # Bo'sh kunlarni (qizil bo'lmaganlarini) qidirish
        days = driver.find_elements(By.CLASS_NAME, "day")
        found_date = ""
        for day in days:
            class_info = day.get_attribute("class")
            if "red" not in class_info and day.text.isdigit():
                found_date = day.text
                break
        
        if found_date:
            send_telegram(f"🔥 BO'SH JOY TOPILDI! Sana: {found_date}. Ro'yxatdan o'ting: https://certiport.uz/uz/register")
        else:
            print("Hozircha bo'sh joy yo'q.")
            
    except Exception as e:
        print(f"Xatolik yuz berdi: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check()
