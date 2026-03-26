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

TOKEN = os.getenv("8783984383:AAFzd6Gj41vOLlPJ5E4oofQZ5tmVAg1mQ5g")
CHAT_ID = os.getenv("1024073475")
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
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 30)
        
        # 1. Imtihonni tanlash: IC3 Digital Literacy GS6
        exam = wait.until(EC.presence_of_element_located((By.NAME, "exam_id")))
        Select(exam).select_by_visible_text("IC3 Digital Literacy GS6")
        time.sleep(2)
        
        # 2. Tilni tanlash: English
        lang = wait.until(EC.presence_of_element_located((By.NAME, "lang_id")))
        Select(lang).select_by_visible_text("English")
        time.sleep(2)
        
        # 3. Modulni tanlash: Level 1
        module = wait.until(EC.presence_of_element_located((By.NAME, "module_id")))
        Select(module).select_by_visible_text("Level 1")
        time.sleep(2)
        
        # 4. Joyni tanlash: Toshkent / Ташкент
        loc = wait.until(EC.presence_of_element_located((By.NAME, "location_id")))
        Select(loc).select_by_visible_text("Toshkent / Ташкент")
        
        # Kalendar yuklanishi uchun biroz ko'proq kutamiz
        print("Kalendar tekshirilmoqda...")
        time.sleep(7)
        
        # Aktiv sanalarni qidirish (v-btn klassi ichidagi disabled bo'lmagan sanalar)
        # Certiport kalendarida bo'sh kunlar odatda 'v-btn--disabled' bo'lmaydi
        available_days = driver.find_elements(By.XPATH, "//button[contains(@class, 'v-btn') and not(contains(@class, 'v-btn--disabled')) and .//div[@class='v-btn__content' and number()]]")
        
        # Bugungi yoki o'tib ketgan kunlarni hisobga olmaslik uchun qo'shimcha filtr
        real_slots = [d for d in available_days if d.is_enabled()]

        if len(real_slots) > 0:
            msg = "🔔 Certiport: Bo'sh joy topildi! Tezroq ro'yxatdan o'ting: " + URL
            send_msg(msg)
            print("Natija: Joy bor!")
        else:
            print("Natija: Bo'sh joy yo'q.")
            
    except Exception as e:
        print(f"Xatolik: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_check()
