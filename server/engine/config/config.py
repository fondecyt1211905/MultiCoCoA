import os
CONFIG = {
    # Server api
    "api_host": str(os.getenv("API_HOST", default="0.0.0.0")),
    "api_port": int(os.getenv("API_PORT", default=3001)),
    "api_debug": (os.getenv("API_MODE", default='True') == 'True'),

    # Connection with mongoDB
    "mongo_host": str(os.getenv("MONGO_HOST", default="localhost")),
    "mongo_port": int(os.getenv("MONGO_PORT", default=27017)),
    "mongo_db": str(os.getenv("MONGO_DB", default="virtualDevice")),

    # Define config system pipeline video
    "pv_name": str(os.getenv("PV_NAME", default="VirtualCam")),
    "pv_format_byte": str(os.getenv("PV_FORMAT", default="ISO-8859-1")),
    "pv_detector_name": str(os.getenv("PV_DETECTOR_NAME", default="retinaface")),
    "pv_radio": int(os.getenv("PV_RADIO", default=90)),

    # Connection with rabbitMQ
    "rabbitmq_host": str(os.getenv("RABBITMQ_HOST", default="localhost")),
    "rabbitmq_port": str(os.getenv("RABBITMQ_PORT", default=5672)),
    "rabbitmq_user": str(os.getenv("RABBITMQ_USER", default='guest')),
    "rabbitmq_password": str(os.getenv("RABBITMQ_PASSWORD", default='guest')),
    "rabbitmq_timeout": int(os.getenv("RABBITMQ_TIMEOUT", default=10)),

    # Define type exchange
    "type_exchange_direct": str(os.getenv("TYPE_EXCHANGE_DIRECT", default="direct")),
    "type_exchange_fanout": str(os.getenv("TYPE_EXCHANGE_FANOUT", default="fanout")),

    # config 8to6wav
    "8to6wav_in_ex": "Exch_in_8to6",
    "8to6wav_in_ex_type": "direct",
    "8to6wav_in_q": "Queue_8to6",
    "8to6wav_out_ex": "Exch_in_vad",
    "8to6wav_out_q": "Queue_vad",

    #config vad
    "vad_in_ex": "Exch_in_vad",
    "vad_in_ex_type": "direct",
    "vad_in_q": "Queue_vad",
    "vad_out_ex": "Exch_in_doa",
    "vad_out_q": "Queue_doa",
    "vad_mode": 1,

    #config doa
    "doa_in_ex": "Exch_in_doa",
    "doa_in_ex_type": "direct",
    "doa_in_q": "Queue_doa",
    "doa_out_ex": "Exch_in_filter_doa",
    "doa_out_q": "Queue_filter_doa",
    "doa_out_q": "Queue_filter_doa",
    "doa_number_of_chunks": 15,
    "doa_chunk_threshold": 5,

    #config filter_doa
    "filter_doa_in_ex": "Exch_in_filter_doa",
    "filter_doa_in_ex_type": "direct",
    "filter_doa_in_q": "Queue_filter_doa",
    "filter_doa_out_ex": "Exch_filter_doa_out",
    "filter_doa_out_q": "",
    "filter_chunk_threshold": 5,

    #config segmentator
    "segmentator_in_ex": "Exch_filter_doa_out",
    "segmentator_in_ex_type": "fanout",
    "segmentator_in_q": "Queue_segmentator",
    "segmentator_out_ex": "Exch_segmentator_out",
    "segmentator_out_q": "",

    #config apm
    "apm_in_ex": "Exch_segmentator_out",
    "apm_in_ex_type": "fanout",
    "apm_in_q": "Queue_apm",
    "apm_out_ex": "Exch_apm_out",
    "apm_out_q": "",

    #config transcriptor
    "transcriptor_in_ex": "Exch_segmentator_out",
    "transcriptor_in_ex_type": "fanout",
    "transcriptor_in_q": "Queue_transcriptor",
    "transcriptor_out_ex": "Exch_in_nlp",
    "transcriptor_out_q": "Queue_nlp",

    #config nlp
    "nlp_in_ex": "Exch_in_nlp",
    "nlp_in_ex_type": "direct",
    "nlp_in_q": "Queue_nlp",
    "nlp_out_ex": "Exch_nlp_out",
    "nlp_out_q": "",

    #config userRecognition
    "userR_in_ex": "Exch_in_userR",
    "userR_in_ex_type": "direct",
    "userR_in_q": "Queue_in_userR",
    "userR_out_ex": "Exch_in_facedirection",
    "userR_out_q": "Queue_facedirection",

    #config facedirection
    "facedirection_in_ex": "Exch_in_facedirection",
    "facedirection_in_ex_type": "direct",
    "facedirection_in_q": "Queue_facedirection",
    "facedirection_out_ex": "Exch_in_headsight",
    "facedirection_out_q": "Queue_headsight",

    #config headsight
    "headsight_in_ex": "Exch_in_headsight",
    "headsight_in_ex_type": "direct",
    "headsight_in_q": "Queue_headsight",
    "headsight_out_ex": "Exch_video_out",
    "headsight_out_q": "Queue_video_out",
}