import os
CONFIG = {
    # Server api
    "api_host": str(os.getenv("API_HOST", default="0.0.0.0")),
    "api_port": int(os.getenv("API_PORT", default=3001)),
    "api_debug": (os.getenv("API_MODE", default='True') == 'True'),

    # Connection with mongoDB
    "mongo_host": str(os.getenv("MONGO_HOST", default="localhost")),
    "mongo_port": int(os.getenv("MONGO_PORT", default=27018)),
    "mongo_db": str(os.getenv("MONGO_DB", default="virtualDevice")),

    # Connection with api
    "host_backend": str(os.getenv("HOST_BACKEND", default="localhost:3001")),

    # Connection with rabbitMQ
    "rabbitmq_host": str(os.getenv("RABBITMQ_HOST", default="localhost")),
    "rabbitmq_port": str(os.getenv("RABBITMQ_PORT", default=5672)),
    "rabbitmq_user": str(os.getenv("RABBITMQ_USER", default='guest')),
    "rabbitmq_password": str(os.getenv("RABBITMQ_PASSWORD", default='guest')),
    "rabbitmq_timeout": int(os.getenv("RABBITMQ_TIMEOUT", default=10)),

    #config acousticProsodicFeatures
    "apf_in_ex": "Exch_apm_out",
    "apf_in_ex_type": "fanout",
    "apf_in_q": "Q_apm_db",
    "apf_name_indicator": "Acoustic-Prosodic-Features",

    #config audioSegment
    "seg_in_ex": "Exch_segmentator_out",
    "seg_in_ex_type": "fanout",
    "seg_in_q": "Q_segmentator_db",
    "seg_name_indicator": "Audio-Segmentation",

    #config vadDoaFeatures
    "vdf_in_ex": "Exch_filter_doa_out",
    "vdf_in_ex_type": "fanout",
    "vdf_in_q": "Q_vad_doa_db",
    "vdf_name_indicator": "VAD-DOA-Features",

    #config HeadSightFeatures
    "hsf_in_ex": "Exch_video_out",
    "hsf_in_ex_type": "fanout",
    "hsf_in_q": "Queue_video_out",
    "hsf_name_indicator": "HeadSight-Features",

    #config NaturalLanguageFeatures
    "nlf_in_ex": "Exch_nlp_out",
    "nlf_in_ex_type": "fanout",
    "nlf_in_q": "Q_nlp_db",
    "nlf_name_indicator": "Natural-Language-Features",
}

