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

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--user", default=conf["user"], help="usuario rabbitmq")
parser.add_argument("--password", default=conf["password"], help="password rabbitmq")
parser.add_argument("--host", default=conf["host"], help="host rabbitmq")
parser.add_argument("--port", type=int, default=conf["port"], help="port rabbitmq")
parser.add_argument("--timeout", type=int, default=conf["timeout"], help="timeout rabbitmq")
parser.add_argument("--exchange", default=conf["exchange_seg"], help="exchange rabbitmq")
parser.add_argument("--queue", default=conf["queue6"], help="queue rabbitmq")
parser.add_argument("--csv", type=str, default=None, help="filename .csv")
parser.add_argument("--chart", type=bool, default=False, help="chart")
parser.add_argument("--save", type=bool, default=False, help="save wav")
args = parser.parse_known_args()

buff_data = []
def main():
    # Connection
    channel = helpers.connect(args[0].user, args[0].password, args[0].host, args[0].port, args[0].timeout)
    # Declare
    channel = helpers.declare(channel, args[0].exchange, "fanout", args[0].queue)
    
    if args[0].csv != None and not helpers.valid_file(args[0].csv):
        raise argparse.ArgumentTypeError('File must have a csv extension')

    def callback(ch, method, properties, body):
        global buff_data
        if helpers.is_reset(body):
            buff_data = []
        else:
            datos = json.loads(body)
            frame_decodificado = helpers.encode(datos["data"], datos["format_byte"])
            if datos["active_voice"] is None:
                datos["data"] = np.zeros(np.frombuffer(frame_decodificado, dtype=np.int16).shape)
            else:
                datos["data"] = np.frombuffer(frame_decodificado, dtype=np.int16)
            buff_data.append(datos)
            print("active_voice:", datos["active_voice"], flush=True)

    channel.basic_consume(queue=args[0].queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        #print(buff_data)
        if args[0].csv != None and helpers.valid_file(args[0].csv):
            df = pd.DataFrame.from_dict(buff_data)
            df.to_csv(args[0].csv, sep=";")
        
        if args[0].chart == True:
            signal_ch0 = np.concatenate([x["data"] for x in buff_data])[0::6]
            Time = np.linspace(0, len(signal_ch0) / buff_data[0]["rate"], num=len(signal_ch0))

            color=["lightcoral", "darkorange", "khaki", "lightgreen", "darkcyan", "cornflowerblue"]
            #users = list(set([x["active_voice"] for x in buff_data]))
            info = {}
            for u in buff_data:
                if u["active_voice"] is not None:
                    if u["active_voice"] not in info.keys():
                        info[u["active_voice"]] = []
                    info[u["active_voice"]].append((u["start_time"],u["speaking_time"]))

            print(info)
            df_wav = pd.DataFrame({
                "time": Time,
                "sample": signal_ch0
            })
            
            fig, ax1 = plt.subplots(figsize=(20,5))
            ax2 = ax1.twinx()
            plt.title("Signal Wave...")
            sns.lineplot(data = df_wav, x = "time", y = "sample", color='lightsteelblue', ax=ax1 )
            #sns.scatterplot(data = df_data, x = "time", y = "dir", hue="users", palette="tab10", ax=ax2)
            for key, value in info.items():
                ax2.broken_barh(value, (((10*key)-9), 8), facecolors=color[key-1])
            ax2.set_ylim(0, 60)
            plt.xlim((Time[0], Time[-1]))
            plt.show()
        
        if args[0].save == True:
            import wave
            c=0
            for x in buff_data:
                if x["active_voice"] != None:
                    name = str(c) + "-" + str(x["active_voice"]) + ".wav"
                    with wave.open(name, "w") as f:
                        # 2 Channels.
                        f.setnchannels(x["channels"])
                        # 2 bytes per sample.
                        f.setsampwidth(2)
                        f.setframerate(x["rate"])
                        f.writeframes(x["data"].tobytes())
                    c+=1
                    print(name)

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
