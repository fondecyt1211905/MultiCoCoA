#import pandas as pd
import json
import config
import helpers
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = conf["hsf_in_ex"]
type_exchange_in = conf["hsf_in_ex_type"]
queue_in = conf["hsf_in_q"]
name_indicator = conf["hsf_name_indicator"]

def video_output():
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
        datos.pop("data")
        print(datos, flush=True)
        features = {
            "position": datos["position"],
            "users": datos["users"],
        }
        helpers.send_post(
            host=config.CONFIG["host_backend"],
            nameIndicator=name_indicator,
            data= helpers.indicator_measure(id_analysis=datos.get("id_device"),measures=features,start_time=datos.get("time"),end_time=datos.get("time"))
        )
    try:
        channel.basic_consume(queue=queue_in, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
        channel.start_consuming()

    except KeyboardInterrupt:
        print('Interrupted', flush=True)
        channel.close()
        con.close()
        
if __name__ == '__main__':
    video_output()
