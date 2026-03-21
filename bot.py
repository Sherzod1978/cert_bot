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
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check():
    chrome_options = Options()
    # Virtual serverlar uchun zaruriy sozlamalar
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Drayverni o'rnatish
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("Sayt tekshirilmoqda...")
        driver.get("https://certiport.uz/uz/register")
        wait = WebDriverWait(driver, 30)

        # Dropdown'larni tanlash
        wait.until(EC.presence_of_element_located((By.NAME, "exam_id"))).send_keys("IC3 Digital Literacy GS6")
        time.sleep(2)
        driver.find_element(By.NAME, "language").send_keys("English")
        time.sleep(2)
        driver.find_element(By.NAME, "module_id").send_keys("Level 1")
        time.sleep(2)
        driver.find_element(By.NAME, "location_id").send_keys("Toshkent / Ташкент")
        
        # Kalendar yuklanishini kutish
        time.sleep(15)

        days = driver.find_elements(By.CLASS_NAME, "day")
        found = False
        for day in days:
            class_info = day.get_attribute("class")
            if "red" not in class_info and day.text.isdigit():
                send_telegram(f"🔥 BO'SH JOY! Sana: {day.text}. Ro'yxatdan o'ting: https://certiport.uz/uz/register")
                found = True
                print(f"Topildi: {day.text}")
                break
        
        if not found:
            print("Tekshirildi: Hozircha bo'sh joy yo'q.")
            
    except Exception as e:
        print(f"Xatolik: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    check()
