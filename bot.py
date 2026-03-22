import os
import time
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# GitHub Secrets orqali ma'lumotlarni olish
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(msg):
    """Telegramga xabar yuborish funksiyasi"""
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
            print(f"Telegram status kodi: {res.status_code}")
        except Exception as e:
            print(f"Telegram xatosi: {e}")

def check():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Bot ekanligini yashirish uchun haqiqiy User-Agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = None
    try:
        print("Drayver yuklanmoqda...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print("Sayt ochilmoqda...")
        driver.get("https://certiport.uz/uz/register")
        
        # Element yuklanishini 30 soniya kutish
        wait = WebDriverWait(driver, 30)

        print("Ma'lumotlar kiritilmoqda...")
        # 1. Imtihon turi
        exam_id = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='exam_id']")))
        Select(exam_id).select_by_visible_text("IC3 Digital Literacy GS6")
        
        time.sleep(3) # Sahifa yangilanishi uchun qisqa tanaffus
        
        # 2. Til
        lang = driver.find_element(By.NAME, "language")
        Select(lang).select_by_visible_text("English")
        
        time.sleep(2)
        
        # 3. Modul
        module = driver.find_element(By.NAME, "module_id")
        Select(module).select_by_visible_text("Level 1")
        
        time.sleep(2)
        
        # 4. Joylashuv
        loc = driver.find_element(By.NAME, "location_id")
        Select(loc).select_by_visible_text("Toshkent / Ташкент")
        
        print("Kalendar tekshirilmoqda...")
        time.sleep(15) # Kalendar yuklanishi uchun uzoqroq kutish

        # Bo'sh kunlarni qidirish
        days = driver.find_elements(By.CLASS_NAME, "day")
        found = False
        for day in days:
            class_info = day.get_attribute("class")
            if "red" not in class_info and day.text.strip().isdigit():
                send_telegram(f"🔥 BO'SH JOY TOPILDI!\nSana: {day.text}\nRo'yxatdan o'tish: https://certiport.uz/uz/register")
                found = True
                break
        
        if not found:
            print("Hozircha bo'sh joy yo'q.")
            
    except Exception as e:
        error_info = f"❌ Botda xatolik: {str(e)[:100]}"
        print(error_info)
        send_telegram(error_info) # Xatoni Telegramga yuborish
        if driver:
            driver.save_screenshot("debug_error.png")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Test xabari yuborish
    send_telegram("🤖 Tizim: Certiport tekshiruvi boshlandi!")
    check()
