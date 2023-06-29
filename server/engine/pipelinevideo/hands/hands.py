import cv2
import json
import mediapipe as mp
import numpy as np
import sys
import os
mp_hands = mp.solutions.hands

import config as config
import helpers as helpers
conf= config.CONFIG

#Global elements
users_data={}

#Main function hands
#Se recibe la imagen y numero de usuario para detectar los puntos de sus manos
def hands(image,num):
  lista=[]
  if num not in users_data:
    users_data[num]=[]
  with mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=2,
      min_detection_confidence=0.5) as hands:
    # Convert the BGR image to RGB before processing.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks is not None:
      for deteccion in results.multi_hand_landmarks:
        for points in deteccion.landmark:
          x= points.x
          y=  points.y
          z= points.z 
          lista.append((x,y,z))
      users_data[num]=lista
    else:
      users_data[num]=[]
  return users_data[num]


def main():
  #Connection
  channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"], conf["timeout"])
  channel = helpers.declare(channel, conf["exchange_userr"], "fanout", conf["queue9"])

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
        body_size=160
        for user, data in identification["users"].items():
          image= np.frombuffer(helpers.encode(identification["data"], identification["format_byte"]), dtype=np.uint8)
          image = cv2.imdecode(image,cv2.IMREAD_COLOR)
          if data["y_medium"] <= 320:
            body = image[0:int(identification["height"]/2),max(0,int(data["x_medium"]-identification["body_size"])):min(int(data["x_medium"]+identification["body_size"]), int(identification["width"]))]
          else:
            body = image[int(identification["height"]/2):int(identification["height"]),max(0,int(data["x_medium"]-identification["body_size"])):min(int(data["x_medium"]+identification["body_size"]), int(identification["width"]))]
          hands_landmarks= hands(body,user)
          identification["users"][user]["hands_landmarks"]= hands_landmarks
        channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue10"], body=json.dumps(identification))
        if len(identification["users"]) > 0:
          print("[x] Sent hands data of users ", identification["users"].keys(), " on frame ", identification["position"], flush=True)
  
  channel.basic_consume(queue=conf["queue9"], on_message_callback=callback, auto_ack=True)
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