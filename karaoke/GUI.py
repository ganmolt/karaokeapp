from turtle import width, window_width
import tkinter as tk

import getUserData, searchSong

import csv
import pandas as pd

try:
    user_name = open('user.txt').read()
    CSV_usrScrData = pd.read_csv(filepath_or_buffer="scr.csv", encoding="utf-8", sep=",")
except:
    user_name = 'No Data'
    print('No Data')


class Frame(tk.Frame):
    def __init__(self,master=None):
        def btn_get_usrdata():
            global user_name;user_name=txtbxUsrnm.get()
            usrnmLbl['text'] = '現在のユーザー: ' + user_name
            getUserData.get_score(user_name)
            # csvデータを再読み込みする
            global CSV_usrScrData;CSV_usrScrData = pd.read_csv(filepath_or_buffer="./scr.csv", encoding="utf-8", sep=",")

        def btn_srch():
            # 検索キーワードを取得
            song_name=txtbxSrchwrd.get()
            # 検索キーワードからデータを取得
            song_id_list=searchSong.get_srch_song_list(song_name)

            # 検索キーワード表示
            SrchKywrdLbl['text'] = '検索キーワード: ' + song_name
            
            # 検索結果を空にする
            SrchRsltLbl.delete("1.0","end")

            # 点数色分け
            SrchRsltLbl.tag_config('true_100', background="#fc1")
            SrchRsltLbl.tag_config('total_100', background="#fff550")
            SrchRsltLbl.tag_config('total_over99', background="#ffa")
            SrchRsltLbl.tag_config('total_over98', background="#cfc")
            SrchRsltLbl.tag_config('total_over95', background="#aff")
            SrchRsltLbl.tag_config('total_over90', background="#ccf")
            SrchRsltLbl.tag_config('total_over85', background="#fbf")
            SrchRsltLbl.tag_config('total_over80', background="#fcd")
            
            # song_id_list: s={song_id(='0000-00'),content(='song_name / singer_name')}検索結果
            for s in song_id_list:
                # 点数
                point = CSV_usrScrData[ CSV_usrScrData['song_id']==s[0] ]['point']
                # 素点
                rawPoint = CSV_usrScrData[ CSV_usrScrData['song_id']==s[0] ]['rawPoint']
                # 表示する点数
                data = '' # 点数がなかったら表示しない
                # 表示する色
                col = None # 点数がないor(point)<80なら白
                # 採点結果が得られた場合
                if not point.empty:
                    # pointをseries型からfloat型に変換
                    data = point.iloc[-1] # value部分を取得
                    fdata = float(data) # float_data
                    if float(rawPoint.iloc[-1])==100: # 素点100点の処理
                        col = 'true_100'
                    else: # 素点100点出ない場合
                        if fdata == 100: # 100点
                            col = 'total_100'
                        elif fdata >= 99: # 99点以上
                            col = 'total_over99'
                        elif fdata >= 98: # 98点以上
                            col = 'total_over98'
                        elif fdata >= 95: # 95点以上
                            col = 'total_over95'
                        elif fdata >= 90: # 90点以上
                            col = 'total_over90'
                        elif fdata >= 85: # 85点以上
                            col = 'total_over85'
                        elif fdata >= 80: # 80点以上
                            col = 'total_over80'
                    #print( data, col )
                # テキストエリアに表示する文字列を1行ずつ作成
                if not point.empty:
                    data = data + ' '
                line = data + s[0] + ' ' + s[1] + '\n'
                SrchRsltLbl.insert('end', line, col)

        # -----------ウィンドウ設定------------
        # メインウィンドウを作成
        tk.Frame.__init__(self, master)

        # ウィンドウのサイズを設定
        self.master.geometry('800x500')

        # ウィンドウのタイトルを設定
        self.master.title('GYAAAAAA!!')
        # -------------------------------------/

        # ----------------HEADER---------------
        f_header = tk.Frame(self.master, relief=tk.RIDGE, bd=5)
        # -----------個人データ取得------------
        f1 = tk.Frame(f_header, relief=tk.RIDGE, bd=1)

        # ユーザー名
        usrnmLbl = tk.Label(f1,text=f'現在のユーザー: {user_name}')
        usrnmLbl.pack()

        # ラベル
        txtbxUsrnmLbl = tk.Label(f1,text='ユーザー名を入力')
        txtbxUsrnmLbl.pack()

        # user_nameを取得するテキストボックス
        txtbxUsrnm = tk.Entry(f1,width=20)
        txtbxUsrnm.pack()

        # データ送信ボタン
        btn = tk.Button(f1, text='データ取得', command=btn_get_usrdata)
        btn.pack()

        f1.pack(side=tk.RIGHT)
        # -------------------------------------/
        # ------------検索結果取得-------------
        f2 = tk.Frame(f_header, relief=tk.RIDGE, bd=1)

        # ラベル
        txtbxSrchLbl = tk.Label(f2,text='キーワードを入力')
        txtbxSrchLbl.pack()

        # キーワードを入力するテキストボックス
        txtbxSrchwrd = tk.Entry(f2,width=20)
        txtbxSrchwrd.pack()

        # データ送信ボタン
        btn2 = tk.Button(f2, text='検索', command=btn_srch)
        btn2.pack()

        # ラベル
        SrchKywrdLbl = tk.Label(f2,text='検索キーワード:')
        SrchKywrdLbl.pack()

        f2.pack(side=tk.LEFT)
        # -------------------------------------/
        f_header.pack(anchor=tk.N, fill=tk.X)
        # ---------------HEADER----------------/
        main_contents = tk.Frame(self.master, relief=tk.RIDGE, bd=1)
        # ラベル
        SrchRsltLbl = tk.Text(main_contents)
        SrchRsltLbl.pack()

        main_contents.pack(expand=True, fill=tk.BOTH)

if __name__ == '__main__':
    f_main = Frame()
    f_main.pack()
    f_main.mainloop()