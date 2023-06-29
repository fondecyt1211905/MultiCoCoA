import speech_recognition as sr
def speech(archivo):
    r = sr.Recognizer()

    with sr.AudioFile(archivo) as source:
        audio = r.record(source)
    #Se cambio por una variable "a" ya que solo mandaba el primer fragmento del audio
    #No se sabe por qué pasa esto, pero al mandarlo de esa forma se envia todo el texto.
    a = r.recognize_google(audio, language='es')
    return a