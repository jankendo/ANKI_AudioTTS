import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# voice.listファイルのパス
voice_list_file = "voice.list"
subprocess.run("edge-tts --list-voice >> voice.list", shell=True)

# GUIの作成
root = tk.Tk()
root.title("voice filter")


# ウィンドウのサイズに合わせてレイアウトを調整する関数
def adjust_layout(event):
    root.update_idletasks()

    # 検索結果で表示されるエリアのサイズをウィンドウのサイズに合わせて調整
    name_listbox.config(width=root.winfo_width() // 10, height=root.winfo_height() // 25)


# ウィンドウのサイズ変更時にレイアウトを自動調整するように設定
root.bind('<Configure>', adjust_layout)

# 名前を表示するリストボックス
name_listbox = tk.Listbox(root)
name_listbox.pack(expand=True, fill="both")

# スクロールバーを追加
scrollbar = ttk.Scrollbar(root, orient="vertical", command=name_listbox.yview)
scrollbar.pack(side="right", fill="y")
name_listbox.config(yscrollcommand=scrollbar.set)

# 選択されたNameを表示するラベル
selected_name_label = tk.Label(root)
selected_name_label.pack()


# Nameをフィルタリングする関数
def filter_names():
    # リストボックスの内容をクリア
    name_listbox.delete(0, tk.END)

    # フィルタ条件の取得
    gender = gender_var.get()
    language = language_var.get()
    country = country_var.get()

    # voice.listファイルの読み込み
    with open(voice_list_file, "r") as file:
        lines = file.readlines()

        # フィルタ条件に合致するNameをリストボックスに追加
        for i in range(len(lines) - 2):
            if lines[i].startswith("Name:"):
                name = lines[i][6:].strip()
                gender_value = lines[i + 1][8:].strip()
                if not lines[i + 2].startswith("\n"):
                    continue
                language_country = lines[i].split("-", 1)
                if len(language_country) >= 2:
                    language_value = language_country[0].replace("Name: ", "")
                    country_value = language_country[1].strip().split("-")[0]
                    if (gender == "Any" or gender == gender_value) and \
                            (language == "Any" or language == language_value) and \
                            (country == "Any" or country == country_value):
                        name_listbox.insert(tk.END, name)

    name_listbox.update()


# 決定ボタンを押したときに呼ばれる関数
def show_selected_name():
    # 選択されたNameを取得
    selected_names = name_listbox.curselection()
    if selected_names:
        selected_name = name_listbox.get(selected_names[0])
        selected_name_label.config(text="Selected Name: " + selected_name)
        messagebox.showinfo("Selected Name", "Selected Name: " + selected_name)
    else:
        selected_name_label.config(text="Selected Name: None")


# フィルタ条件の初期値
gender_var = tk.StringVar(root, "Any")
language_var = tk.StringVar(root, "Any")
country_var = tk.StringVar(root, "Any")

# フィルタ条件の選択肢を作成
gender_choices = ["Any", "Male", "Female"]
language_choices = ["Any", "en", "ja", "es", "fr", "de", "it", "zh", "ko"]
country_choices = ["Any", "US", "GB", "JP", "ES", "FR", "DE", "IT", "CN", "KR"]

# ラベルとコンボボックスの作成
gender_label = tk.Label(root, text="Gender:")
gender_label.pack()
# ttk.Comboboxを使用するための修正
gender_combobox = ttk.Combobox(root, textvariable=gender_var, values=gender_choices)
gender_combobox.pack()

language_label = tk.Label(root, text="Language:")
language_label.pack()
language_combobox = ttk.Combobox(root, textvariable=language_var, values=language_choices)
language_combobox.pack()

country_label = tk.Label(root, text="Country:")
country_label.pack()
country_combobox = ttk.Combobox(root, textvariable=country_var, values=country_choices)
country_combobox.pack()

# フィルタリングボタンを作成
filter_button = tk.Button(root, text="Filter Names", command=filter_names)
filter_button.pack()

# 決定ボタンを作成
select_button = tk.Button(root, text="Select Name", command=show_selected_name)
select_button.pack()

# ウィンドウを表示
root.mainloop()
