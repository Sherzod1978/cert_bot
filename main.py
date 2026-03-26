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
        print("Sayt yuklanmoqda...")
        driver.get(URL)
        wait = WebDriverWait(driver, 20)
        
        print("1. Imtihon turi tanlanmoqda...")
        exam_el = wait.until(EC.presence_of_element_located((By.NAME, "exam_id")))
        # ... qolgan kodlar
        
        print("Tekshiruv yakunlandi, bo'sh joy topilmadi.") # Agar xato bo'lmasa shu chiqadi
   
        
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
    # send_msg("Bot tekshiruvni boshladi...") # Test uchun buni vaqtincha yoqing
    run_check()
