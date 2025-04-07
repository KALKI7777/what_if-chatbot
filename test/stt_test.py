import whisper

model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
result = model.transcribe(r"audio\Romeo_and_Juliet_Act_1_64kb.mp3")
print(result["text"])

# Save to file
with open(r"R:\KuKu FM project\test\output.txt", "w") as file:
    file.write(result["text"])
