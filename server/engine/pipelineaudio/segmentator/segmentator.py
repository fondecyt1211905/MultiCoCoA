import numpy as np
import sys, os
import json
import config
import helpers
conf = config.CONFIG

queue = []
new_frame = None
previous_user = None
buf = []

#Configurations for the pipeline
exchange_in = conf["Exch_filter_doa_out"]
type_exchange_in = conf["type_exchange_fanout"]
queue_in = conf["Q_segmentator"]
exchange_out = conf["Exch_segmentator_out"]
queue_out = ""

def createNewFrame(data):
    #print("----------------------NewFrame ", data["active_voice"], flush=True)
    return {
        "name": data["name"],
        "id_device": data["id_device"],
        "type": data["type"],
        "fps": data["fps"],
        "sampwidth": data["sampwidth"],
        "channels": data["channels"],
        "format_byte": data["format_byte"],
        "speaking_time": 0,
        "active_voice": data["active_voice"],
        #"direction": data["direction"],
        #"speech_count": data["speech_count"],
        "start_time": data["time"] - data["duration"]
    }

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

    def callback(ch, method, properties, body):
        global queue
        global new_frame
        global previous_user
        global buf
        if helpers.is_reset(body):
            queue = []
            buf = []
            new_frame = None
            previous_user = None
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        queue.append(datos)
        if len(queue) == 3:
            x = 1
            frame_decodificado = helpers.encode(queue[x]["data"], queue[x]["format_byte"])
            queue[x]["data"] = np.frombuffer(frame_decodificado, dtype=np.int16)
            frame_duration = round(1/(queue[x]["fps"]/queue[x]["chunk"]) * conf["pa_doa_chunks"], 2)
            previous_user = queue[x-1]["active_voice"]
            current_user = queue[x]["active_voice"]
            next_user = queue[x+1]["active_voice"]
            
            def break_frame(f, d, b):
                f["data"] = helpers.decode(b''.join(b), d["format_byte"])
                f["end_time"] = f["start_time"] + f["speaking_time"]
                channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(f))
                b = []
                f = createNewFrame(d)
                return b, f
            
            if new_frame is not None:
                #print(new_frame["active_voice"], previous_user, current_user, next_user, flush=True)
                if previous_user is None and current_user is not None:
                    buf, new_frame = break_frame(new_frame, queue[x], buf)
                elif previous_user is None and current_user is None:
                    pass
                elif previous_user is not None and current_user is None:
                    if next_user is None:
                        buf, new_frame = break_frame(new_frame, queue[x], buf)
                    else:
                        queue[x]["active_voice"] = previous_user
                elif previous_user is not None and current_user is not None:
                    if previous_user == current_user:
                        pass
                    else:
                        if next_user == current_user:
                            buf, new_frame = break_frame(new_frame, queue[x], buf)
                        else:
                            queue[x]["active_voice"] = previous_user
  
            if new_frame is None:
                new_frame = createNewFrame(queue[x])
                buf.append(queue[x]["data"])
                
            if new_frame:
                new_frame["speaking_time"]+=frame_duration
                buf.append(queue[x]["data"])

            queue.pop(0)
    
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