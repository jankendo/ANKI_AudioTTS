import json
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinter.simpledialog import askstring

voice_list_file = "voice.list"


def get_voice_list():
    if not os.path.exists(voice_list_file):
        subprocess.run("edge-tts --list-voice >> voice.list", shell=True)


def adjust_layout(event):
    root.update_idletasks()
    name_listbox.config(width=root.winfo_width() // 10, height=root.winfo_height() // 25)


def create_gui_elements():
    global name_listbox, scrollbar
    # 名前を表示するリストボックス
    name_listbox = tk.Listbox(root)
    name_listbox.pack(expand=True, fill="both")

    # スクロールバーを追加
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=name_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    name_listbox.config(yscrollcommand=scrollbar.set)


def create_filter_elements():
    global gender_combobox, language_combobox, country_combobox

    gender_label = tk.Label(root, text="Gender:")
    gender_label.pack()
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

    filter_button = tk.Button(root, text="Filter Names", command=filter_names)
    filter_button.pack()


def create_buttons():
    show_all_button = tk.Button(root, text="Generate Voice", command=show_all_names)
    show_all_button.pack()
    show_all_button = tk.Button(root, text="Generate Json Voice", command=output_all_json)
    show_all_button.pack()


def filter_names():
    name_listbox.delete(0, tk.END)

    gender = gender_var.get()
    language = language_var.get()
    country = country_var.get()
    arraylist = []

    with open(voice_list_file, "r") as file:
        lines = file.readlines()

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
                            (country == "Any" or country == country_value) and \
                            name not in arraylist:
                        arraylist.append(name)
                        name_listbox.insert(tk.END, name)

    name_listbox.update()


def show_all_names():
    all_names = name_listbox.get(0, tk.END)
    text = askstring("words", "Enter Words:")
    if all_names:
        for voice in all_names:
            command = ["edge-tts", "--voice", voice, "--text", text, "--write-media", voice + ".mp3"]
            subprocess.run(command, shell=False)
    else:
        messagebox.showwarning("No Names", "There are no Names to save")


def output_all_json():
    all_names = name_listbox.get(0, tk.END)
    folder_path = filedialog.askdirectory()

    output_folder = "./output"
    os.makedirs(output_folder, exist_ok=True)

    for file_path in os.listdir(folder_path):
        if file_path.endswith(".json"):
            json_open = open(os.path.join(folder_path, file_path), 'r')
            json_load = json.load(json_open)
            jsonpath = os.path.join(output_folder, file_path.replace(".json", ""))
            os.makedirs(jsonpath, exist_ok=True)
            for voice in all_names:
                voicepath = os.path.join(jsonpath, voice)
                os.makedirs(voicepath, exist_ok=True)
                for jsoncards in json_load['cards']:
                    command = [
                        "edge-tts",
                        "--voice", voice,
                        "--text", jsoncards['sentence'],
                        "--write-media", os.path.join(voicepath, f"{voice}_{json_load['id']}_{jsoncards['id']}.mp3")
                    ]
                    subprocess.run(command, shell=False)

    if not all_names:
        messagebox.showwarning("No Names", "There are no Names to save")


get_voice_list()

root = tk.Tk()
root.title("voice filter")
root.bind('<Configure>', adjust_layout)

gender_var = tk.StringVar(root, "Any")
language_var = tk.StringVar(root, "Any")
country_var = tk.StringVar(root, "Any")

gender_choices = ["Any", "Male", "Female"]
language_choices = ["Any", "en", "ja", "es", "fr", "de", "it", "zh", "ko"]
country_choices = ["Any", "US", "GB", "JP", "ES", "FR", "DE", "IT", "CN", "KR"]

create_gui_elements()
create_filter_elements()
create_buttons()

root.mainloop()
