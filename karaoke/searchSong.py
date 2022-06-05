# -*- coding: utf-8 -*-
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time

# ブラウザ
#browser_path = 'browser/chrome.exe'
# ドライバ
#driver_path = 'driver/chromedriver.exe'

def get_srch_song_list(song_name):
    # 曲一覧の取得
    SEARCH_RESULT = f'https://www.clubdam.com/karaokesearch/?keyword={song_name}'
    # 取得結果
    current_value = ''

    options = Options()
    # ヘッドレスモードで実行する場合
    options.add_argument("--headless")
    #driver = webdriver.Chrome("google-chrome", options=options)
    driver = webdriver.Chrome(options=options)


    try:
        # 取得先URLにアクセス
        driver.get(SEARCH_RESULT)
        # コンテンツが描画されるまで待機
        time.sleep(3)

        # 対象を抽出
        #values = driver.find_element_by_id("data_\d")
        #current_value = str(values.text)
        values = driver.find_elements_by_class_name('result-item')
        #values = driver.find_elements_by_css_selector('li[class^="result-item"]')
        #print(value.text)
        songs=[]
        for val in values:
            url = str(val.get_attribute("data-url"))
            #print(url)
            idx = int(url.find('='))
            #print(idx)
            song_id = str(url[idx+1:])
            content = val.text.replace('\n', ' / ')
            songs.append([song_id,content])
            #print(song_id)
            #print(val.text)

    finally:
        # プラウザを閉じる
        driver.quit()
    
    return songs


if __name__ == '__main__':
    get_srch_song_list('ご注文はうさぎですか')