import tkinter as tk
from tkinter import ttk

from filter_operations import generate_single_audio, output_all_json


class GUIOperations:
    def __init__(self, root, gender_var, language_var, country_var, voice_ops):
        """
        GUIOperations クラスのコンストラクタ
        """
        self.language_combobox = None
        self.gender_combobox = None
        self.country_combobox = None
        self.name_listbox = None
        self.root = root
        self.gender_var = gender_var
        self.language_var = language_var
        self.country_var = country_var
        self.gender_choices = voice_ops.gender_choices
        self.language_choices = voice_ops.language_choices
        self.country_choices = voice_ops.country_choices

    def adjust_layout(self, event):
        """
        ウィンドウのサイズが変更されたときに呼び出される
        レイアウトを自動調整する
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.name_listbox.config(width=width // 10, height=height // 25)

    def create_gui_elements(self):
        """
        GUIの要素を作成する
        """
        # 名前を表示するリストボックス
        self.name_listbox = tk.Listbox(self.root)
        self.name_listbox.pack(expand=True, fill="both")

        # スクロールバーを追加
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.name_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.name_listbox.config(yscrollcommand=scrollbar.set)

    # フィルターの要素を作成する
    def create_filter_elements(self):
        """
        フィルターの要素を作成する
        """
        gender_label = tk.Label(self.root, text="Gender:")
        gender_label.pack()
        gender_combobox = ttk.Combobox(self.root, textvariable=self.gender_var, values=self.gender_choices)
        gender_combobox.pack()

        language_label = tk.Label(self.root, text="Language:")
        language_label.pack()
        language_combobox = ttk.Combobox(self.root, textvariable=self.language_var, values=self.language_choices)
        language_combobox.pack()

        country_label = tk.Label(self.root, text="Country:")
        country_label.pack()
        country_combobox = ttk.Combobox(self.root, textvariable=self.country_var, values=self.country_choices)
        country_combobox.pack()

    def create_buttons(self):
        """
        ボタンを作成する
        """
        single_button = tk.Button(self.root, text="Generate Single Voice",
                                  command=lambda: generate_single_audio(self.name_listbox))
        single_button.pack()
        json_button = tk.Button(self.root, text="Generate Json Voice",
                                command=lambda: output_all_json(self.name_listbox))
        json_button.pack()

    def update_combobox_choices(self):
        """
        コンボボックスの選択肢を更新する
        """
        # 各コンボボックスの選択肢を更新
        self.language_combobox['values'] = self.language_choices
        self.country_combobox['values'] = self.country_choices

        # 初期選択を更新
        self.language_combobox.set(self.language_var.get())
        self.country_combobox.set(self.country_var.get())
