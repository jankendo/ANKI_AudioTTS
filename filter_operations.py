# filter_operations.py
import json
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import messagebox


def generate_single_audio(name_listbox):
    """
    選択された名前からオーディオファイルを生成する。
    """
    selected_indexes = name_listbox.curselection()

    if not selected_indexes:
        messagebox.showwarning("No Names", "There are no Names to save")
        return

    for index in selected_indexes:
        voice = name_listbox.get(index)
        text = simpledialog.askstring("Words", "Enter Words:")

        try:
            # Create a temporary file in the current directory
            temp_file_path = f"{voice}_temp.mp3"
            command = ["edge-tts", "--voice", voice, "--text", text, "--write-media", temp_file_path]
            subprocess.run(command, shell=False)
        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", f"The file {e.filename} does not exist.")


def output_all_json(name_listbox):
    """
    選択された名前からオーディオファイルを生成する。
    """
    all_names = name_listbox.get(0, tk.END)
    folder_path = filedialog.askdirectory()

    output_folder = "./Voices"
    os.makedirs(output_folder, exist_ok=True)

    for file_path in os.listdir(folder_path):
        if file_path.endswith(".json"):
            json_open = open(os.path.join(folder_path, file_path), 'r')
            json_load = json.load(json_open)
            jsonpath = os.path.join(output_folder, f"deck{json_load['id']}")
            os.makedirs(jsonpath, exist_ok=True)
            for voice in all_names:
                voicepath = os.path.join(jsonpath, voice)
                os.makedirs(voicepath, exist_ok=True)
                for jsoncards in json_load['cards']:
                    command = [
                        "edge-tts",
                        "--voice", voice,
                        "--text", jsoncards['sentence'],
                        "--write-media", os.path.join(voicepath, f"{jsoncards['id']}.mp3")
                    ]
                    subprocess.run(command, shell=False)

    if not all_names:
        messagebox.showwarning("No Names", "There are no Names to save")


class FilterOperations:

    def __init__(self, root, guiops, voice_list_file):
        self.name_listbox = guiops.name_listbox
        self.root = root
        self.VOICE_LIST_FILE = voice_list_file
        self.gender_var = guiops.gender_var
        self.language_var = guiops.language_var
        self.country_var = guiops.country_var
        self.gender_choices = guiops.gender_choices
        self.language_choices = guiops.language_choices
        self.country_choices = guiops.country_choices

    def filter_names(self):
        """
        フィルターを適用して名前を表示する
        """
        self.name_listbox.delete(0, tk.END)

        selected_gender = self.gender_var.get()
        selected_language = self.language_var.get()
        selected_country = self.country_var.get()
        unique_names = []

        with open(self.VOICE_LIST_FILE, "r") as file:
            lines = file.readlines()

            for i in range(len(lines) - 2):
                if lines[i].startswith("Name:"):
                    name = lines[i][6:].strip()
                    gender_value = lines[i + 2][8:].strip()
                    if not lines[i + 3].startswith("\n"):
                        continue
                    language_country = lines[i].split("-", 1)
                    if len(language_country) >= 2:
                        language_value = language_country[0].replace("Name: ", "")
                        country_value = language_country[1].strip().split("-")[0]
                        if (selected_gender == "Any" or selected_gender == gender_value) and \
                                (selected_language == "Any" or selected_language == language_value) and \
                                (selected_country == "Any" or selected_country == country_value) and \
                                name not in unique_names:
                            unique_names.append(name)
                            self.name_listbox.insert(tk.END, name)

        self.name_listbox.update()
