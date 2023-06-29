import sys, os
import json
import pandas as pd
sys.path.append(''.join((os.getcwd(), '/server/engine/pipelineaudio/config')))
sys.path.append(''.join((os.getcwd(), '/server/engine/pipelineaudio/helpers')))
import config
import helpers
import argparse
conf = config.CONFIG
import sys

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--user", default=conf["user"], help="usuario rabbitmq")
parser.add_argument("--password", default=conf["password"], help="password rabbitmq")
parser.add_argument("--host", default=conf["host"], help="host rabbitmq")
parser.add_argument("--port", type=int, default=conf["port"], help="port rabbitmq")
parser.add_argument("--timeout", type=int, default=conf["timeout"], help="timeout rabbitmq")
parser.add_argument("--exchange", default=conf["exchange_apm"], help="exchange rabbitmq")
parser.add_argument("--queue", default=conf["queue17"], help="queue rabbitmq")
parser.add_argument("--csv", type=str, default=None, help="filename .csv")
args = parser.parse_known_args()

buff_data = []
def main():
	# Connection
	channel = helpers.connect(args[0].user, args[0].password, args[0].host, args[0].port, args[0].timeout)
	# Declare
	channel = helpers.declare(channel, args[0].exchange, "fanout", args[0].queue)

	if args[0].csv != None and not helpers.valid_file(args[0].csv):
		raise argparse.ArgumentTypeError('File must have a csv extension')

	def callback(ch, method, properties, body):
		global buff_data
		if helpers.is_reset(body):
			buff_data = []
		else:
			datos = json.loads(body)
			features = datos.pop("features")
			datos.pop("data")
			datos.update(features)
			buff_data.append(datos)
			print("active_voice:", datos["active_voice"], flush=True)
	channel.basic_consume(queue=args[0].queue, on_message_callback=callback, auto_ack=True)
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		#print(buff_data)
		if args[0].csv != None and helpers.valid_file(args[0].csv):
			df = pd.DataFrame.from_dict(buff_data)
			df.to_csv(args[0].csv, sep=";")
			print(df.info())
		
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)