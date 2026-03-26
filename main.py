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
    options.add_argument("--headless=new") # Ekransiz rejim
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Drayverni sozlash
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        print("Sayt ochilmoqda...")
        driver.get(URL)
        wait = WebDriverWait(driver, 30)
        
        # Element yuklanishini kutish
        print("Imtihon turi tanlanmoqda...")
        exam_el = wait.until(EC.presence_of_element_located((By.NAME, "exam_id")))
        Select(exam_el).select_by_visible_text("IC3 Digital Literacy GS6")
        
        time.sleep(3) # Tanlovlar orasida kutish
        
        print("Joy tanlanmoqda...")
        loc_el = wait.until(EC.presence_of_element_located((By.NAME, "location_id")))
        Select(loc_el).select_by_visible_text("Toshkent / Ташкент")
        
        time.sleep(5) # Kalendar yuklanishi uchun
        
        # Aktiv sanalarni tekshirish
        available = driver.find_elements(By.CSS_SELECTOR, ".v-btn--active:not(.v-btn--disabled)")
        
        if len(available) > 0:
            send_msg("🔔 Certiport.uz saytida bo'sh joy topildi! Tezroq ro'yxatdan o'ting.")
            print("Natija: Bo'sh joy bor!")
        else:
            print("Natija: Hozircha bo'sh joy yo'q.")
            
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_check()
