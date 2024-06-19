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
    li_texts_list = []
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
            root_ul = root_element.find('ul')

            li_texts = [li.get_text(strip=True)
                        for li in root_ul.find_all('li')]
            li_texts_str = ', '.join(li_texts)
            li_texts_list.append(li_texts_str)

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
            'Details': li_texts_list
        })

        df.to_excel('kakao_store_data.xlsx', index=False)
    except:
        driver.quit()

        df = pd.DataFrame({
            'Product URL': product_url,
            'Shop URL': shop_url,
            'Title': tit_detail_texts,
            'Price': desc_price_texts,
            'Images': img_urls_list,
            'Details': li_texts_list
        })

        df.to_excel('kakao_store_data.xlsx', index=False)


scrape_kakao_store(
    "https://store.kakao.com/kakaofriends/search/products?q=%EB%B9%A4%EC%AE%B8%ED%86%A0%EB%81%BC")

print("Kakao scraping done. File is saved. Now starting to scrape Coupang store")

time.sleep(5)


def sleepTime():
    time.sleep(random.randint(1, 5))


url_coupang = "https://www.coupang.com/np/search?rocketAll=false&searchId=1222877bf6ba4493b0ab3d5499bf4d54&q=%EB%B9%A4%EC%AE%B8%ED%86%A0%EB%81%BC&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=auto&backgroundColor=&searchProductCount=2163&component=&rating=0&sorter=scoreDesc&listSize=36"

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
    for url1 in products[:30]:
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

    df.to_excel('coupang.xlsx', index=False)
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

    df.to_excel('coupang.xlsx', index=False)
print("Coupang Data is Saved")
