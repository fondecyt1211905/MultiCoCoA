# import requests, os, json
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import json
import config
import helpers
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = conf["vdf_in_ex"]
type_exchange_in = conf["vdf_in_ex_type"]
queue_in = conf["vdf_in_q"]
name_indicator = conf["vdf_name_indicator"]

def VadDoa():
    buff_data = []
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"], conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

    def callback(ch, method, properties, body):
        if helpers.is_reset(body):
            return
        if helpers.is_save(body):
            return
        datos = json.loads(body)
        features = {
            "active_voice": datos["active_voice"],
            "active_voice_c": datos["active_voice_c"],
            "active_voice_m": datos["active_voice_m"],
            "direction": datos["direction"],
            "speech_count": datos["speech_count"],
            "Voice": datos["Voice"],
        }
        start = datos["time"],
        end = datos["time"] + datos["duration"],
        helpers.send_post(
            host=conf["host_backend"],
            nameIndicator=name_indicator,
            data = helpers.indicator_measure(datos["id_device"],features,start[0],end[0])
        )
        # frame_decodificado = helpers.encode(datos["data"], datos["format_byte"])
        # if datos["active_voice"] is None:
        #     datos["data"] = np.zeros(np.frombuffer(frame_decodificado, dtype=np.int16).shape)
        # else:
        #     datos["data"] = np.frombuffer(frame_decodificado, dtype=np.int16)
        # buff_data.append(datos)
        #print("active_voice:", datos["active_voice"], flush=True)
    try:
        channel.basic_consume(queue=queue_in, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted', flush=True)
        channel.close()
        con.close()

if __name__ == '__main__':
    VadDoa()
