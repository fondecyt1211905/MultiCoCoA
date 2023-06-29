import sys, os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sys.path.append(''.join((os.getcwd(), '/server/engine/pipelineaudio/config')))
sys.path.append(''.join((os.getcwd(), '/server/engine/pipelineaudio/helpers')))
import config # No es error
import helpers # No es error
import argparse
conf = config.CONFIG
buff_data = []

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--user", default=conf["user"], help="usuario rabbitmq")
parser.add_argument("--password", default=conf["password"], help="password rabbitmq")
parser.add_argument("--host", default=conf["host"], help="host rabbitmq")
parser.add_argument("--port", type=int, default=conf["port"], help="port rabbitmq")
parser.add_argument("--timeout", type=int, default=conf["timeout"], help="timeout rabbitmq")
parser.add_argument("--exchange", default=conf["exchange_doa"], help="exchange rabbitmq")
parser.add_argument("--queue", default=conf["queue7"], help="queue rabbitmq")
args = parser.parse_known_args()

def main():
    # Connection
    channel = helpers.connect(args[0].user, args[0].password, args[0].host, args[0].port, args[0].timeout)
    # Declare
    channel = helpers.declare(channel, args[0].exchange, "fanout", args[0].queue)
    
    def callback(ch, method, properties, body):
        global buff_data
        if helpers.is_reset(body):
            buff_data = []
        else:
            datos = json.loads(body)
            frame_decodificado = helpers.encode(datos["data"], datos["format_byte"])
            datos["data"] = np.frombuffer(frame_decodificado, dtype=np.int16)
            buff_data.append(datos)
            print( 
                "active_voice:", datos["active_voice"], 
                "dirección: ", datos["direction"], 
                "speech_count:", datos["speech_count"],
                "time", datos["time"], flush=True)

    channel.basic_consume(queue=args[0].queue, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        
        signal_ch0 = np.concatenate([x["data"] for x in buff_data])[0::6]
        #print(len(signal_ch0))
        Time = np.linspace(0, len(signal_ch0) / buff_data[0]["rate"], num=len(signal_ch0))
        users = [x["active_voice"] for x in buff_data]
        dir_ = [x["direction"] for x in buff_data]
        Time_2 = np.linspace(0, len(signal_ch0) / buff_data[0]["rate"], num=len(buff_data))

        #print(len(Time))
        df_wav = pd.DataFrame({
            "time": Time,
            "sample": signal_ch0
        })
        df_data = pd.DataFrame({
            "time": Time_2,
            "users": users,
            "dir": dir_
        })
        fig, ax1 = plt.subplots(figsize=(20,5))
        ax2 = ax1.twinx()
        plt.title("Signal Wave...")
        sns.lineplot(data = df_wav, x = "time", y = "sample", ax=ax1)
        sns.scatterplot(data = df_data, x = "time", y = "dir", hue="users", palette="tab10", ax=ax2)
        ax2.set_ylim(0, 360)
        plt.xlim((Time[0], Time[-1]))
        plt.show()
        print(Time_2)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
