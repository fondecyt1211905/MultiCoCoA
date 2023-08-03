#import pandas as pd
import json
import config
import helpers
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = conf["nlf_in_ex"]
type_exchange_in = conf["nlf_in_ex_type"]
queue_in = conf["nlf_in_q"]
name_indicator = conf["nlf_name_indicator"]

def nlp():
    #buff_data = []
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
        features = {
            "active_voice": datos["active_voice"],
            "frase": datos["data"]["frase"],
            "data": datos["data"]["data"],
        }
        helpers.send_post(
            host=config.CONFIG["host_backend"],
            nameIndicator=name_indicator,
            data= helpers.indicator_measure(datos.get("id_device"),features,datos.get("start_time"),datos.get("end_time"))
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
    nlp()
