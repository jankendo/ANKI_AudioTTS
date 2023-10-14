# main.py
import tkinter as tk
from voice_operations import VoiceOperations
from gui_operations import GUIOperations
from filter_operations import FilterOperations


class VoiceFilterApp:
    def __init__(self):
        self.filter_button = None
        self.name_listbox = None

        self.root = tk.Tk()
        self.root.title("Voice Filter")
        self.root.bind('<Configure>', self.adjust_layout)

        # これらの変数を tk.StringVar で初期化
        self.gender_var = tk.StringVar(value="Any")
        self.language_var = tk.StringVar(value="Any")
        self.country_var = tk.StringVar(value="Any")

        self.voice_ops = VoiceOperations()
        self.voice_ops.get_voice_list()
        self.gui_ops = GUIOperations(self.root, self.gender_var, self.language_var, self.country_var,
                                     self.voice_ops)

        self.create_gui_elements()
        self.create_filter_elements()
        self.filter_ops = FilterOperations(self.root, self.gui_ops, self.voice_ops.VOICE_LIST_FILE)

        self.filter_buttons()
        self.create_buttons()

    def run(self):
        self.root.mainloop()

    def adjust_layout(self, event):
        self.gui_ops.adjust_layout(event)

    def create_gui_elements(self):
        self.gui_ops.create_gui_elements()

    def create_filter_elements(self):
        self.gui_ops.create_filter_elements()

    def create_buttons(self):
        self.gui_ops.create_buttons()

    def filter_buttons(self):
        self.filter_button = tk.Button(self.root, text="Filter Names", command=self.filter_ops.filter_names)
        self.filter_button.pack()


if __name__ == "__main__":
    app = VoiceFilterApp()
    app.run()
