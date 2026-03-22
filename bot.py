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
    # Bot ekanligimizni yashirish uchun qo'shimcha sozlamalar
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    # Brauzerga bot emasligimizni ko'rsatuvchi script
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        print("Sayt ochilmoqda...")
        driver.get("https://certiport.uz/uz/register")
        wait = WebDriverWait(driver, 60) # Kutish vaqtini 60 soniyaga oshirdik

        # Sahifa to'liq yuklanishi uchun biroz kutamiz
        time.sleep(10)

        print("Imtihon turi tanlanmoqda...")
        # Elementni qidirish usulini o'zgartirdik (ID bo'yicha)
        exam_select = wait.until(EC.presence_of_element_located((By.ID, "exam_id")))
        Select(exam_select).select_by_visible_value("2") # IC3 GS6 qiymati odatda 2 bo'ladi
        
        time.sleep(3)
        print("Viloyat tanlanmoqda...")
        loc_select = driver.find_element(By.ID, "location_id")
        Select(loc_select).select_by_visible_text("Toshkent / Ташкент")

        time.sleep(5)
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
            print("Bo'sh joylar topilmadi.")

    except Exception as e:
        error_brief = str(e).split('\n')[0]
        print(f"Xatolik: {error_brief}")
        # Faqat jiddiy xatolarni yuboramiz
        if "TimeoutException" in str(e):
             send_telegram("⚠️ Kalendar yuklanishida muammo (Timeout). Sayt GitHub serverlarini cheklayotgan bo'lishi mumkin.")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    check()
