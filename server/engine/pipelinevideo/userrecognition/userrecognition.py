#import libraries
import cv2
from deepface.detectors import FaceDetector
from deep_sort_realtime.deepsort_tracker import DeepSort
import json
import numpy as np
import sys
import os

import config as config
import helpers as helpers
conf= config.CONFIG

#Global elements
detector_name=conf["pv_detector_name"] #change model name to get diferents results: "opencv", "ssd", "dlib", "mtcnn", "retinaface" or "mediapipe"
detector = FaceDetector.build_model(detector_name)
users= dict() #Memory of all users

#Configurations for the pipeline
exchange_in = conf["Exch_in_userr"]
type_exchange_in = conf["type_exchange_direct"]
queue_in = conf["Q_userR"]
exchange_out = conf["Exch_in_facedirection"]
queue_out = conf["Q_facedirection"]

#Main function userRecognition
"""
Elementos de Entrada
img= imagen de un frame en arreglo np.array
detector = Modelo de deteccion de deepface, por defecto es mediapipe en el archivo conf
detector_name = nombre del modelo de deteccion entre 6 posibles, por defecto es mediapipe en el archivo conf
contador= numero del frame actual

Elementos de salida
image_data= diccionario cuyas keys equivalen al numero de usuario (desde 1 hasta la cantidad maxima) y con su valor una lista de tuplas con los siguientes elementos
-face: np array correspondiente a la imagen de la cara detectada
-x: punto x correspondiente a la esquina superior izquierda de la cara detectada
-y: punto y correspondiente a la esquina superior izquierda de la cara detectada
-w: ancho de la imagen de la cara detectada
-h: alto de la imagen de la cara detectada
-x_medium: punto x del centro de la cara detectada
-y_medium: punto y del centro de la cara detectada
-frame_position: valor int del frame correspondiente
-visible: valor booleano que indica si la cara fue detectada o no. En caso de no ser detectada, es false y la cara corresponde al del último frame donde si se encontro la cara
"""

def userRecognition(image, detector, detector_name, tracker, position):
  faces = FaceDetector.detect_faces(detector, detector_name, image)
  bbs = []
  for obj in faces:
    if len(obj) == 2:
      b, region = obj
      a = 0
    if len(obj) == 3:
      b, region, a = obj
    x_,y_,w_,h_= region
    hipotenusa = np.sqrt((w_**2) + (h_**2))
    bbs.append(([x_, y_, w_, h_], a, "face", hipotenusa))
  
  # ordenar por hipotenusa
  bbs.sort(key=lambda tup: tup[3], reverse=True)
  bbs = bbs[:6]

  tracks = tracker.update_tracks(bbs, frame=image)
  users_frame=dict()
  for track in tracks:
    track_id = int(track.track_id)
    users_frame[track_id]=dict()
    users_frame[track_id]["x"] = int(track.to_tlwh()[0])
    users_frame[track_id]["y"] = int(track.to_tlwh()[1])
    users_frame[track_id]["width"] = int(track.to_tlwh()[2])
    users_frame[track_id]["height"] = int(track.to_tlwh()[3])
    users_frame[track_id]["is_tentative"] = track.is_tentative()
    users_frame[track_id]["is_confirmed"] = track.is_confirmed()
    users_frame[track_id]["position"] = position
  return users_frame

def main():
  #Connection
  con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"], conf["rabbitmq_timeout"])
  channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

  tracker = DeepSort(max_age=30, max_iou_distance=1.3, max_cosine_distance=0.2, n_init=5)

  #Callback function
  def callback(ch, method, properties, body):
    if helpers.is_reset(body):
      users.clear()
      channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
      return
    if helpers.is_save(body):
      channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
      return
    
    datos = json.loads(body)
    #Extract image and decode to use on userRecognition function
    image= np.frombuffer(helpers.encode(datos["data"], datos["format_byte"]), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    datos["users"]=userRecognition(image, detector, detector_name, tracker, int(datos["position"]))

    #Publishing info to exchange_userr
    channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(datos))
    #if(len(datos["users"])> 0):
    #  print("[x] Sent userrecognition data of users ", datos["users"].keys(), " on frame ", datos["position"], flush=True)

  channel.basic_consume(queue=queue_in, on_message_callback=callback, auto_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C',flush=True)
  channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)