# -*- coding: utf-8 -*-
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_binary
import time

def get_score(user_name):
	# ユーザーネームを保存
	user_file = open('user.txt', 'w')
	user_file.write(user_name)
	user_file.close()
	# 曲一覧の取得
	SONG_LIST_BASE = f'https://dx-g.clubdam.info/user/{user_name}/song/index/max_totalPoint/desc/'
	options = Options()
	# ヘッドレスモードで実行する場合
	options.add_argument("--headless")
	driver = webdriver.Chrome(options=options)

	file = open('scr.csv', 'w') # 書き込みファイルの準備
	try:
		## ラベル
		#file.write('song_id'+',')
		#file.write('song_name'+',')
		#file.write('singer_name'+',')
		#file.write('point'+',')
		#file.write('rawPoint'+',')
		#file.write('chart_total'+',')
		#file.write('\n')
		# ページ数
		i = 1
		while True:
			# 取得先URLにアクセス
			driver.get(SONG_LIST_BASE+str(i))
			
			# コンテンツが描画されるまで待機
			time.sleep(1)

			# 対象を抽出
			values = driver.find_elements(By.CSS_SELECTOR, 'tbody[id^="data_"]')
			if not values:
				break
			# ラベル
			file.write('song_id'+',')
			file.write('song_name'+',')
			file.write('singer_name'+',')
			file.write('point'+',')
			file.write('rawPoint'+',')
			file.write('chart_total'+',')
			file.write('\n')
			for val in values:
				# データをきれいにする
				#選曲番号
				song_id = str(val.get_attribute("data-requestno"))
				#曲名と歌手名を分離
				content = val.find_element(By.CLASS_NAME, 'table_song').text
				sep_idx = content.find('/')
				#曲名
				song_name = content[:sep_idx-1].replace(',', '.')
				#歌手名
				singer_name = content[sep_idx+2:].replace(',', '.')
				#ボーナス込み点数
				point = val.find_element(By.CLASS_NAME, 'table_point').text
				#ボーナス無し点数(素点)
				rawPoint = val.find_element(By.CLASS_NAME, 'table_rawPoint').text
				#5値合計
				chart_total=val.find_element(By.CLASS_NAME, 'table_chart_total').text

				###
				file.write(song_id+',')
				file.write(song_name+',')
				file.write(singer_name+',')
				file.write(point+',')
				file.write(rawPoint+',')
				file.write(chart_total+',')
				file.write('\n')
			i += 1
	finally:
		# プラウザを閉じる
		driver.quit()
		file.close()

# データ取得を実行
if __name__ == '__main__':
	get_score('ganmalt')