import os
import time
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# GitHub Secrets'dan ma'lumotlarni olish
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(msg):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        except Exception as e:
            print(f"Telegram yuborishda xato: {e}")

def check():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = None
    try:
        print("Drayver yuklanmoqda...")
        # GitHub Actions muhitida drayverni avtomatik topish uchun
        driver = webdriver.Chrome(options=chrome_options)
        
        print("Sayt ochilmoqda...")
        driver.get("https://certiport.uz/uz/register")
        wait = WebDriverWait(driver, 20)

        print("Ma'lumotlar kiritilmoqda...")
        # Select klassidan foydalanish (bu xatolarni oldini oladi)
        exam_id = wait.until(EC.presence_of_element_located((By.NAME, "exam_id")))
        Select(exam_id).select_by_visible_text("IC3 Digital Literacy GS6")
        
        time.sleep(1) # Sayt dropdowndagi qiymatni qayta yuklashi uchun qisqa kutish
        
        lang = driver.find_element(By.NAME, "language")
        Select(lang).select_by_visible_text("English")
        
        time.sleep(1)
        
        module = driver.find_element(By.NAME, "module_id")
        Select(module).select_by_visible_text("Level 1")
        
        time.sleep(1)
        
        loc = driver.find_element(By.NAME, "location_id")
        Select(loc).select_by_visible_text("Toshkent / Ташкент")
        
        print("Kalendar tekshirilmoqda...")
        time.sleep(10) # Kalendar yuklanishini kutish

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
        # Xatolikni to'liq Telegramga yuborish (shunda skrinshotga qarab o'tirmaysiz)
        error_details = traceback.format_exc()
        print(f"Xatolik yuz berdi:\n{error_details}")
        # send_telegram(f"❌ Botda xatolik:\n{error_details[:200]}") # Ixtiyoriy: xatoni botga yuborish
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    send_telegram("🤖 Tizim: Ishni boshladim!")
    check()
