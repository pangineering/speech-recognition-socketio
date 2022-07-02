import speech_recognition as sr

recog = sr.Recognizer()
audio_file_ = sr.AudioFile("test.wav")

with audio_file_ as source:
    audio_file = recog.record(source, duration = 7.0)
    result = recog.recognize_google(audio_data=audio_file, language='th')
    print(result)

# print(sr.Microphone.list_microphone_names())
# mic = sr.Microphone(2)
# with mic as source:
#     while True:
#         audio = recog.listen(source)
#         try:
#             print(recog.recognize_google(audio,language='th'))
#         except:
#             continue