import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GitHub Secrets orqali olinadi
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://certiport.uz/uz/register"

def send_msg(text):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": text})

def run_check():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # GitHub (Linux) uchun drayverni avtomatik sozlash
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 30)
        
        # 1. Imtihon: IC3 Digital Literacy GS6
        exam = wait.until(EC.presence_of_element_located((By.NAME, "exam_id")))
        Select(exam).select_by_visible_text("IC3 Digital Literacy GS6")
        time.sleep(2)
        
        # 2. Til: English
        lang = wait.until(EC.presence_of_element_located((By.NAME, "lang_id")))
        Select(lang).select_by_visible_text("English")
        time.sleep(2)
        
        # 3. Modul: Level 1
        module = wait.until(EC.presence_of_element_located((By.NAME, "module_id")))
        Select(module).select_by_visible_text("Level 1")
        time.sleep(2)
        
        # 4. Joy: Toshkent / Ташкент
        loc = wait.until(EC.presence_of_element_located((By.NAME, "location_id")))
        Select(loc).select_by_visible_text("Toshkent / Ташкент")
        
        # Kalendar yuklanishini kutish (Skrinshotdagi kalendar chiqishi uchun)
        time.sleep(8)
        
        # Bo'sh kunlarni qidirish (v-btn klassi ichidagi band bo'lmagan kunlar)
        # Qizil (band) kunlar odatda 'v-btn--disabled' bo'ladi
        available_days = driver.find_elements(By.XPATH, "//button[contains(@class, 'v-btn') and not(contains(@class, 'v-btn--disabled')) and .//div[@class='v-btn__content' and number()]]")
        
        if len(available_days) > 0:
            msg = "🔔 Certiport: BO'SH JOY TOPILDI! Tezroq ro'yxatdan o'ting: " + URL
            send_msg(msg)
            print("Natija: Bo'sh sana bor!")
        else:
            print("Natija: Hamma kunlar band.")
            
    except Exception as e:
        print(f"Xatolik: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_check()
