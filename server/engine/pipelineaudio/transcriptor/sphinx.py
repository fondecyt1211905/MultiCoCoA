import speech_recognition as sr
def speech(archivo):
    r = sr.Recognizer()

    with sr.AudioFile(archivo) as source:
        audio = r.record(source)

    return r.recognize_sphinx(audio, language='es')