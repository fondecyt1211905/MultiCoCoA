# Abrir un archivo de audio .wav
import wave
import sys, os
import time
import json
import argparse
print(os.getcwd())
sys.path.append(''.join((os.getcwd(), '/server/engine/pipelineaudio/config')))
sys.path.append(''.join((os.getcwd(), '/server/engine/pipelineaudio/helpers')))
import config # No es error
import helpers # No es error
conf = config.CONFIG

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--wav", type=argparse.FileType('rb'), required=True, help="URI de archivo AUDIO WAV")
parser.add_argument("--name", default="MIC", help="Nombre del dispositivo, Default = MIC")
parser.add_argument("--id", default="0000000000000001", help="Identificador, Default = 0000000000000001")
parser.add_argument("--type", default="AUDIO", help="Tipo de dispositivo, Default = AUDIO")
parser.add_argument("--format", default="pyaudio.paInt16", help="Tipo de dispositivo, Default = pyaudio.paInt16")
parser.add_argument("--start", type=int, default=0, help="Indica el segundo para iniciar lectura, Default = 0")
parser.add_argument("--end", type=int, default=0, help="Indica el segundo para finalizar lectura, Default = None")
parser.add_argument("--chunk", type=int, default=100, help="chunk")
parser.add_argument("--user", default=conf["user"], help="usuario rabbitmq")
parser.add_argument("--password", default=conf["password"], help="password rabbitmq")
parser.add_argument("--host", default=conf["host"], help="host rabbitmq")
parser.add_argument("--port", type=int, default=conf["port"], help="port rabbitmq")
parser.add_argument("--timeout", type=int, default=conf["timeout"], help="timeout rabbitmq")
parser.add_argument("--exchange", default=conf["exchange_direct"], help="exchange rabbitmq")
parser.add_argument("--queue", default=conf["queue1"], help="queue rabbitmq")
parser.add_argument("--init", default=True, help="resetService")
args = parser.parse_known_args()

def main():
    # Validations
    assert args[0].start <= args[0].end, "Error en tiempo final"
    # Connection
    channel = helpers.connect(args[0].user, args[0].password, args[0].host, args[0].port, args[0].timeout)
    
    # Declare
    channel.exchange_declare(exchange=args[0].exchange, exchange_type='direct')

    # Open File
    f = wave.open(args[0].wav,"rb")
    channels = f.getnchannels()
    rate = f.getframerate()
    sampwidth = f.getsampwidth()
    start = rate*args[0].start
    channels = f.getnchannels()
    size_chunk = int(rate/args[0].chunk)
    identification = helpers.identificador(args[0].name, args[0].id, args[0].type, args[0].format, rate, sampwidth, channels, size_chunk, conf["format_byte"])

    # init
    if args[0].init:
        channel.basic_publish(exchange=args[0].exchange, routing_key=args[0].queue, body="ResetService")

    # Streaming
    start = rate*args[0].start
    f.setpos(start)
    delta_time = (1 / rate) * size_chunk
    startTime = time.time()
    nextTime = startTime + delta_time
    end = rate*args[0].end
    while True:
        t = time.time()
        if t < nextTime:
            time.sleep(nextTime - t)
        sdata = f.readframes(size_chunk)  
        if sdata:
            point = f.tell()
            identification["time"] = round(((point - start) / rate ) - delta_time, 2)
            sdata_decoded = helpers.decode(sdata, identification["format_byte"])
            identification["data"] = sdata_decoded 
            channel.basic_publish(exchange=args[0].exchange, routing_key=args[0].queue, body=json.dumps(identification))
            startTime = nextTime
            nextTime = startTime + delta_time
            print("[x] Sent frame in the time: ", identification["time"], "rate: ", identification["rate"], "pos: ", point )  
            if end != 0 and point >= end:
                break
        else:
            break
    channel.close()
    f.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


