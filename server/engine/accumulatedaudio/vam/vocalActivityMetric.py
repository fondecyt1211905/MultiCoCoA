import sys, os
import json
import config
import helpers
conf = config.CONFIG
nodes = {}
links = {}
previous_user = None
start_time = 0
end_time = 0

#Configurations for the pipeline
exchange_in = "Exchange_segmentation_out"
type_exchange_in = "fanout"
queue_in = "Buffer_vam"
exchange_out = "Exchange_vam_out"
queue_out = ""

"""
# Estructura de salida comentado (links y nodos, frames)
links = {
    "1-2":{
    "source": 1,
    "target": 3,
    "size_link": 20,
    },
    "2-3":{
    "source": 2
    "target": 3,
    "size_link": 10
    }
}

nodes = {
    1: {
        "name": 1,
        "duration": 0.05,
        "num_intervenciones": 1,
        "intervention": [
            {
                start: 0
                end: 0.1
            }
        ]
            ,
    2: {
        "name": 2,
        "duration": 0.10,
        "num_intervenciones": 2,
         "intervention": [
            {
                start: 2
                end: 3
            },
            {
                start: 3.1 
                end: 4
            }
        ]
            },
        
}
"""
def CreateSegments(start_time, end_time, active):
    return {
        "start": start_time,
        "end": end_time,
        "active": active,
    }

def CreateIntervention(start_time, end_time, segments):
    return {
        "start": start_time,
        "end": end_time,
        "segments": segments
    }

def CreateNode(current_user, frame_duration, segment):
    return {
        "name": current_user,
        "duration": frame_duration,
        "num_inter": 0,
        "interventions": [],
        "buff": [segment]
    }

def CreateLink(current_user, previous_user):
    return {
        "source": previous_user,
        "target": current_user,
        "size_link": 1
    }

def main():
    # Connection
    channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"],conf["timeout"])
    # Declare
    channel = helpers.declare(channel, conf[exchange_in], type_exchange_in, conf[queue_in])

    def callback(ch, method, properties, body):
        global nodes
        global links
        global previous_user
        global start_time
        global end_time
        if helpers.is_reset(body):
            nodes = {}
            links = {}
            previous_user = None
            start_time = 0
            end_time = 0
            channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
       
        frame_duration = datos["speaking_time"]
        current_user = datos["active_voice"]

        if current_user != None and current_user not in nodes: # crear nodo de no existir
            nodes[current_user] = CreateNode(current_user, frame_duration, CreateSegments(datos["start_time"], datos["end_time"], datos["active_voice"]))
        else:
            if current_user == None:
                if previous_user != None:
                    nodes[previous_user]["duration"] += frame_duration
                    nodes[previous_user]["buff"].append(CreateSegments(datos["start_time"], datos["end_time"], datos["active_voice"]))
                else:
                    pass
            else:
                nodes[current_user]["duration"] += frame_duration
                nodes[current_user]["buff"].append(CreateSegments(datos["start_time"], datos["end_time"], datos["active_voice"]))
        
        # crear enlaces
        if previous_user!=current_user and previous_user != None and current_user != None:
            end_time = datos["end_time"]
            nodes[previous_user]["num_inter"] += 1
            nodes[previous_user]["interventions"].append(CreateIntervention(start_time, end_time, nodes[previous_user]["buff"]))
            nodes[previous_user]["buff"] = []
            start_time = end_time

            if f"{previous_user}-{current_user}" not in links:
                links[f"{previous_user}-{current_user}"] = CreateLink(current_user,previous_user)
            else:
                links[f"{previous_user}-{current_user}"]["size_link"] += 1
        
        if current_user != None:
            previous_user = current_user
        
        #print(nodes, flush=True)
        channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=json.dumps({"frame": datos, "nodes": nodes, "links": links}))

    channel.basic_consume(queue=conf[queue_in], on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        for clave, valor in nodes.items():
            print("----------------------")
            print(clave, ":", valor)
            print("----------------------")
        for clave, valor in links.items():
            print("******************************")
            print(clave, ":", valor)
            print("****************************")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)