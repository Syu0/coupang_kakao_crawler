from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import re
import random


def sleepTime():
    time.sleep(random.randint(1, 5))

collect_count = 5
url_coupang = "https://www.coupang.com/np/search?component=&q=%EB%84%A4%EC%9D%BC+%ED%8C%8C%EC%B8%A0&channel=user"
TODAY = datetime.today().strftime("%Y%m%d%H%M")
FILE_NAME = f'{TODAY}_coupang_store_collected'
CSV_PATH = f'C:/Users/user/Downloads/{FILE_NAME}.csv'
EXCEL_PATH =  f'C:/Users/user/Downloads/{FILE_NAME}.xlsx'

print(f'CSV PATH: {CSV_PATH}\n EXCEL_PATH: {EXCEL_PATH}')

options = ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--start-maximized')

driver = Chrome(options=options)

wait = WebDriverWait(driver, 120)
driver.get(url_coupang)
wait = WebDriverWait(driver, 120)
products = []
product_links = []
Cat_text = []
Title = []
Descp = []
Price = []
images_list = []


a_tags = driver.find_elements(
    By.CSS_SELECTOR, "ul#productList a.search-product-link")
urls = [a_tag.get_attribute("href") for a_tag in a_tags]
products.extend(urls)

time.sleep(5)
try:
    for url1 in products[:collect_count]:
        driver.get(url1)
        product_links.append(url1)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        cat_text = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul#breadcrumb li:nth-child(3)")))
        cat_text = cat_text.text.strip()
        Cat_text.append(cat_text)
        sleepTime()

        tit_detail_tag = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h2.prod-buy-header__title")))
        tit_detail_text = tit_detail_tag.text.strip()
        Title.append(tit_detail_text)
        sleepTime()

        desc_price_tag = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.total-price strong")))
        desc_price_text = desc_price_tag.text.strip()
        Price.append(desc_price_text)
        sleepTime()

        ul_tag = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'ul.prod-description-attribute')))
        li_tags = ul_tag.find_elements(By.CSS_SELECTOR, 'li.prod-attr-item')
        li_texts_str = ', '.join([li.text.strip() for li in li_tags])
        Descp.append(li_texts_str)
        sleepTime()

        items = driver.find_elements(By.CLASS_NAME, 'prod-image__item')
        # img_urls = [item.find_element(By.TAG_NAME, 'img').get_attribute('src') for item in items]
        img_urls = [item.find_element(By.TAG_NAME, 'img').get_attribute(
            'src').replace('48x48ex', '800x800ex') for item in items]
        img_urls_str = ', '.join(img_urls)
        images_list.append(img_urls_str)

    driver.quit()

    df = pd.DataFrame({
        'Product URL': product_links,
        'category': Cat_text,
        'Title': Title,
        'Price': Price,
        'Description Text': Descp,
        'Images': images_list,
    })

    df.to_excel(EXCEL_PATH, index=False)
    df.to_csv(CSV_PATH, index=False)
except:
    driver.quit()

    df = pd.DataFrame({
        'Product URL': product_links,
        'category': Cat_text,
        'Title': Title,
        'Price': Price,
        'Description Text': Descp,
        'Images': images_list,
    })

    df.to_excel(EXCEL_PATH, index=False)
    df.to_csv(CSV_PATH, index=False)

print("Coupang scraping done. File is saved.")
