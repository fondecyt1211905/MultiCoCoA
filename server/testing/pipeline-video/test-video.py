#Import libraries
import json
import sys
import os
import config.config as config
import helpers.helpers as helpers
import numpy as np
import cv2
import argparse
conf= config.CONFIG

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--user", default=conf["user"], help="usuario rabbitmq")
parser.add_argument("--password", default=conf["password"], help="password rabbitmq")
parser.add_argument("--host", default=conf["host"], help="host rabbitmq")
parser.add_argument("--port", type=int, default=conf["port"], help="port rabbitmq")
parser.add_argument("--timeout", type=int, default=conf["timeout"], help="timeout rabbitmq")
parser.add_argument("--exchange", default=conf["exchange_direct"], help="exchange rabbitmq")
parser.add_argument("--type_exchange", default="direct", help="type exchange rabbitmq")
parser.add_argument("--queue", default=conf["queue8"], help="queue rabbitmq")
parser.add_argument("--csv", type=str, default=None, help="filename .csv")
args = parser.parse_known_args()

def main():
  # Connection
  con, channel = helpers.connect(args[0].user, args[0].password, args[0].host, args[0].port, args[0].timeout)

  # Declare
  channel = helpers.declare(channel, args[0].exchange, args[0].type_exchange, args[0].queue, True)
  #Use this channel connection for userrecognition
  #channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"], conf["timeout"])
  #channel = helpers.declare(channel, conf["exchange_userr"], "fanout", conf["queue3"])

  #Callback function
  def callback(ch, method, properties, body):
    if helpers.is_reset(body):
      global buff_data
      buff_data=[]
      return
    if helpers.is_save(body):
      return
    print("*",flush=True)
    identification = json.loads(body)
    image= np.frombuffer(helpers.encode(identification["data"], identification["format_byte"]), dtype=np.uint8)
    image = cv2.imdecode(image,cv2.IMREAD_COLOR)
    if "users" in identification:   
      for user,data in identification["users"].items():
        #Print data of userrecognition
        image= cv2.rectangle(image,(data["x"],data["y"]),(data["x"]+data["width"],data["y"]+data["height"]),(255,255,255),2)
        image=cv2.putText(image, user, (data["x"]-30, data["y"]-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),2)
        image=cv2.putText(image, "x,y: "+str(int(data["x_medium"])) + " , " + str(int(data["y_medium"])), (data["x"]-30,data["y"]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),2)
        image=cv2.putText(image, "visible: "+str(data["visible"]), (data["x"]-30,data["y"]+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),2)
        
        #Print data of facedirection
        if "angles" in data:
          image=cv2.putText(image, "Angulos: " + str(round(data["angles"][0])) + " , " + str(round(data["angles"][1])), (data["x"]-30,data["y"]+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Yaw: " + str(round(data["yaw"],2)), (data["x"]-30,data["y"]+80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Pitch: " + str(round(data["pitch"],2)), (data["x"]-30,data["y"]+100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Roll: " + str(round(data["roll"],2)), (data["x"]-30,data["y"]+120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
        
        #Print data of emotion 
        if "emotion" in data: 
          image=cv2.putText(image, "Edad: " + str(data["age"]), (data["x"]-30,data["y"]+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Genero: " + str(data["gender"]), (data["x"]-30,data["y"]+80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Raza: " + str(data["race"]), (data["x"]-30,data["y"]+100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Emocion: " + str(data["emotion"]), (data["x"]-30,data["y"]+120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
        
        #Print data of pose  
        if "pose_landmarks" in data:
          for x,y,z,visibility in data["pose_landmarks"]:
            x= data["x_medium"]+2*identification["body_size"]*(x-0.5)
            if data["y_medium"] <= 320:
              y=identification["height"]/2*y
            else: 
              y= identification["height"]/2 + identification["height"]/2*y
            image= cv2.circle(image,(int(x),int(y)),4,(128,0,255),-1)
        
        #Print data of hands    
        if "hands_landmarks" in data:
          for x,y,z in data["hands_landmarks"]:
            x= data["x_medium"]+2*identification["body_size"]*(x-0.5)
            if data["y_medium"] <= 320:
              y=identification["height"]/2*y
            else: 
              y= identification["height"]/2 + identification["height"]/2*y
            image= cv2.circle(image,(int(x),int(y)),4,(128,0,255),-1)
        
        #Print data of lookinghead    
        if "looking_user" in data:
          image=cv2.putText(image, "Usuario que mira: " + str(data["looking_user"]), (data["x"]-30,data["y"]+140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Estado: " + str(data["looking_status"]), (data["x"]-30,data["y"]+160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Angulos de mirada: " + str(round(data["looking_angle"][0],2)) + " , " + str(round(data["looking_angle"][1],2)), (data["x"]-30,data["y"]+180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
          image=cv2.putText(image, "Tiempo mirando: " + str(data["looking_time"]) + " s", (data["x"]-30,data["y"]+200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
    
    #Display frame      
    cv2.imshow("Image",  cv2.resize(image,(1366,768)))
    print("[x] Frame imshow", flush=True)
    if cv2.waitKey(1) & 0xFF == ord("q"):
      return
  try:
    channel.basic_consume(queue=args[0].queue, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for file. To exit press CTRL+C', flush=True)
    channel.start_consuming()
  except KeyboardInterrupt:
      print('Interrupted', flush=True)
  finally:
      channel.close()
      cv2.destroyAllWindows()
      con.close()

if __name__ == '__main__':
  main()