import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

URL = "https://www.obilet.com/seferler/409-678/2026-03-13"
DATA_FILE = "firmalar.json"


def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text}
    )


def get_firmalar():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)
    time.sleep(8)

    firmalar = set()

    elements = driver.find_elements(By.CSS_SELECTOR, "div.partner-name")

    for el in elements:
        name = el.text.strip()
        if name:
            firmalar.add(name)

    driver.quit()
    return firmalar


def load_old_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(list(data), f)


def main():
    eski_firmalar = load_old_data()
    yeni_firmalar = get_firmalar()

    fark = yeni_firmalar - eski_firmalar

    if fark:
        for firma in fark:
            send_message(f"🆕 Yeni firma bulundu: {firma}")

    save_data(yeni_firmalar)


if __name__ == "__main__":
    main()
