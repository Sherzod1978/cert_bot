import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ.get("8783984383:AAFzd6Gj41vOLlPJ5E4oofQZ5tmVAg1mQ5g")
CHAT_ID = os.environ.get("1024073475")


def send_telegram(msg):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def check():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        print("Sayt ochilmoqda...")
        page.goto("https://certiport.uz/uz/register")

        page.wait_for_timeout(8000)

        print("Imtihon tanlanmoqda...")
        page.select_option('select[name="exam_id"]', label="IC3 Digital Literacy GS6")

        print("Viloyat tanlanmoqda...")
        page.select_option('select[name="location_id"]', label="Toshkent / Ташкент")

        page.wait_for_timeout(5000)

        print("Kalendar tekshirilmoqda...")

        days = page.query_selector_all(".day")

        found = False

        for day in days:

            text = day.inner_text().strip()
            class_name = day.get_attribute("class")

            if text.isdigit() and "red" not in class_name:

                send_telegram(
                    f"🔥 BO'SH JOY TOPILDI!\n\nSana: {text}\nhttps://certiport.uz/uz/register"
                )

                found = True
                break

        if not found:
            print("Hozircha bo'sh joy yo'q.")

        browser.close()


if __name__ == "__main__":

    send_telegram("🤖 Certiport monitoring ishga tushdi")

    check()
