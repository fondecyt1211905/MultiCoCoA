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

    # Connection with api
    "host_backend": str(os.getenv("HOST_BACKEND", default="mmla-api")),

    # Define config system pipeline audio
    "pa_name": str(os.getenv("PA_NAME", default="VirtualMic")),
    "pa_format_byte": str(os.getenv("PA_FORMAT", default="ISO-8859-1")),
    "pa_chunk": int(os.getenv("PA_CHUNK", default=100)),
    "pa_vad_mode": int(os.getenv("PA_VAD_MODE", default=1)),
    "pa_doa_chunks": int(os.getenv("PA_DOA_CHUNKS", default=15)),
    "pa_doa_chunks_s": int(os.getenv("PA_DOA_CHUNKS_S", default=5)),
    "pa_filter_doa_chunks": int(os.getenv("PA_FILTER_DOA_CHUNKS", default=5)),

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
    "Exch_in_vad": "Exch_in_vad",
    "Exch_in_doa": "Exch_in_doa",
    "Exch_in_filter_doa": "Exch_in_filter_doa",
    "Exch_in_nlp": "Exch_in_nlp",
    "Exch_filter_doa_out": "Exch_filter_doa_out",
    "Exch_segmentator_out": "Exch_segmentator_out",
    "Exch_apm_out": "Exch_apm_out",
    "Exch_nlp_out": "Exch_nlp_out",
    
    "Exch_in_userr": "Exch_in_userr",
    "Exch_in_facedirection": "Exch_in_facedirection",
    "Exch_in_lookingdirection": "Exch_in_lookingdirection",
    "Exch_video_out": "Exch_video_out","Exch_in_userr": "Exch_in_userr",
    
    # name queue audio
    "Q_audio": "Queue_audio",
    "Q_8to6": "Queue_8to6",
    "Q_vad": "Queue_vad",
    "Q_doa": "Queue_doa",
    "Q_filter_doa": "Queue_filter_doa",
    "Q_segmentator": "Queue_segmentator",
    "Q_apm": "Queue_apm",
    "Q_transcriptor": "Queue_transcriptor",
    "Q_nlp": "Queue_nlp",

    # name queue video
    "Q_video": "Queue_video",
    "Q_userR": "Queue_in_userR",
    "Q_facedirection": "Queue_facedirection",
    "Q_lookingdirection": "Queue_lookingdirection",
    "Q_video_out": "Queue_video_out",

    # name queue output
    "Q_apm_db": "Queue_apm_db",
    "Q_nlp_db": "Queue_nlp_db",
    "Q_segmentator_db": "Queue_segmentator_db",
    "Q_vad_doa_db": "Queue_vad_doa_db",
    "Q_video_db": "Queue_video_db",
}

