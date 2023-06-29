#Import libraries
import json
import sys
import os
import cv2
import numpy as np
import config as config
import helpers as helpers
conf= config.CONFIG

#Global elements
users_data={}

#Configurations for the pipeline
exchange_in = conf["Exch_in_lookingdirection"]
type_exchange_in = conf["type_exchange_direct"]
queue_in = conf["Q_lookingdirection"]
exchange_out = conf["Exch_emotion"]
queue_out = conf["Q_emotion"]

radio = conf["pv_radio"]

def create_vector(angles):
    return np.array([
        radio * np.cos(np.radians(angles[0])), 
        radio * np.sin(np.radians(angles[0])),	
        radio * np.tan(np.radians(angles[1])),
    ])

def create_vector_focus(yaw, pitch, angles_y_source, vector_source):
    lx = radio + radio* np.cos(np.radians(2*pitch))
    ly = radio* np.sin(np.radians(2*pitch))
    h = np.sqrt(lx**2 + ly**2)
    lz = h * np.tan(np.radians(angles_y_source-yaw))

    return np.array([
        -vector_source[0] * np.cos(np.radians(2*pitch)) - -vector_source[1] * np.sin(np.radians(2*pitch)),
        -vector_source[0] * np.sin(np.radians(2*pitch)) + -vector_source[1] * np.cos(np.radians(2*pitch)),
        vector_source[2] - lz
    ])

def create_angles(vector):
    aux = np.array([
        np.degrees(np.arcsin(vector[0] / radio)),
        np.degrees(np.arccos(vector[0] / radio)),
        np.degrees(np.arcsin(vector[1] / radio)),
        np.degrees(np.arctan(vector[2] / radio)),
    ])
    value = 0
    if aux[0] >= 0 and aux[2] >= 0:
        value = aux[2]
    if aux[0] > 0 and aux[2] < 0:
        value = 360 + aux[2]
    if (aux[0] < 0 and aux[2] < 0) or (aux[0] < 0 and aux[2] > 0):
        value = 180 - aux[2]
    return np.array([
        int(value),
        int(aux[3])
    ])

def create_angles_pixel(angles_x, angles_y, width, height, viewing_angles=(45,180)):
    y = ((angles_y * (height/2) / (viewing_angles[0]*2)) - (height/4) ) * -1
    if angles_x > viewing_angles[1]:
        angles_x = angles_x - viewing_angles[1]
        y = y + height/2
    x = angles_x * width / viewing_angles[1]
    if x >= width:
        x = width
    if y >= height:
        y = height
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    return np.array([ int(x), int(y)])

def distance(vertor_target, vector_focus):
    return np.sqrt(
        (vector_focus[0] - vertor_target[0])**2 +
        (vector_focus[1] - vertor_target[1])**2 +
        (vector_focus[2] - vertor_target[2])**2
    )

def main():
  #Connection
  con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"], conf["rabbitmq_timeout"])
  channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

  #Callback function
  def callback(ch, method, properties, body):
    if helpers.is_reset(body):
      users_data.clear()
      channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
      return
    if helpers.is_save(body):
      channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
      return
    datos = json.loads(body)
    image = np.frombuffer(helpers.encode(datos["data"], datos["format_byte"]), dtype=np.uint8)
    image = cv2.imdecode(image,cv2.IMREAD_COLOR)
    for user, data in datos["users"].items():
      try:
        vector = create_vector(data["angles"])
        focus = create_vector_focus(data['yaw'], data['pitch'], data['angles'][1], vector)
        angles_focus = create_angles(focus)
        pixel_focus = create_angles_pixel(angles_focus[0], angles_focus[1], image.shape[1], image.shape[0])
        datos["users"][user]["vector"] = vector.tolist()
        datos["users"][user]["focus"] = focus.tolist()
        datos["users"][user]["pixel_focus"] = pixel_focus.tolist()
      except TypeError:
        datos["users"][user]["vector"] = None
        datos["users"][user]["focus"] = None
        datos["users"][user]["focus"] = None
    # recorrer pares de usuarios y calcular distancia entre vectores
    for i, d1 in datos["users"].items():
      min_distance = None
      user_min_distance = None
      for j, d2 in datos["users"].items():
          if i != j:
            if d1["focus"] is not None and d2["focus"] is not None:
              if min_distance is None or distance(d1["focus"], d2["vector"]) < min_distance:
                min_distance = distance(d1["focus"], d2["vector"])
                user_min_distance = j
      datos["users"][i]["distance"] = min_distance
      datos["users"][i]["user_min_distance"] = user_min_distance
    
    channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(datos))
    #if len(datos["users"]) > 0:
    #  print("[x] Sent lookingposition data of users ", datos["users"].keys(), " on frame ", datos["position"], flush=True)
  
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