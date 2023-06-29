import sys, os
import json
import config
import helpers
import collections
conf = config.CONFIG

queue = []
active_voices = []

#Configurations for the pipeline
exchange_in = conf["Exch_in_filter_doa"]
type_exchange_in = conf["type_exchange_direct"]
queue_in = conf["Q_filter_doa"]
exchange_out = conf["Exch_filter_doa_out"]
queue_out = ""

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)
    
    def callback(ch, method, properties, body):
        global queue
        global active_voices
        if helpers.is_reset(body):
            queue = []
            active_voices = []
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        queue.append(datos)
        active_voices.append(datos["active_voice"])
        if len(queue) == conf["pa_filter_doa_chunks"]:
            x = int(len(queue)/2)
            middle = active_voices[x]
            count = collections.Counter(active_voices).most_common(conf["pa_filter_doa_chunks"])
            min = 0
            common = []
            for c, n in count:
                if n >= min:
                    common.append(c)
                    min = n
            output = middle
            if len(common) != 0 and middle is not None:
                if middle in common:
                    output = middle
                else: 
                    if len(common) == 1:
                        output = common[0]
                    else:
                        output = None
            #print(middle, output, common, active_voices, datos["time"], flush=True, sep="\t")
            queue[x]["active_voice"] = output
            queue[x]["active_voice_c"] = common[0]
            queue[x]["active_voice_m"] = middle
            queue[x]["time"] = queue[x]["time"] - queue[x]["duration"]
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(queue[x]))
            queue.pop(0)
            active_voices.pop(0)
            
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
