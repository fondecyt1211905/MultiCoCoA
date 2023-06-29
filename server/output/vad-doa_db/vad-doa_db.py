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
exchange_in = conf["Exch_filter_doa_out"]
type_exchange_in = conf["type_exchange_fanout"]
queue_in = conf["Q_vad_doa_db"]

# # Flags
# parser = argparse.ArgumentParser()
# parser.add_argument("--user", default=conf["user_R"], help="usuario rabbitmq")
# parser.add_argument("--password", default=conf["password_R"], help="password rabbitmq")
# parser.add_argument("--host", default=conf["host_R"], help="host rabbitmq")
# parser.add_argument("--port", type=int, default=conf["port_R"], help="port rabbitmq")
# parser.add_argument("--timeout", type=int, default=conf["timeout"], help="timeout rabbitmq")
# parser.add_argument("--exchange", default=conf["exchange_seg"], help="exchange rabbitmq")
# parser.add_argument("--queue", default=conf["queue6"], help="queue rabbitmq")
# parser.add_argument("--csv", type=bool, default=True, help="filename .csv")
# parser.add_argument("--chart", type=bool, default=True, help="chart")
# parser.add_argument("--save", type=bool, default=True, help="save wav")
# args = parser.parse_known_args()

# def save(buff_data):
#     if len(buff_data) > 0 and buff_data[0]["id_device"] == buff_data[-1]["id_device"]:
#         id_process = buff_data[-1]["id_device"]
#         filename = "vadDoa.csv"

#         df = pd.DataFrame.from_dict(buff_data)
#         df.to_csv("vadDoa.csv", sep=";")

#         helpers.send_file(conf["host_backend"], id_process, filename)

#         filename = 'vadDoa.png'
        
#         signal_ch0 = np.concatenate([x["data"] for x in buff_data])[0::6]
#         Time = np.linspace(0, len(signal_ch0) / buff_data[0]["rate"], num=len(signal_ch0))
#         color=["lightcoral", "darkorange", "khaki", "lightgreen", "darkcyan", "cornflowerblue"]
#         info = {}
#         for u in buff_data:
#             if u["active_voice"] is not None:
#                 if u["active_voice"] not in info.keys():
#                     info[u["active_voice"]] = []
#                 info[u["active_voice"]].append((u["start_time"],u["speaking_time"]))
#         df_wav = pd.DataFrame({
#             "time": Time,
#             "sample": signal_ch0
#         })
#         fig, ax1 = plt.subplots(figsize=(20,5))
#         ax2 = ax1.twinx()
#         plt.title("Signal Wave...")
#         sns.lineplot(data = df_wav, x = "time", y = "sample", color='lightsteelblue', ax=ax1 )
#         for key, value in info.items():
#             ax2.broken_barh(value, (((10*key)-9), 8), facecolors=color[key-1])
#         ax2.set_ylim(0, 60)
#         plt.xlim((Time[0], Time[-1]))
#         plt.savefig(filename)

#         helpers.send_file(conf["host_backend"], id_process, filename)

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
            nameIndicator="vad-doa",
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
