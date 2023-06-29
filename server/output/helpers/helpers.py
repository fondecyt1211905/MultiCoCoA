import pika
import time
import requests
def connect(user, password, host, port, timeout):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host,port,'/', credentials)
    connection = None
    for i in range(timeout):
        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            print("Error AMQPConnectionError: %d" % i, flush=True)
            time.sleep(1)
    if connection is None:
        raise pika.exceptions.AMQPConnectionError
    return connection, connection.channel()

def declare(channel, exchange, exchange_type, queue):
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    result = channel.queue_declare(queue=queue, exclusive=True)
    channel.queue_bind(exchange=exchange, queue=result.method.queue, routing_key=result.method.queue)
    return channel
   
def is_reset(menssage):
    if menssage == b'ResetService':
        print("ResetService", flush=True)
        return True
    else:
        return False
    
def is_save(menssage):
    if menssage == b'SaveService':
        print("SaveService", flush=True)
        return True
    else:
        return False

def decode(data, format_byte):
    data_decoded = data.decode(format_byte)
    return data_decoded

def encode(data, format_byte):
    data_encoded = data.encode(format_byte)
    return data_encoded

def valid_file(filename):
    if filename != None and filename[-4:].lower() in ['.csv']:
        return True
    return False

# Envio post a backend
def send_post(host, nameIndicator, data):
    #/indicator-measure/NameIndicator
    session = requests.Session()
    response = session.post(f'http://{host}/indicator-measure/{nameIndicator}', json=data)
    if response.status_code == 200:
        pass
    else:
        print(f'Error al enviar a backend:{nameIndicator} {response.status_code} - {response.reason}', flush=True)

def indicator_measure(id_analysis, measures, start_time, end_time):
    return {
        "id_analysis": id_analysis,
        "measures": measures,
        "start": start_time,
        "end": end_time
    }