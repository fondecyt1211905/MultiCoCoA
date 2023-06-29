#Import libraries
import json
import sys
import os
import math
import mediapipe as mp
import numpy as np
import cv2

import config as config
import helpers as helpers
conf= config.CONFIG

#Global elements
face_mesh = []

#Configurations for the pipeline
exchange_in = conf["Exch_in_facedirection"]
type_exchange_in = conf["type_exchange_direct"]
queue_in = conf["Q_facedirection"]
exchange_out = conf["Exch_in_lookingdirection"]
queue_out = conf["Q_lookingdirection"]

#Main function faceDirection
"""
Elementos de entrada
face: nparray correspondiente a la imagen de una cara
num: numero del usuario
frameRate: frameRate del video 
x_medium: punto x central de la imagen de la cara
y_medium: punto y central de la imagen de la cara
w: ancho de la imagen de la cara
h: alto de la imagen de la cara
alpha: valor de angulo de la camara, por defecto es 45°

Valores de salida
angles: arreglo con los angulos x,y de la cara
yaw: inclinacion del eje x
pitch: inclinacion del eje y
roll: inclinacion del eje z
landmark: arreglo de 468 puntos x,y,z en tuplas que poseen los puntos de deteccion de cara de mediapipe
"""

def create_pixel_angles(x, y, width, height, viewing_angles=(45,180)):
    angles_x = 0
    angles_y = 0
    angles_x = ((x * viewing_angles[1]) / width)
    if y < height / 2:
        angles_y = -((y * viewing_angles[0]*2 / (height / 2)) - viewing_angles[0])
    else:
        y = y - height / 2
        angles_y = -((y * viewing_angles[0] * 2 / (height / 2)) - viewing_angles[0])
        angles_x = angles_x + viewing_angles[1]
    return [ int(angles_x), int(angles_y) ]

def rotation_matrix_to_angles(rotation_matrix):
    x = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
    y = math.atan2(-rotation_matrix[2, 0], math.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2))
    z = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    return np.array([x, y, z]) * 180. / math.pi

face_coordination_in_real_world = np.array([
        [285, 528, 200],
        [285, 371, 152],
        [197, 574, 128],
        [173, 425, 108],
        [360, 574, 128],
        [391, 425, 108]
    ], dtype=np.float64)

def faceDirection(image, i, x_, y_, w_, h_):
    i = i - 1
    face = image[y_:y_ + h_, x_:x_ + w_]
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    if i >= len(face_mesh):
        face_mesh.append(mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5))
    
    results = face_mesh[i].process(face)
    h, w, _ = face.shape
    face_coordination_in_image = []
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [1, 9, 57, 130, 287, 359]:
                    x, y = int(lm.x * w), int(lm.y * h)
                    face_coordination_in_image.append([x, y])

            focal_length = 1 * w
            cam_matrix = np.array([[focal_length, 0, w / 2], [0, focal_length, h / 2], [0, 0, 1]])
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            face_coordination_in_image = np.array(face_coordination_in_image, dtype=np.float64)
            success, rotation_vec, transition_vec = cv2.solvePnP( face_coordination_in_real_world, face_coordination_in_image, cam_matrix, dist_matrix)
            rotation_matrix, jacobian = cv2.Rodrigues(rotation_vec)

        yaw, pitch, roll = rotation_matrix_to_angles(rotation_matrix)
        return yaw, pitch, roll, list(face_landmarks.landmark)
    return None, None, None, None

def main():
  #Connection
  con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"], conf["rabbitmq_timeout"])
  channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

  #Callback function
  def callback(ch, method, properties, body):
    if helpers.is_reset(body):
      face_mesh.clear()
      channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
      return
    if helpers.is_save(body):
      channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
      return
    datos = json.loads(body)
    for user, data in datos["users"].items():
      image= np.frombuffer(helpers.encode(datos["data"], datos["format_byte"]), dtype=np.uint8)
      image = cv2.imdecode(image,cv2.IMREAD_COLOR)
      x_ = data["x"]
      y_ = data["y"]
      w_ = data["width"]
      h_ = data["height"]
      center = (int(x_ + w_ / 2), int(y_ + h_ / 2))
      yaw, pitch, roll, landmark= faceDirection(image, int(user), x_, y_, w_, h_)
      datos["users"][user]["angles"]= create_pixel_angles(center[0], center[1], image.shape[1], image.shape[0])
      datos["users"][user]["yaw"]= yaw
      datos["users"][user]["pitch"]= pitch
      datos["users"][user]["roll"]= roll
      #datos["users"][user]["landmark"]= landmark
    channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(datos))
    #if len(datos["users"]) > 0:
    #  print("[x] Sent facedirection data of users ", datos["users"].keys(), " on frame ", datos["position"], flush=True)

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