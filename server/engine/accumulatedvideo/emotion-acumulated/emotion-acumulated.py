import cv2
import sys
import pika
import json
import sys
import os
#sys.path.append(''.join((os.getcwd(), '/server/pipeline-video/config')))
#sys.path.append(''.join((os.getcwd(), '/server/pipeline-video/helpers')))
import config.config as config
import helpers.helpers as helpers
conf= config.CONFIG
cont = 0
def main():
    
    channel = helpers.connect(conf["user"],conf["password"],conf["host"], conf["port"],conf["timeout"])
    channel = helpers.declare(channel,conf["exchange_direct"],"direct",conf["queue4"])
    print("PAso")
    def callback(ch, method, properties, body):
        print("LEgga calbdack")
        print(body)

    channel.basic_consume(queue=conf["queue4"], on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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