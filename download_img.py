import csv
from datetime import datetime
import os
import time
import re
from urllib import request

import pandas as pd


TODAY = datetime.today().strftime("%Y%m%d%H%M")
csv_path = os.path.join("C:/Users/user/Documents/개발프로그램/coupang_kakao_crawler/","coupang.csv")

# TODO :
# 폴더명 앞에 인덱스를 붙이면 어떨까, 아니면 docid라도 'ㅅ;
# 비동기로 만들어본다.
# 정상동작함!!


def read_csv_pandas(filepath):
    df = pd.read_csv(filepath,delimiter=',',encoding= 'euc-kr')
    df.head(2)
    return df


def read_csv_reader(filepath, encoding=None):

    # open("file.name", "r", encoding='utf-16')
    # open("file.name", "r", encoding='euc-kr')
    # open("file.name", "r", encoding='cp949')
    # open("file.name", "r", encoding='latin_1')

    csv_file = open(f'{filepath}', 'r', encoding='utf-8-sig')
    lines = csv.reader(csv_file)
    return lines


# csv를 읽어온다. open cs
# def read_csv_pandas(filepath):
#     # about Error tokenizing data
#     # 공백의 컬럼은 pandas 에서 결측치가 되므로
#     # csv모듈로 모두 불러온 뒤 데이터를 pandas로 변환한다.
#     f = open(filepath, 'r', encoding='utf-8-sig', errors='backslashreplace')
#     reader = csv.reader(f)
#     csv_list = []
#     for l in reader:
#         csv_list.append(l)
#     f.close()

#     df = pd.DataFrame(csv_list)

#     return df


def make_path(path, filename):
    if not os.path.exists(f'{path}'):
        os.makedirs(f'{path}')
        filepath = os.path.join(path, filename)
        print("created path : ", filepath)
        return filepath
    else:
        print("arleady exist path : ", os.path.join(path, filename))

        return os.path.join(path, filename)


def extract_filename(url_text):
    url = url_text

    filename_txt = re.findall(r"[a-zA-Z0-9-]+\.\w{3}$",  url)
    # print("filename : ", filename_txt[0], "\n")
    return filename_txt[0]


def read_csv_and_extract_urls_titles(csv_path):
    img_urls = []
    titles = []
    csv_reader = read_csv_pandas(csv_path)
    #컬럼명들을 지운다.
   

    img_datas = csv_reader['Images']
    title_datas = csv_reader['Title']
    for idx, imgs in enumerate(img_datas):
        image_strs = imgs.split(',')
        title = title_datas[idx]
        for img_str in image_strs:
            img_urls.append(img_str)
            titles.append(title.replace(' ', '_'))

    return img_urls, titles


# img_urls = URLS
img_urls, titles = read_csv_and_extract_urls_titles(csv_path)

# time check
start = time.time()
for idx, url in enumerate(img_urls):
    # extract filename
    filename = extract_filename(url)
    # make path to save
    filepath = make_path(titles[idx], filename)
    # curl 요청
    os.system("curl " + url + " > " + filepath)

# 이미지 다운로드 시간 체크
print(time.time() - start)

# 저장 된 이미지 확인
# img = Image.open("test.jpg")
