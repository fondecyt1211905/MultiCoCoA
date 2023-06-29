import cv2
import sys
import json
import os
import numpy as np
from deepface import DeepFace as dp

import config as config
import helpers as helpers
conf= config.CONFIG

#Configurations for the pipeline
exchange_in = conf["Exch_emotion"]
type_exchange_in = conf["type_exchange_direct"]
queue_in = conf["Q_emotion"]
exchange_out = conf["Exch_video_out"]
queue_out = conf["Q_video_out"]

def main():
    #Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"], conf["rabbitmq_timeout"])
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

    #Callback function
    def callback(ch, method, properties, body):
        if helpers.is_reset(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        image = np.frombuffer(helpers.encode(datos["data"], datos["format_byte"]), dtype=np.uint8)
        image = cv2.imdecode(image,cv2.IMREAD_COLOR)
        for track_id, data in datos["users"].items():
            if data["is_confirmed"] == True:
                x = data["x"]
                y = data["y"]
                w = data["width"]
                h = data["height"]
                # recortar imagen
                face = image[y:y+h, x:x+w]
                print("track_id: ",track_id, face.shape, flush=True)
                datos["users"][track_id]["emotion"] = dp.analyze(img_path=face, detector_backend="mediapipe" , actions = ['emotion'], enforce_detection=False)
                print(datos["users"][track_id]["emotion"], flush=True)
        channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(datos))
    channel.basic_consume(queue=queue_in, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
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
