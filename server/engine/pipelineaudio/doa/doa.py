import sys, os
import json
import collections
import config
import helpers
import get_direction as gd
import numpy as np
conf = config.CONFIG

queue = collections.deque(maxlen=conf["pa_doa_chunks"])

#Configurations for the pipeline
exchange_in = conf["Exch_in_doa"]
type_exchange_in = conf["type_exchange_direct"]
queue_in = conf["Q_doa"]
exchange_out = conf["Exch_in_filter_doa"]
queue_out = conf["Q_filter_doa"]

def dir_to_user(dir_, channels):
    user = None
    if channels == 6:
        if dir_ > 0 and dir_ <= 60:
            user=1
        elif dir_> 60 and dir_ <= 120:
            user=2
        elif dir_> 120 and dir_ <= 180:
            user=3
        elif dir_> 180 and dir_ <= 240:
            user=4
        elif dir_> 240 and dir_ <= 300:
            user=5
        elif dir_> 300 and dir_ <= 360:
            user=6
    elif channels == 4:
        if dir_ > 0 and dir_ <= 90:
            user=1
        elif dir_> 90 and dir_ <= 180:
            user=2
        elif dir_> 180 and dir_ <= 270:
            user=3
        elif dir_> 270 and dir_ <= 360:
            user=4
    return user

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)
    
    def callback(ch, method, properties, body):
        global queue
        if helpers.is_reset(body):
            queue = collections.deque(maxlen=conf["pa_doa_chunks"])
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        queue.append(datos)
        
        if len(queue) == conf["pa_doa_chunks"]:
            
            datos["direction"] = ""
            datos["active_voice"] = ""
            dir_, buf_ = gd.get_direction([np.frombuffer(helpers.encode(x["data"], datos["format_byte"]), dtype=np.int16) for x in queue], datos["channels"], datos["fps"])
            user = dir_to_user(dir_, datos["channels"])
            datos["Voice"] = [x["Voice"] for x in queue]
            datos["speech_count"] = sum(datos["Voice"])
            if datos["speech_count"] > conf["pa_doa_chunks_s"]:
                datos["active_voice"] = user
            else:
                datos["active_voice"] = None
            datos["direction"] = dir_
            datos["data"] = helpers.decode(buf_, datos["format_byte"])
            datos["time"] = queue[0]["time"]
            datos["duration"] = (1 / (datos["fps"] / datos["chunk"])) * conf["pa_doa_chunks"]
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
