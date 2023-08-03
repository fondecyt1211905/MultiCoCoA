from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json
def speech(archivo):
    wf = wave.open(archivo, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)
    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    #rec.SetPartialWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            (rec.Result())
        else:
            (rec.PartialResult())

    return json.loads(rec.FinalResult())["text"]