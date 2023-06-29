import cv2
import json
import mediapipe as mp
import numpy as np
import sys
import os
mp_pose = mp.solutions.pose

import config as config
import helpers as helpers
conf= config.CONFIG

#Global elements
users_data={}

#Main function
#Se recibe la imagen de un usuario y el numero de este para encontrar los puntos del cuerpo del usuario utilizado mediapipe
#Marcar notbelow=False si se desean obtener todos los puntos del cuerpo y notbelow=True si se desean obtener solo los puntos superiores del cuerpo
def pose(image,num,notbelow=False):
  lista=[]
  if num not in users_data:
    users_data[num]=[]
  with mp_pose.Pose(
      static_image_mode=True,
      model_complexity=2,
      min_detection_confidence=0.5,
      min_tracking_confidence = 0.5) as pose:
    # Convert the BGR image to RGB before processing.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks is not None:
      contador=0
      for deteccion in results.pose_landmarks.landmark:
        if notbelow and contador > 22:
          break
        x= deteccion.x
        y=deteccion.y
        z= deteccion.z
        visibility= deteccion.visibility
        if y <= 1.0:
          lista.append((x,y,z,visibility))
        contador+=1
      users_data[num]=lista
    else:
      users_data[num]=[]
  return users_data[num]


def main():
  #Connection
  channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"], conf["timeout"])
  channel = helpers.declare(channel, conf["exchange_userr"], "fanout", conf["queue7"])

  #Callback function
  def callback(ch, method, properties, body):
    global buff_data
    if helpers.is_reset(body):
      users_data.clear()
      buff_data = []
    else:
        datos = json.loads(body)
        #buff_data.append(datos)
        identification=datos
        for user, data in identification["users"].items():
          image= np.frombuffer(helpers.encode(identification["data"], identification["format_byte"]), dtype=np.uint8)
          image = cv2.imdecode(image,cv2.IMREAD_COLOR)
          if data["y_medium"] <= 320:
            body = image[0:int(identification["height"]/2),max(0,int(data["x_medium"]-identification["body_size"])):min(int(data["x_medium"])+identification["body_size"], int(identification["width"]))]
          else:
            body = image[int(identification["height"]/2):int(identification["height"]),max(0,int(data["x_medium"]-identification["body_size"])):min(int(data["x_medium"]+identification["body_size"]), int(identification["width"]))]
          pose_landmarks= pose(body,user,notbelow=True)
          identification["users"][user]["pose_landmarks"]= pose_landmarks
        channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue8"], body=json.dumps(identification))
        if len(identification["users"]) > 0:
          print("[x] Sent pose data of users ", identification["users"].keys(), " on frame ", identification["position"], flush=True)
  
  channel.basic_consume(queue=conf["queue7"], on_message_callback=callback, auto_ack=True)
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