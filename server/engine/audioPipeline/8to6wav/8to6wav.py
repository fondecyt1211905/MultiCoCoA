import sys, os
#sys.path.append("../..")
import json
import numpy as np
#import config.config as config
#import helpers.helpers as helpers
import config
import helpers
conf = config.CONFIG
mem = None

#Configurations for the pipeline
exchange_in = conf["8to6wav_in_ex"]
type_exchange_in = conf["8to6wav_in_ex_type"]
queue_in = conf["8to6wav_in_q"]
exchange_out = conf["8to6wav_out_ex"]
queue_out = conf["8to6wav_out_q"]

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)
    arr = np.array((0,1,2,3,4,5,6,7))

    def callback(ch, method, properties, body):
        global mem
        if helpers.is_reset(body):
            mem = None
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        try:    
            datos = json.loads(body)
        except json.decoder.JSONDecodeError as e:
            print(e, flush=True)
            return
        datos_encodificados = helpers.encode(datos["data"], datos["format_byte"])
       
        data = np.frombuffer(datos_encodificados, dtype=np.int16)
        data = np.resize(data,(int(len(data)/8),8))
        k = 2
        filterSTD = np.argpartition(np.std(data, axis=0), k)
        filterchannel = np.sort(filterSTD[:k])
        if np.abs(filterchannel[0] - filterchannel[1]) > 1:
            if not mem is None:
                if filterchannel[0] in mem or filterchannel[1] in mem:
                    filterchannel = mem
        
        chs = np.concatenate((arr[filterchannel[1]+1:8],arr[0:filterchannel[0]]))
        data = np.ravel(data[:,chs])
        data_bytes = data.tobytes()
        datos["data"] = helpers.decode(data_bytes, datos["format_byte"])
        datos["channels"] = 6 # de 8 a 6 canales
        channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(datos))

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
