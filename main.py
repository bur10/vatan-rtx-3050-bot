# add-to-cart-button
import time
import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

load_dotenv()

CARDHOLDER = os.environ.get("CARDHOLDER")
CARD_NO = os.environ.get("CARD_NO")
EXP_DATE = os.environ.get("EXP_DATE")
CVV2 = os.environ.get("CVV2")

print("hello")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
BOT_MAIL = os.environ.get("BOT_MAIL")
BOT_MAIL_PASSWORD = os.environ.get("BOT_MAIL_PASSWORD")


link1 = "https://www.vatanbilgisayar.com/msi-geforce-rtx-3050-aero-itx-8gb-gddr6-128bit-nvidia-ekran-karti.html"
link2 = "https://www.vatanbilgisayar.com/msi-geforce-rtx-3050-ventus-2x-8gb-gddr6-128-bit-nvidia-ekran-karti.html"
# https://www.vatanbilgisayar.com/msi-geforce-rtx-3050-ventus-2x-8gb-gddr6-128-bit-nvidia-ekran-karti.html
# https://www.vatanbilgisayar.com/mikado-md-bt54-siyah-desenli-bluetooth-usb-aux-tf-card-tasinabilir-speaker.html test
# link3 = "https://www.vatanbilgisayar.com/msi-geforce-gt1030-2ghd4-lp-oc-2gb-gddr5-64bit-nvidia-dx12-ekran-karti.html" test

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options)


def check_stock():

    is_check_finished = False
    links = [link1, link2]

    while not is_check_finished:
        driver.get(links[0])
        try:
            add_to_cart_button = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//button[@id='add-to-cart-button']")))
        except:
            print(f"stok yok {links[0]} diger url deneniyor")
            if links[0] == link1:
                # fonksiyon yap
                links.pop(links.index(link1))
                if link2 not in links:
                    links.append(link2)
            elif links[0] == link2:
                links.pop(links.index(link2))
                if link1 not in links:
                    links.append(link1)
        else:
            print("stokta var")
            print(f"{EMAIL} adresine email gönderiliyor...")
            with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as server:
                msg = EmailMessage()
                msg.set_content(
                    f"Bitmeden önce acele etsen iyi olur. 🙄🙄\nStokta Olan Ürünün Linki: {links[0]}")
                msg["Subject"] = "Vatan RTX 3050 Şu Anda Stokta 🎉🎉"
                msg["From"] = BOT_MAIL
                msg["To"] = EMAIL
                msg['Message-ID'] = make_msgid()

                server.login(BOT_MAIL, BOT_MAIL_PASSWORD)
                server.send_message(msg)

            # satın alma işlemleri

            # add to basket
            add_to_cart_button.click()
            time.sleep(1)
            # go to basket
            driver.get("https://www.vatanbilgisayar.com/sepet/sepetim/")
            wait = WebDriverWait(driver, 5)

            # basket
            wait.until(EC.presence_of_element_located((
                By.XPATH, "//button[contains(@class, 'basket-ordersummary__button')]"))).click()
            try:
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "(//span[position()=1 and @class='basket-address__cargos-action']//span)")))
            except:
                pass
            else:
                # delivery
                wait.until(EC.presence_of_element_located((
                    By.XPATH, "//button[contains(@class, 'basket-ordersummary__button')]"))).click()
                # checkout
                # card info
                driver.find_element(By.ID, "cardnumber").send_keys(CARD_NO)
                driver.find_element(By.ID, "cardholder").send_keys(CARDHOLDER)
                Select(driver.find_element(
                    By.ID, "cardexpiredatemonth")).select_by_value(EXP_DATE[0:2])
                Select(driver.find_element(
                    By.ID, "cardexpiredateyear")).select_by_value(EXP_DATE[3:5])
                driver.find_element(By.ID, "cardcvv2").send_keys(CVV2)
                # installment
                time.sleep(2)
                driver.find_elements(
                    By.XPATH, "//table[@class='table']//span")[-1].click()
                driver.find_element(
                    By.XPATH, "//label[@class='wrapper-checkbox color-blue']//span").click()
                print(driver.current_url)
                # submitPayment
                driver.find_element(By.ID, "submitPayment").click()

                wait.until(EC.presence_of_element_located((By.ID, "code"))).send_keys(
                    input("dogrulama kodunu girin: "))
                driver.find_element(By.ID, "btn-commit").click()

            is_check_finished = True


driver.get("https://www.vatanbilgisayar.com/login")

email_input = driver.find_element(By.ID, "email")
email_input.send_keys(EMAIL)

password_input = driver.find_element(By.ID, "pass")
password_input.send_keys(PASSWORD)

# login button
driver.find_element(By.ID, "login-button").click()
time.sleep(1)


check_stock()
