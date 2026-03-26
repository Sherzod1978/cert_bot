import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOKEN = os.getenv("8783984383:AAFzd6Gj41vOLlPJ5E4oofQZ5tmVAg1mQ5g")
CHAT_ID = os.getenv("1024073475")
URL = "https://certiport.uz/uz/register"

def send_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": text})

def run_check():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 30)
        
        # Elementni kutish va topish
        exam_select = wait.until(EC.presence_of_element_located((By.NAME, "exam_id")))
        
        # Tanlovlarni amalga oshirish
        Select(exam_select).select_by_visible_text("IC3 Digital Literacy GS6")
        time.sleep(2)
        
        # Toshkentni tanlash
        loc_select = Select(driver.find_element(By.NAME, "location_id"))
        loc_select.select_by_visible_text("Toshkent / Ташкент")
        time.sleep(5) # Kalendar yuklanishi uchun
        
        # Bo'sh kunlarni tekshirish (v-btn klassi orqali)
        available = driver.find_elements(By.CSS_SELECTOR, ".v-btn--active:not(.v-btn--disabled)")
        
        if len(available) > 0:
            send_msg("DIQQAT! Certiport.uz saytida bo'sh joy topildi!")
        else:
            print("Bo'sh joy yo'q.")
            
    except Exception as e:
        print(f"Xato: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_check()
