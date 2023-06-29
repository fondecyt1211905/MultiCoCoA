#Import libraries
import json
import sys
import os
import config.config as config
import helpers.helpers as helpers
import argparse
conf= config.CONFIG

import plotly.figure_factory as ff
import datetime
from operator import itemgetter

colors = {"Usuario 1": 'rgb(255, 0, 0)',
          "Usuario 2": 'rgb(255, 20, 147)',
          "Usuario 3": 'rgb(255, 69, 0)',
          "Usuario 4": 'rgb(0, 255, 0)',
          "Usuario 5": 'rgb(32, 178, 70)',
          "Usuario 6": 'rgb(210, 180, 40)',
          "Usuario 7": 'rgb(160, 82, 45)'}

#Global Elements
buff_data=[]

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--user", default=conf["user"], help="usuario rabbitmq")
parser.add_argument("--password", default=conf["password"], help="password rabbitmq")
parser.add_argument("--host", default=conf["host"], help="host rabbitmq")
parser.add_argument("--port", type=int, default=conf["port"], help="port rabbitmq")
parser.add_argument("--timeout", type=int, default=conf["timeout"], help="timeout rabbitmq")
parser.add_argument("--exchange", default=conf["exchange_direct"], help="exchange rabbitmq")
parser.add_argument("--queue", default=conf["queue6"], help="queue rabbitmq")
parser.add_argument("--csv", type=str, default=None, help="filename .csv")
parser.add_argument("--notlooking", type=bool, default=True, help="True para marcar cuando el usuario no está mirando, False para marcar siempre")
args = parser.parse_known_args()

def main():
  # Connection
  channel = helpers.connect(args[0].user, args[0].password, args[0].host, args[0].port, args[0].timeout)

  # Declare
  channel = helpers.declare(channel, args[0].exchange, "direct", args[0].queue)

  #Callback function
  def callback(ch, method, properties, body):
    if helpers.is_reset(body):
      buff_data.clear()
    else:
        identification = json.loads(body)   
        actual_time=int(identification["time"])
        for user, data in identification["users"].items():
          if args[0].notlooking and data["looking_status"] != "Not Sure":
            buff_data.append(dict(Task="Usuario "+ user, Usuarios="Usuario " + data["looking_user"], Start=datetime.datetime.fromtimestamp(actual_time), Finish=datetime.datetime.fromtimestamp(actual_time+1)))
          elif args[0].notlooking == False:
             buff_data.append(dict(Task="Usuario "+ user, Usuarios="Usuario " + data["looking_user"], Start=datetime.datetime.fromtimestamp(actual_time), Finish=datetime.datetime.fromtimestamp(actual_time+1)))
        print("[*] Received info from frame in second ", actual_time)
  
  channel.basic_consume(queue=args[0].queue, on_message_callback=callback, auto_ack=True)
  print(' [*] Waiting for messages. To exit and generate graphic press CTRL+C',flush=True)
  channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        buff_data= sorted(buff_data, key=itemgetter('Task','Usuarios'))
        #buff_data = sorted(buff_data, key=lambda d: (d['Task'],d['Usuarios'])) 
        print(buff_data)
        fig = ff.create_gantt(buff_data, colors=colors, index_col='Usuarios', show_colorbar=True, group_tasks=True, title= "Miradas de usuarios a lo largo del tiempo")
        fig['layout']['yaxis2'] = {}
        fig.layout.yaxis2.update({'title': 'Usuarios'})
        fig.show()

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)