import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = os.environ.get("8783984383:AAFzd6Gj41vOLlPJ5E4oofQZ5tmVAg1mQ5g")
CHAT_ID = os.environ.get("1024073475")


def send_telegram(msg):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def check():

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:

        print("Sayt ochilmoqda...")
        driver.get("https://certiport.uz/uz/register")

        wait = WebDriverWait(driver, 60)

        print("Imtihon tanlanmoqda...")
        exam = wait.until(
            EC.element_to_be_clickable((By.NAME, "exam_id"))
        )

        Select(exam).select_by_visible_text("IC3 Digital Literacy GS6")

        time.sleep(2)

        print("Viloyat tanlanmoqda...")
        loc = wait.until(
            EC.element_to_be_clickable((By.NAME, "location_id"))
        )

        Select(loc).select_by_visible_text("Toshkent / Ташкент")

        time.sleep(5)

        print("Kalendar tekshirilmoqda...")
        days = driver.find_elements(By.CLASS_NAME, "day")

        found = False

        for day in days:

            class_name = day.get_attribute("class")

            if "red" not in class_name and day.text.strip().isdigit():

                send_telegram(
                    f"🔥 BO'SH JOY TOPILDI!\n\nSana: {day.text}\nhttps://certiport.uz/uz/register"
                )

                found = True
                break

        if not found:
            print("Bo'sh joy yo'q")

    except Exception as e:

        print("Xatolik:", e)
        driver.save_screenshot("error.png")

    finally:
        driver.quit()


if __name__ == "__main__":

    send_telegram("🤖 Certiport tekshiruv boshlandi")

    check()
