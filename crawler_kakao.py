# 2024.02.17 a_tag 지정 오류 수정 line:90
# 2024.02.18 저장되는 경로 변경
# 2024.02.19 to_excel 에서 to_csv로 변경
# 저장경로 지정변수 추가 CSV_PATH

from datetime import datetime
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import random

KAKAO_URL = "https://store.kakao.com/kakaofriends/search/products?q=%EB%84%A5%EC%BF%A8%EB%9F%AC"
TODAY = datetime.today().strftime("%Y%m%d%H%M")
CSV_PATH = f'C:/Users/user/Downloads/{TODAY}_kakao_store_data.csv'


def scrape_kakao_store(url):

    options = ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')

    driver = Chrome(options=options)
    # wait = WebDriverWait(driver, 120)
    driver.get(url)

    wait = WebDriverWait(driver, 120)

    product_data = []

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    a_tags = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul.list_productcmp a.link_thumb")))
    urls = [a_tag.get_attribute("href") for a_tag in a_tags]
    time.sleep(6)

    product_url = []
    shop_url = []
    tit_detail_texts = []
    desc_price_texts = []
    img_urls_list = []
    p_texts_list = []
    # p = []
    try:
        for url in urls:
            driver.get(url)
            pattern = re.compile(r'\/([^\/]+)\/products\/')
            match = pattern.search(url)
            shopUrl = match.group(1)

            driver.implicitly_wait(60)

            tit_detail_tag = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "strong.tit_detail")))
            tit_detail_text = tit_detail_tag.text.strip()
            print(tit_detail_text)
            desc_price_tag = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "em.num_thin.emph_g")))
            desc_price_text = desc_price_tag.text.strip()

            img_tags = driver.find_elements(
                By.CSS_SELECTOR, 'div._contents.info_txt img')
            img_urls = [img.get_attribute('src') for img in img_tags]
            img_urls_str = ', '.join(img_urls)
            img_urls_list.append(img_urls_str)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            root_element = soup.find("div", "_contents info_txt")

            p_texts = [p_tag.get_text(strip=True)
                       for p_tag in root_element.find_all('p')]
            p_texts_str = ', '.join(p_texts)
            p_texts_list.append(p_texts_str)

# case of LIST element
            # root_ul = root_element.find('ul')

            # li_texts = [li.get_text(strip=True)
            #             for li in root_ul.find_all('li')]
            # li_texts_str = ', '.join(li_texts)
            # p.append(li_texts_str)

            product_url.append(url)
            shop_url.append(shopUrl)
            tit_detail_texts.append(tit_detail_text)
            desc_price_texts.append(desc_price_text)
            time.sleep(5)

        driver.quit()

        df = pd.DataFrame({
            'Product URL': product_url,
            'Shop URL': shop_url,
            'Title': tit_detail_texts,
            'Price': desc_price_texts,
            'Images': img_urls_list,
            'Details': p_texts_list
        })

        df.to_csv(
            CSV_PATH, index=False)
    except:
        driver.quit()

        df = pd.DataFrame({
            'Product URL': product_url,
            'Shop URL': shop_url,
            'Title': tit_detail_texts,
            'Price': desc_price_texts,
            'Images': img_urls_list,
            'Details': p_texts_list
        })

        df.to_csv(
            CSV_PATH, index=False)


scrape_kakao_store(KAKAO_URL)

print("Kakao scraping done. File is saved.")
print(CSV_PATH, " file saved.")
