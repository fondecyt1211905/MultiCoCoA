# Abrir un archivo de audio .wav
import numpy as np
import sys, os
#sys.path.append("../..")
import json
from webrtcvad import Vad
#import config.config as config
#import helpers.helpers as helpers
import config
import helpers
conf = config.CONFIG
vad = Vad(conf["vad_mode"])

#Configurations for the pipeline
exchange_in = conf["vad_in_ex"]
type_exchange_in = conf["vad_in_ex_type"]
queue_in = conf["vad_in_q"]
exchange_out = conf["vad_out_ex"]
queue_out = conf["vad_out_q"]

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

    def callback(ch, method, properties, body):
        global vad
        if helpers.is_reset(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        frame_decodificado = helpers.encode(datos["data"], datos["format_byte"])
        data = np.frombuffer(frame_decodificado, dtype=np.int16)
        active = vad.is_speech(data, datos["fps"])
        datos["Voice"] = active
        datos["data"] = helpers.decode(frame_decodificado, datos["format_byte"])
        channel.basic_publish(exchange= exchange_out, routing_key=queue_out, body=json.dumps(datos))
        
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
