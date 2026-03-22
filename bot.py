import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(msg):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        except Exception as e:
            print(f"Telegram error: {e}")

def check():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Sayt ochilmoqda...")
        driver.get("https://certiport.uz/uz/register")
        wait = WebDriverWait(driver, 60)

        # Sahifa to'liq yuklanishi uchun biroz kutamiz
        time.sleep(10)

        print("Imtihon turi tanlanmoqda...")
        # Select elementini topishda CSS_SELECTOR o'rniga NAME ishlatamiz
        exam_id = wait.until(EC.presence_of_element_located((By.NAME, "exam_id")))
        Select(exam_id).select_by_visible_text("IC3 Digital Literacy GS6")
        
        time.sleep(3)
        print("Viloyat tanlanmoqda...")
        loc = driver.find_element(By.NAME, "location_id")
        Select(loc).select_by_visible_text("Toshkent / Ташкент")
        
        time.sleep(10)
        print("Kalendar tekshirilmoqda...")
        days = driver.find_elements(By.CLASS_NAME, "day")
        found = False
        for day in days:
            class_info = day.get_attribute("class")
            if "red" not in class_info and day.text.strip().isdigit():
                send_telegram(f"🔥 BO'SH JOY TOPILDI! \nSana: {day.text}\nRo'yxatdan o'tish: https://certiport.uz/uz/register")
                found = True
                break
        
        if not found:
            print("Hozircha bo'sh joy yo'q.")

    except Exception as e:
        print(f"Xatolik tafsiloti: {e}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    send_telegram("🤖 Tizim: Certiport tekshiruvi boshlandi!")
    check()
