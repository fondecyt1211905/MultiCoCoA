import sys, os
import json
import config
import helpers
conf = config.CONFIG

nodes = {}

def main():
    # Connection
    channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"],conf["timeout"])
    # Declare
    channel = helpers.declare(channel, conf["exchange_apm"], "fanout", conf["queue14"])
    
    def CreateNode(current_user):
        return {
            "name": current_user,
            "duration": 0,
            "num_inter": 0,
            "interventions": []
        }

    def callback(ch, method, properties, body):
        global nodes
        if helpers.is_reset(body):
            nodes = {}
            channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue15"], body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue15"], body=body)
            return
        datos = json.loads(body)
       
        frame_duration = datos["speaking_time"]
        current_user = datos["active_voice"]
        features = datos["features"]

        if current_user not in nodes:
            nodes[current_user] = CreateNode(current_user)
        nodes[current_user]["duration"] += frame_duration
        nodes[current_user]["num_inter"] += 1
        nodes[current_user]["interventions"].append({"start:": datos["start_time"], "end": datos["end_time"], "features": features})
        
        channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue15"], body=json.dumps(nodes))
    
    channel.basic_consume(queue=conf["queue14"], on_message_callback=callback, auto_ack=True)
   
    print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        for clave, valor in nodes.items():
            print("----------------------", flush=True)
            print(clave, ":", valor, flush=True)
            print("----------------------", flush=True)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)