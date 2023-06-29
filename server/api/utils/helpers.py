import pika
import time
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

def menssage(
        name, 
        id_device, 
        tipo, 
        fps=None,
        sampwidth=None, 
        channels=None, 
        chunk=None, 
        format_byte=None,
        frames=None,
        width=None,
        height=None,
    ):
    msg = {
        "name": name,
        "id_device": id_device,
        "type": tipo,
    }
    if fps != None:
        msg["fps"] = fps
    if sampwidth != None:
        msg["sampwidth"] = sampwidth
    if channels != None:
        msg["channels"] = channels
    if chunk != None:
        msg["chunk"] = chunk
    if format_byte != None:
        msg["format_byte"] = format_byte
    if frames != None:
        msg["frames"] = frames
    if width != None:
        msg["width"] = width
    if height != None:
        msg["height"] = height
    return msg

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