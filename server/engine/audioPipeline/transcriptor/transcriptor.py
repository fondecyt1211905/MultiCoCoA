import json
import wave
import gooogle as gooogle
#import voskRecognition as vosk
#import sphinx as sphinx
import numpy as np
import sys, os
import config
import helpers
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = conf["transcriptor_in_ex"]
type_exchange_in = conf["transcriptor_in_ex_type"]
queue_in = conf["transcriptor_in_q"]
exchange_out = conf["transcriptor_out_ex"]
queue_out = conf["transcriptor_out_q"]

def CreateTranscript(datos, text):
    return {
        'name':datos["name"],
        'id_device': datos["id_device"],
        'active_voice':datos["active_voice"],
        'start_time':datos["start_time"],
        'end_time':datos["end_time"],
        'data': text,
        'type': "TEXT",
        'format_byte': datos["format_byte"],
    }

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

    def callback(ch, method, properties, body):
        if helpers.is_reset(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        if datos["active_voice"] != None:
            frame_decodificado = helpers.encode(datos["data"], datos["format_byte"])
            data = np.frombuffer(frame_decodificado, dtype=np.int16)
            filename="temp.wav"
            #print(filename, datos["channels"], len(data), len(data[0::datos["channels"]]), flush=True)
            waveFile= wave.open(filename, 'wb')
            waveFile.setnchannels(1)
            waveFile.setsampwidth(datos["sampwidth"])
            waveFile.setframerate(datos["fps"])
            # wav = np.zeros(data[0::datos["channels"]].shape)
            # for i in range(datos["channels"]):
            #     wav = wav + data[i::datos["channels"]]
            # wav = wav/2
            waveFile.writeframes(b''.join(data[0::datos["channels"]]))
            waveFile.close()
            try:
                text= gooogle.speech(filename)
            except Exception as e:
                text=""
            if text != None and text != "":
                #print(datos["active_voice"], text, flush=True)
                new_frame = CreateTranscript(datos, text)
                channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(new_frame))
            os.remove(filename)

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