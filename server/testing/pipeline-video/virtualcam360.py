#Importacion de librerias
import cv2
import os
import sys
import time 
import json
import argparse
import config.config as config
import helpers.helpers as helpers
conf= config.CONFIG

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--mp4", type=argparse.FileType('rb'), required=False, help="URI de archivo VIDEO MP4")
parser.add_argument("--avi", type=argparse.FileType('rb'), required=False, help="URI de archivo VIDEO AVI")
parser.add_argument("--name", default="Camara1", help="Nombre del dispositivo, Default = Camara1")
parser.add_argument("--id", default="0000000000000001", help="Identificador, Default = 0000000000000001")
parser.add_argument("--type", default="VIDEO", help="Tipo de dispositivo, Default = VIDEO")
parser.add_argument("--format", default="ISO-8859-1", help="Tipo de dispositivo, Default = ISO-8859-1")
parser.add_argument("--start", type=int, default=0, help="Indica el segundo para iniciar lectura, Default = 0")
parser.add_argument("--end", type=int, default=0, help="Indica el segundo para finalizar lectura, Default = None")
parser.add_argument("--chunk", type=int, default=5, help="chunk")
parser.add_argument("--user", default=conf["user"], help="usuario rabbitmq")
parser.add_argument("--password", default=conf["password"], help="password rabbitmq")
parser.add_argument("--host", default=conf["host"], help="host rabbitmq")
parser.add_argument("--port", type=int, default=conf["port"], help="port rabbitmq")
parser.add_argument("--timeout", type=int, default=conf["timeout"], help="timeout rabbitmq")
parser.add_argument("--exchange", default=conf["exchange_direct"], help="exchange rabbitmq")
parser.add_argument("--queue", default=conf["queue1"], help="queue rabbitmq")
parser.add_argument("--init", default=True, help="resetService")
parser.add_argument("--distance", type=int, default=None, help="Distancia en cm de los usuarios a la camara, modificar manualmente")
parser.add_argument("--body_size", type=int, default=None, help="Ancho de imagen de los usuarios, modificar manualmente")
args = parser.parse_known_args()

def main():
    # Validations
    #assert args[0].end != None and args[0].start < args[0].end, "Error en tiempo final"

    #Connection
    channel = helpers.connect(args[0].user, args[0].password, args[0].host, args[0].port, args[0].timeout)
    channel.exchange_declare(exchange=args[0].exchange, exchange_type="direct")

    #Open File
    cap = cv2.VideoCapture('video/videofile.mp4') #Video por defecto, para introducir otro añadir el campo de mp4 o mavi
    if args[0].mp4 is not None:
        cap = cv2.VideoCapture(args[0].mp4)
    elif args[0].avi is not None:
        cap = cv2.VideoCapture(args[0].avi)

    #Obtencion de data del video
    channels = cap.get(cv2.CAP_PROP_CHANNEL)
    frameRate = int(cap.get(cv2.CAP_PROP_FPS))
    frameCount= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size_chunk = int(frameRate/args[0].chunk)

    #Generar valor de identificador
    identification = helpers.identificador(args[0].name, args[0].id, args[0].type, args[0].format, frameRate, frameCount, width, height, channels, size_chunk, conf["format_byte"])
    if args[0].distance is not None:
        identification["distance"]= args[0].distance
    else:    
        identification["distance"] = 100 
    
    if args[0].body_size is not None:
        identification["body_size"]=args[0].body_size
    else:
        identification["body_size"]= 200 

    #init
    if args[0].init:
        channel.basic_publish(exchange=args[0].exchange, routing_key=args[0].queue, body="ResetService")

    #Streaming
    if frameRate*args[0].start == 0:
        start = 0
    else:
        start = frameRate*args[0].start
    delta_time = (1 / frameRate)
    startTime = time.time()
    nextTime = startTime + delta_time
    if frameRate*args[0].end == 0:
        end = frameCount
    else:
        end = frameRate*args[0].end
    while True:
        t = time.time()
        if t < nextTime:
            time.sleep(nextTime - t)
        sucess, frame = cap.read()
        position = cap.get(cv2.CAP_PROP_POS_FRAMES)
        if sucess:
            if position >= start*frameRate and (position-1)%frameRate==0: #Envio de frames por cada segundo del programa
                identification["position"] = position
                identification["time"] = round(((position - start) / frameRate)-delta_time,2)
                is_success, im_buf_arr = cv2.imencode(".jpg", frame)
                sdata_decoded = helpers.decode(im_buf_arr.tobytes(), identification["format_byte"])
                identification["data"] = sdata_decoded

                #Publicacion de data en json hacia la queue1
                channel.basic_publish(exchange=args[0].exchange, routing_key=args[0].queue, body=json.dumps(identification))
                startTime = nextTime
                nextTime = startTime + delta_time
                print("[x] Sent frame in the time", identification["time"], "frameRate: ", identification["frameRate"], "pos: ", position )
                if position >= end:
                    break
        else:
            break
    channel.close()
    cap.release()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)