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

def declare(channel, exchange, exchange_type, queue, exclusive):
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    result = channel.queue_declare(queue=queue, exclusive=exclusive)
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

def identificador(name, id_device, tipo, formato, frameRate, frameCount, width, height, channels, chunk, format_byte):
    return {
        "name": name,
        "id_device": id_device,
        "type": tipo,
        "format": formato,
        "frameRate": frameRate,
        "frameCount": frameCount,
        "width": width,
        "height": height,
        "channels": channels,
        "chunk": chunk,
        "format_byte": format_byte
    }

def decode(data, format_byte):
    data_decoded = data.decode(format_byte)
    return data_decoded

def encode(data, format_byte):
    data_encoded = data.encode(format_byte)
    return data_encoded

