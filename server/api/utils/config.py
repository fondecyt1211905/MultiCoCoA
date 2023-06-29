import os
CONFIG = {
    # Server api
    "api_host": str(os.getenv("API_HOST", default="0.0.0.0")),
    "api_port": int(os.getenv("API_PORT", default=3001)),
    "api_debug": (os.getenv("API_MODE", default='True') == 'True'),

    # Connection with mongoDB
    "mongo_host": str(os.getenv("MONGO_HOST", default="10.100.6.14")),
    "mongo_port": int(os.getenv("MONGO_PORT", default=27017)),
    "mongo_db": str(os.getenv("MONGO_DB", default="virtualDevice")),

    # Define config system pipeline audio
    "pa_name": str(os.getenv("PA_NAME", default="VirtualMic")),
    "pa_format_byte": str(os.getenv("PA_FORMAT", default="ISO-8859-1")),
    "pa_chunk": int(os.getenv("PA_CHUNK", default=100)),

    # Define config system pipeline video
    "pv_name": str(os.getenv("PV_NAME", default="VirtualCam")),
    "pv_format_byte": str(os.getenv("PV_FORMAT", default="ISO-8859-1")),

    # Connection with rabbitMQ
    "rabbitmq_host": str(os.getenv("RABBITMQ_HOST", default="10.100.6.14")),
    "rabbitmq_port": str(os.getenv("RABBITMQ_PORT", default=5672)),
    "rabbitmq_user": str(os.getenv("RABBITMQ_USER", default='guest')),
    "rabbitmq_password": str(os.getenv("RABBITMQ_PASSWORD", default='guest')),
    "rabbitmq_timeout": int(os.getenv("RABBITMQ_TIMEOUT", default=10)),

    # Define type exchange
    "type_exchange_direct": str(os.getenv("TYPE_EXCHANGE_DIRECT", default="direct")),
    "type_exchange_fanout": str(os.getenv("TYPE_EXCHANGE_FANOUT", default="fanout")),

    # Define Exchange
    "Exch_analysis": "Exch_analysis",
    "Exch_in_8to6": "Exch_in_8to6",
    "Exch_in_userr": "Exch_in_userr",
    
    # name queue audio
    "Q_audio": "Queue_audio",
    "Q_8to6": "Queue_8to6",

    # name queue video
    "Q_video": "Queue_video",
    "Q_userR": "Queue_in_userR",
}