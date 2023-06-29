import os
CONFIG = {
    # Connection with rabbitMQ
    "host": str(os.getenv("RABBITMQ_HOST", default="10.100.6.14")),
    "port": str(os.getenv("RABBITMQ_PORT", default=5672)),
    "user": str(os.getenv("RABBITMQ_USER", default='guest')),
    "password": str(os.getenv("RABBITMQ_PASSWORD", default='guest')),
    "credentials": str(os.getenv("CREDENT_RABBITMQ", default='guest')),

    # Define Exchange
    "exchange_direct": str(os.getenv("RABBITMQ_EX_DIRECT", default='direct_logs')),
    "exchange_userr": str(os.getenv("RABBITMQ_EX_USERR", default='fanout_userr')),
    
    # Define config system
    "format_byte": str(os.getenv("FORMAT", default="ISO-8859-1")),
    "timeout": int(os.getenv("TIMEOUT", default=10)),
    "tematica":os.getenv("TEMATICA", default="").split(","),
    "margen":int(os.getenv("MARGEN", default=0.70)),
    "chunks_doa": int(os.getenv("CHUNKSDOA", default=15)),
    "chunks_filter_doa": int(os.getenv("CHUNKSFILTERDOA", default=5)),
    "detector_name": str(os.getenv("DETECTOR_NAME", default="mediapipe")),
    
    # name queue
    "queue1": str(os.getenv("QUEUE1", default="Buff1")),
    "queue2": str(os.getenv("QUEUE2", default="Buff2")),
    "queue3": str(os.getenv("QUEUE3", default="Buff3")),
    "queue4": str(os.getenv("QUEUE4", default="Buff4")),
    "queue5": str(os.getenv("QUEUE5", default="Buff5")),
    "queue6": str(os.getenv("QUEUE6", default="Buff6")),
    "queue7": str(os.getenv("QUEUE7", default="Buff7")),
    "queue8": str(os.getenv("QUEUE8", default="Buff8")),
    "queue9": str(os.getenv("QUEUE9", default="Buff9")),
    "queue10": str(os.getenv("QUEUE10", default="Buff10")),

}


