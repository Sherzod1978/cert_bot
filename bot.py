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
    """Telegramga xabar yuborish funksiyasi"""
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        except Exception as e:
            print(f"Telegram yuborishda xato: {e}")

def check():
    chrome_options = Options()
    # GitHub Actions va blokirovkadan qochish uchun sozlamalar
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Bot ekanligini yashirish uchun qo'shimcha argumentlar
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = None
    try:
        print("Drayver yuklanmoqda...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Brauzerga "bot emasman" degan buyruqni yuborish
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
            """
        })

        print("Sayt ochilmoqda...")
        driver.get("https://certiport.uz/uz/register")
        
        # Barcha iframe'lardan chiqib, asosiy sahifaga fokuslanish
        driver.switch_to.default_content()
        
        # Kutish vaqtini 30 soniyaga oshirdik
        wait = WebDriverWait(driver, 30)

        print("Ma'lumotlar kiritilmoqda...")
        
        # 1. Imtihon turini tanlash (CSS Selector orqali)
        exam_id = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='exam_id']")))
        Select(exam_id).select_by_visible_text("IC3 Digital Literacy GS6")
        time.sleep(2) # Formaning dinamik yangilanishi uchun
        
        # 2. Tilni tanlash
        lang_el = driver.find_element(By.NAME, "language")
        Select(lang_el).select_by_visible_text("English")
        time.sleep(2)
        
        # 3. Modulni tanlash
        mod_el = driver.find_element(By.NAME, "module_id")
        Select(mod_el).select_by_visible_text("Level 1")
        time.sleep(2)
        
        # 4. Joylashuvni tanlash
        loc_el = driver.find_element(By.NAME, "location_id")
        Select(loc_el).select_by_visible_text("Toshkent / Ташкент")
        
        print("Kalendar yuklanishini kutmoqdaman...")
        time.sleep(12) # Kalendar elementlari paydo bo'lishi uchun

        # Kalendar kunlarini tekshirish
        days = driver.find_elements(By.CLASS_NAME, "day")
        found = False
        for day in days:
            class_info = day.get_attribute("class")
            # 'red' bo'lmagan va raqamli kunlarni qidirish
            if "red" not in class_info and day.text.strip().isdigit():
                msg = f"🔥 BO'SH JOY TOPILDI!\nSana: {day.text}\nRo'yxatdan o'tish: https://certiport.uz/uz/register"
                send_telegram(msg)
                found = True
                print(f"Topildi: {day.text}")
                break
        
        if not found:
            print("Tekshirildi: Hozircha bo'sh joy yo'q.")
            
    except Exception as e:
        print("Xatolik yuz berdi. Skrinshot saqlanmoqda...")
        if driver:
            driver.save_screenshot("debug_error.png")
        
        error_msg = traceback.format_exc()
        print(f"Xatolik tafsiloti:\n{error_msg}")
        # Ixtiyoriy: Xatoni telegramga qisqacha yuborish
        # send_telegram(f"❌ Xatolik yuz berdi: {str(e)[:100]}")
        
    finally:
        if driver:
            driver.quit()
            print("Brauzer yopildi.")

if __name__ == "__main__":
    # Har safar ishga tushganda 1 marta xabar beradi
    send_telegram("🤖 Tizim: Kunlik tekshirish boshlandi. Ishni boshladim!")
    check()
