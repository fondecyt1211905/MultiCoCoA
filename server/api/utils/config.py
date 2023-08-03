import os
CONFIG = {
    # Server api
    "api_host": str(os.getenv("API_HOST", default="0.0.0.0")),
    "api_port": int(os.getenv("API_PORT", default=3001)),
    "api_debug": (os.getenv("API_MODE", default='True') == 'True'),
    "api_exchange": "Exch_analysis",
    "api_exchange_type": "direct",
    "api_out_audio": "Queue_audio",
    "api_out_video": "Queue_video2",

    # Connection with mongoDB
    "mongo_host": str(os.getenv("MONGO_HOST", default="localhost")),
    "mongo_port": int(os.getenv("MONGO_PORT", default=27018)),
    "mongo_db": str(os.getenv("MONGO_DB", default="virtualDevice")),
    
    # Connection with rabbitMQ
    "rabbitmq_host": str(os.getenv("RABBITMQ_HOST", default="localhost")),
    "rabbitmq_port": str(os.getenv("RABBITMQ_PORT", default=5672)),
    "rabbitmq_user": str(os.getenv("RABBITMQ_USER", default='guest')),
    "rabbitmq_password": str(os.getenv("RABBITMQ_PASSWORD", default='guest')),
    "rabbitmq_timeout": int(os.getenv("RABBITMQ_TIMEOUT", default=10)),

    ## define config streamAudio
    "sa_in_ex": "Exch_analysis",
    "sa_in_ex_type": "direct",
    "sa_in_q": "Queue_audio",
    "sa_out_ex": "Exch_in_8to6",
    "sa_out_q": "Queue_8to6",
    "sa_chunk": 100,
    "sa_name": "VirtualAudio",
    "sa_format_byte": "ISO-8859-1",

    ## define config streamVideo
    "sv_in_ex": "Exch_analysis",
    "sv_in_ex_type": "direct",
    "sv_in_q": "Queue_video2",
    "sv_out_ex": "Exch_in_userR",
    "sv_out_q": "Queue_in_userR",
    "sv_name": "VirtualVideo",
    "sv_format_byte": "ISO-8859-1",
}