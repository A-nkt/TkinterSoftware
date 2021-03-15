import tkinter
from tkinter import messagebox
import sqlite3
import tkinter.ttk as ttk
import tkinter.font as font
import os
from tkinter import filedialog
from tkinter import StringVar
import pandas as pd
from tqdm import tqdm
import jaconv

class ProgressBarSampleApp(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.pack()

        input_label = ttk.Label(self,text="DBを作成中")
        input_label.pack(side="left")
        self.pbIndeterminateVer = ttk.Progressbar(self, orient=tkinter.HORIZONTAL, length=200, mode='indeterminate')
        self.pbIndeterminateVer.pack(side="left")
        self.pbIndeterminateVer.start(10)

def CreateUser():
    def button_click(event):
        input_value = input_box.get()
        input_value_kana = input_box_kana.get()
        cur.execute('SELECT * FROM data WHERE input_name_kana="'+ str(input_value_kana) +'"')
        dataset = cur.fetchall()

        if len(dataset) == 0:
            try:
                c.execute('INSERT INTO data(input_name, input_name_kana) VALUES("'+ str(input_value) + '", "' + str(input_value_kana) +'")')
                c.commit()
                tkinter.messagebox.showinfo("完了",input_value + "を登録しました。")
            except:
                tkinter.messagebox.showinfo("エラー","登録できませんでした")
        elif input_value == "":
            tkinter.messagebox.showinfo("エラー","名前を入力してください。")
        else:
            tkinter.messagebox.showinfo("エラー","すでに同じ名前が登録されています。")
        main()
        newwindow.destroy()

    newwindow = tkinter.Tk()
    my_font = font.Font(newwindow,family="メイリオ",size=12)
    newwindow.title("新規登録")
    newwindow.geometry("480x180")

    #ラベルの作成
    input_label = tkinter.Label(newwindow,text="氏名",font=my_font)
    input_label.place(x=10, y=30)
    #入力欄の作成
    input_box = tkinter.Entry(newwindow,width=30,font=my_font)
    input_box.place(x=100, y=30)
    #ラベルの作成
    input_label_kana = tkinter.Label(newwindow,text="氏名(カナ)",font=my_font)
    input_label_kana.place(x=10, y=60)
    #入力欄の作成
    input_box_kana = tkinter.Entry(newwindow,width=30,font=my_font)
    #input_box_kana.bind("<Return>",button_click)
    input_box_kana.place(x=100, y=60)
    #ボタンの作成
    button = tkinter.Button(newwindow,text="登録",font=my_font)
    button.bind("<1>",button_click)

    button.place(x=10, y=110)
    #ウインドウの描画
    newwindow.mainloop()

def callback(event):
    def button_submit(event):
        text_value = text_widget.get("1.0", "end")
        try:
            c.execute('UPDATE data set content = "'+ str(text_value) +'" where input_name = "'+ str(input_name) +'"')
            c.commit()
            tkinter.messagebox.showinfo("完了","データを登録しました。")
        except:
            tkinter.messagebox.showinfo("エラー","登録できませんでした")
        main()
        newwindow.destroy()

    newwindow = tkinter.Tk()
    Title_font = font.Font(newwindow,family="メイリオ",size=16)
    Content_font = font.Font(newwindow,family="メイリオ",size=10)
    newwindow.title(u"顧客情報")
    newwindow.geometry("700x800")

    newframe = tkinter.Frame(newwindow,width=10000,height=50)
    newframe.pack()
    newframe2 = tkinter.Frame(newwindow,width=10000,height=600)
    newframe2.pack()
    input_name = event.widget["text"]
    Static1 = tkinter.Label(newframe,text=event.widget["text"],font=Title_font)
    Static1.pack(side="left", pady=(30, 10))

    cur.execute('SELECT * FROM data WHERE input_name="'+ str(event.widget["text"]) +'"') #名前からdataを抽出
    dataset = cur.fetchall()

    Static2 = tkinter.Label(newframe,text='(' + dataset[0][2] + ')',font=Title_font)
    Static2.pack(side="left",pady=(30, 10))

    text_widget = tkinter.Text(newframe2,font=Content_font)
    try:
        text_widget.insert('1.0',dataset[0][3])
    except:
        pass
    text_widget.grid()
    text_widget.place(x=10, y=50)
    button = tkinter.Button(newwindow,text="登録",font=Title_font)
    button.place(x=25, y=625)
    button.bind("<1>",button_submit)

    newwindow.mainloop()

def callback_search(event):
    def button_submit():
        text_value = text_widget.get("1.0", "end")
        # SQLを発行してDBへ登録
        try:
            c.execute('UPDATE data set content = "'+ str(text_value) +'" where input_name = "'+ str(dataset[0][1]) +'"')
            c.commit()
            tkinter.messagebox.showinfo("完了","データを登録しました。")
        # ドメインエラーなどにより登録できなかった場合のエラー処理
        except:
            tkinter.messagebox.showinfo("エラーにより登録できませんでした")
        main()
        newwindow.destroy()
    input_value = input_box.get()
    # カナ検索
    cur.execute('SELECT * FROM data WHERE input_name_kana="'+ str(input_value) +'"')
    dataset = cur.fetchall()
    # 通常検索
    if len(dataset) == 0:
        cur.execute('SELECT * FROM data WHERE input_name="'+ str(input_value) +'"')
        dataset = cur.fetchall()
    #　検索結果,width=8
    if input_value == "":
        tkinter.messagebox.showinfo("エラー","検索ワードを入力してください")
    elif len(dataset) == 0:#検索結果がない時
        tkinter.messagebox.showinfo("検索結果","登録データがありませんでした")
    #検索結果がある時
    else:
        newwindow = tkinter.Tk()
        Title_font = font.Font(newwindow,family="メイリオ",size=16)
        Content_font = font.Font(newwindow,family="メイリオ",size=10)
        newwindow.title(u"顧客情報")
        newwindow.geometry("700x800")

        newframe = tkinter.Frame(newwindow,width=10000,height=50)
        newframe.pack()
        newframe2 = tkinter.Frame(newwindow,width=10000,height=600)
        newframe2.pack()

        Static1 = tkinter.Label(newframe,text=dataset[0][1],font=Title_font)
        Static1.pack(side="left", pady=(30, 10))

        Static2 = tkinter.Label(newframe,text='(' + dataset[0][2] + ')',font=Title_font)
        Static2.pack(side="left",pady=(30, 10))

        text_widget = tkinter.Text(newframe2,font=Content_font)
        try:
            text_widget.insert('1.0',dataset[0][3])
        except:
            pass
        text_widget.grid()
        text_widget.place(x=10, y=50)
        button = tkinter.Button(newwindow,text="登録",command=button_submit,font=Title_font)
        button.place(x=25, y=625)

        newwindow.mainloop()

def file_search(event):
    # ファイル指定の関数
    def filedialog_clicked():
        fTyp = [("", "*")]
        iFile = os.path.abspath(os.path.dirname(__file__))
        iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
        IFileEntry.insert(0, iFilePath)
        file1.set(iFilePath)

    def conductMain():
        file = file1.get()
        root, ext = os.path.splitext(file)
        #db_name = input_box.get()
        #print(db_name)
        #csvの時
        if ext == '.csv':
            #dataの読み取り・登録
            df = pd.read_csv(file,encoding="shift-jis")

            dbname = "database.db"#dbname = str(db_name) + ".db"
            c = sqlite3.connect(dbname)
            cur = c.cursor()
            try:
                ddl = 'CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT, input_name STRING, input_name_kana STRING, content TEXT)'
                cur.execute(ddl)
                c.commit()
            except sqlite3.OperationalError:
                pass

            tkinter.messagebox.showinfo("Start","データベースを作成します\n完了画面が出るまで何も触らずにお待ちください")
            for k in tqdm(range(len(df))):
                input_value = df.loc[k,'得意先略称'][1:]
                input_value_han_kana = df.loc[k,'名カナ'][1:]
                input_value_kana = jaconv.hira2hkata(input_value_han_kana)
                input_value_kana = jaconv.h2z(input_value_kana,digit=True, ascii=True)
                content = df.loc[k,'備考'][1:]

                c.execute('INSERT INTO data(input_name, input_name_kana,content) VALUES("'+ str(input_value) + '", "' + str(input_value_kana) + '", "' + str(content) + '")')
                c.commit()
            tkinter.messagebox.showinfo("完了","データベースが作成されました")
        #csv以外
        else:
            tkinter.messagebox.showinfo("不適切なファイル形式です","csvファイルを指定してください")

        newwindow.destroy()

    def back():
        newwindow.destroy()

    newwindow = tkinter.Tk()
    my_font = font.Font(newwindow,family="メイリオ",size=12)
    newwindow.title("CSVインポート")
    newwindow.geometry("580x220")
    newwindow.attributes('-topmost', True)

    frame2 = tkinter.Frame(newwindow)
    frame2.grid(row=2, column=1, sticky=tkinter.E)

    IFileLabel = tkinter.Label(frame2, text="ファイル参照＞＞",font=my_font)
    IFileLabel.pack(side=tkinter.LEFT)

    file1 = StringVar()
    IFileEntry = tkinter.Entry(frame2, width=30,font=my_font)
    IFileEntry.pack(side=tkinter.LEFT)

    IFileButton = tkinter.Button(frame2, text="参照", command=filedialog_clicked,font=my_font)
    IFileButton.pack(side=tkinter.LEFT, padx=10)

    #frame22 = tkinter.Frame(newwindow)
    #frame22.grid(row=5,column=1,sticky=tkinter.W)

    #input_label = tkinter.Label(frame22,text="DB名>>",font=my_font)
    #input_label.pack(fill='x', padx=10,side="left",pady=5)

    #input_box = tkinter.Entry(frame22,width=20,font=my_font)
    #input_box.pack(fill='x', padx=10,side="left",pady=5)

    frame3 = tkinter.Frame(newwindow)
    frame3.grid(row=6,column=1,sticky=tkinter.W)

    button1 = tkinter.Button(frame3, text="実行", command=conductMain,font=my_font)
    button1.pack(fill = "x", padx=30, side = "left",pady=5)

    button2 = tkinter.Button(frame3, text="閉じる", command=back,font=my_font)
    button2.pack(fill = "x", padx=10, side = "left",pady=5)

    newwindow.mainloop()


def main():
    dbname = "database.db"
    c = sqlite3.connect(dbname)
    cur = c.cursor()
    cur.execute('SELECT * FROM data')
    dataset = cur.fetchall()

    def mouse_y_scroll(event):
        if event.delta > 0:
            canvas.yview_scroll(-1, 'units')
        elif event.delta < 0:
            canvas.yview_scroll(1, 'units')

    canvas = tkinter.Canvas(frame3, height=600,width=350)
    canvas.grid(row=0, column=0)

    scrollbar = tkinter.Scrollbar(frame3, orient=tkinter.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky=(tkinter.N, tkinter.S))
    canvas["yscrollcommand"] = scrollbar.set
    canvas.yview_moveto(0)

    size_y = len(dataset) * 38
    canvas.config(scrollregion=(0,0,0,size_y))

    frame_canvas = tkinter.Frame(canvas)
    canvas.create_window((0,0), window=frame_canvas, anchor=tkinter.NW, width=canvas.cget('width'))
    canvas.bind("<MouseWheel>", mouse_y_scroll)
    canvas.bind("<1>", mouse_y_scroll)

    for j in range(len(dataset)):
        style = ttk.Style()
        style.configure("office.TButton", font=my_font)
        button1 = ttk.Button(frame_canvas, text=dataset[j][1], style="office.TButton", width=350, compound="left")
        #button1=tkinter.Button(frame_canvas, text=dataset[j][1],font=my_font,width=350,height=1)
        button1.bind("<MouseWheel>", mouse_y_scroll)
        button1.bind("<1>",callback)
        button1.pack(pady=0.1)
        #button1.pack(pady=0.1,ipady=10)

dbname = "database.db"
c = sqlite3.connect(dbname)
cur = c.cursor()
try:
    ddl = 'CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT, input_name STRING, input_name_kana STRING, content TEXT)'
    cur.execute(ddl)
    c.commit()
except sqlite3.OperationalError:
    pass

root = tkinter.Tk()
my_font = font.Font(root,family="メイリオ",size=14)
root.title(u"Python Software")
root.geometry("800x900")

frame1 = tkinter.Frame(root,width=10000,height=200)
frame1.pack()
frame2 = tkinter.Frame(root,width=10000,height=200)
frame2.pack()
frame2_1 = tkinter.Frame(root,width=10000,height=200)
frame2_1.pack()
frame3 = tkinter.Frame(root)
frame3.pack()

#新規登録
button1=tkinter.Button(frame1, text="新規登録",command=CreateUser,font=my_font,width=8)
button1.pack(fill='x', padx=20,side="left",pady=20)
#更新
button2=tkinter.Button(frame1, text="更新",command=main,font=my_font,width=8)
button2.pack(fill='x', padx=20,side="left",pady=20)
#検索
input_box = tkinter.Entry(frame2,width=20,font=my_font)
input_box.bind("<Key-F5>",callback_search)
input_box.pack(fill='x', padx=10,side="left",pady=5)

button = tkinter.Button(frame2,text="検索",font=my_font)
button.bind("<1>",callback_search)
button.pack(fill='x', padx=10,side="left")

button1 = tkinter.Button(frame2_1,text="CSV インポート",font=my_font)
button1.bind("<1>",file_search)
button1.pack(fill='x',pady=20,side="left")

main()

root.mainloop()
