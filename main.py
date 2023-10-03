import subprocess

voice = "en-ZA-LeahNeural"
text = "HEELO"
output_file = "hello8.mp3"

command = ["edge-tts", "--voice", voice, "--text", text, "--write-media", output_file]
subprocess.run(command, shell=False)
