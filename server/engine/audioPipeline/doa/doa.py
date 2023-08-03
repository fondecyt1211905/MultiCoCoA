import sys, os
#sys.path.append("../..")
import json
import collections
#import config.config as config
#import helpers.helpers as helpers
import config
import helpers
import get_direction as gd
import numpy as np
conf = config.CONFIG

queue = collections.deque(maxlen=conf["doa_number_of_chunks"])

#Configurations for the pipeline
exchange_in = conf["doa_in_ex"]
type_exchange_in = conf["doa_in_ex_type"]
queue_in = conf["doa_in_q"]
exchange_out = conf["doa_out_ex"]
queue_out = conf["doa_out_q"]

def dir_to_user(direction, numUsers):
    user = None
    numBins = 0
    if numUsers in [5, 6]:
        numBins = 6
    elif numUsers in [3, 4]:
        numBins = 4
    elif numUsers in [2]:
        numBins = 2
    angle = 360 / numBins
    bins = [(angle * i) for i in range(numBins + 1)]
    bins.append(360)
    for i in range(len(bins) - 1):
        if direction > bins[i] and direction <= bins[i + 1]:
            user = i + 1
            break
    return user

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)
    
    def callback(ch, method, properties, body):
        global queue
        if helpers.is_reset(body):
            queue = collections.deque(maxlen=conf["doa_number_of_chunks"])
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        queue.append(datos)
        
        if len(queue) == conf["doa_number_of_chunks"]:
            
            datos["direction"] = ""
            datos["active_voice"] = ""
            dir_, buf_ = gd.get_direction([np.frombuffer(helpers.encode(x["data"], datos["format_byte"]), dtype=np.int16) for x in queue], datos["channels"], datos["fps"])
            user = dir_to_user(dir_, datos["numUsers"])
            datos["Voice"] = [x["Voice"] for x in queue]
            datos["speech_count"] = sum(datos["Voice"])
            if datos["speech_count"] > conf["doa_chunk_threshold"]:
                datos["active_voice"] = user
            else:
                datos["active_voice"] = None
            datos["direction"] = dir_
            datos["data"] = helpers.decode(buf_, datos["format_byte"])
            datos["time"] = queue[0]["time"]
            datos["duration"] = (1 / (datos["fps"] / datos["chunk"])) * conf["doa_number_of_chunks"]
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(datos))
            queue.clear()
           
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
