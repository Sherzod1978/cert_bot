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

TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def check():
    chrome_options = Options()
    # Virtual serverlar uchun eng muhim sozlamalar
    chrome_options.add_argument("--headless=new") # Yangi headless rejim
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get("https://certiport.uz/uz/register")
        wait = WebDriverWait(driver, 30)

        # Sahifa yuklanishini va elementlar chiqishini kutamiz
        exam_field = wait.until(EC.presence_of_element_located((By.NAME, "exam_id")))
        exam_field.send_keys("IC3 Digital Literacy GS6")
        time.sleep(2)
        
        driver.find_element(By.NAME, "language").send_keys("English")
        time.sleep(2)
        
        driver.find_element(By.NAME, "module_id").send_keys("Level 1")
        time.sleep(2)
        
        driver.find_element(By.NAME, "location_id").send_keys("Toshkent / Ташкент")
        
        # Kalendar yuklanishi uchun uzunroq kutish
        time.sleep(15)

        days = driver.find_elements(By.CLASS_NAME, "day")
        found = False
        for day in days:
            class_name = day.get_attribute("class")
            if "red" not in class_name and day.text.isdigit():
                send_telegram(f"🔥 BO'SH JOY TOPILDI! Sana: {day.text}. Ro'yxatdan o'ting: https://certiport.uz/uz/register")
                found = True
                break
        
        if not found:
            print("Tekshirildi: Hozircha bo'sh joy yo'q.")
            
    except Exception as e:
        print(f"Xatolik: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check()
