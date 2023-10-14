# voice_operations.py
import os
import subprocess
import re


class VoiceOperations:
    def __init__(self):
        self.VOICE_LIST_FILE = "voice.list"
        self.gender_choices = ["Any", "Male", "Female"]
        self.language_choices = ["Any"]
        self.country_choices = ["Any"]

    def get_voice_list(self):
        """
        現在利用可能な音声の一覧を取得する
        """
        try:
            # Check if VOICE_LIST_FILE exists and delete it if it does
            if os.path.exists(self.VOICE_LIST_FILE):
                os.remove(self.VOICE_LIST_FILE)

            result = subprocess.run("edge-tts --list-voice", shell=True, capture_output=True)
            output = result.stdout.decode()
            with open(self.VOICE_LIST_FILE, "w") as file:
                file.write(output)

            # Extract gender, language, and country choices from the voice list file
            self.extract_choices_from_voice_list(output)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def extract_choices_from_voice_list(self, voice_list):
        """
        音声リストから性別、言語、国の選択肢を抽出する
        """
        lines = voice_list.split('\n')
        for line in lines:
            if line.startswith("Name:"):
                pattern = r"(\w{2})-(\w{2})"
                match = re.search(pattern, line)
                language_choice = match.group(1)
                country_choice = match.group(2)
                if language_choice not in self.language_choices:
                    self.language_choices.append(language_choice)
                if country_choice not in self.country_choices:
                    self.country_choices.append(country_choice)
