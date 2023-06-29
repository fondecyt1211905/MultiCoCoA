# Abrir un archivo de audio .wav
import os, wave, time, json
import database.directdb as directdb
import utils.config as config
import utils.helpers as helpers
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = conf["Exch_analysis"]
type_exchange_in = conf["type_exchange_direct"]
queue_in = conf["Q_audio"]
exchange_out = conf["Exch_in_8to6"]
queue_out = conf["Q_8to6"]
def AudioService():

    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"], conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

    def callback(ch, method, properties, data):
        data = json.loads(data)
        idAnalysis = data["id"]
        filename = data["filename"]
        # establecemos la conexión con la base de datos MongoDB
        result = directdb.getAnalysis(idAnalysis)

        print("idAct: ", result.get("id_activity"), "start: ", result.get("start"), "end: ", result.get("end"), flush=True)
        # send message to reset service
        channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body="ResetService")

        # Open File
        file = os.path.join(os.getcwd(), "data", str(result.get("id_activity")), filename)
        if os.path.exists(file):
            f = wave.open(file,"rb")
            channels = f.getnchannels()
            fps = f.getframerate()
            sampwidth = f.getsampwidth()
            size_chunk = int(fps/conf["pa_chunk"])
            identification = helpers.menssage(
                name=conf["pa_name"],
                id_device=idAnalysis,
                tipo="AUDIO",
                fps=fps,
                sampwidth = sampwidth,
                channels = channels,
                chunk = size_chunk, 
                format_byte = conf["pa_format_byte"]
            )
            print("Process", idAnalysis, filename, flush=True)
            
            # Streaming
            start = fps*result.get("start")
            f.setpos(start)
            delta_time = (1 / fps) * size_chunk
            startTime = time.time()
            nextTime = startTime + delta_time
            if result.get("end") != None:
                end = fps*result.get("end")
            else:
                end = 0

            while True:
                t = time.time()
                if t < nextTime:
                    time.sleep(nextTime - t)
                sdata = f.readframes(size_chunk)  
                if sdata:
                    point = f.tell()
                    identification["time"] = round(((point - start) / fps ) - delta_time, 2)
                    sdata_decoded = helpers.decode(sdata, identification["format_byte"])
                    identification["data"] = sdata_decoded 
                    channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(identification))
                    startTime = nextTime
                    nextTime = startTime + delta_time
                    #print("[x] Sent frame in the time: ", identification["time"], "rate: ", identification["rate"], "pos: ", point )  
                    if end != 0 and point >= end:
                        break
                else:
                    break
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body="SaveService")
            
            f.close()
            print("Process", idAnalysis, filename, "OK", flush=True)
        else:
            print("The file does not exist at the specified path",flush=True) 

    try:
        channel.basic_consume(queue=queue_in, on_message_callback=callback, auto_ack=True)
    
        print(' [*] Waiting for file. To exit press CTRL+C', flush=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted', flush=True)
    finally:
        channel.close()
        con.close()

if __name__ == '__main__':
    AudioService()