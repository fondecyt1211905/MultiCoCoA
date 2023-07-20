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
    "Exch_emotion": "Exch_emotion",
    "Exch_video_out": "Exch_video_out",
    
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
    "Q_emotion": "Q_emotion",
    "Q_video_out": "Queue_video_out",
}


# import os
# CONFIG = {
#     # Connection with rabbitMQ
#     "host": str(os.getenv("RABBITMQ_HOST", default="localhost")),
#     "port": str(os.getenv("RABBITMQ_PORT", default=5672)),
#     "user": str(os.getenv("RABBITMQ_USER", default='guest')),
#     "password": str(os.getenv("RABBITMQ_PASSWORD", default='guest')),

#     # Connection with mongoDB
#     "host_mongo": str(os.getenv("HOST_MONGO", default="localhost")),
#     "port_mongo": int(os.getenv("PORT_MONGO", default=27017)),
#     "db_mongo": str(os.getenv("DB_MONGO", default="virtualDevice")),
#     "host_backend": str(os.getenv("HOST_BACKEND", default="localhost")),

#     # Define config system
#     "format_byte": str(os.getenv("FORMAT", default="ISO-8859-1")),
#     "timeout": int(os.getenv("TIMEOUT", default=10)),
#     "tematica":os.getenv("TEMATICA", default="").split(","),
#     "margen":int(os.getenv("MARGEN", default=0.70)),
#     "vad_mode": int(os.getenv("CHUNKSVAD", default=1)),
#     "chunks_doa": int(os.getenv("CHUNKSDOA", default=15)),
#     "chunks_doa_s": int(os.getenv("CHUNKSDOAS", default=5)),
#     "chunks_filter_doa": int(os.getenv("CHUNKSFILTERDOA", default=5)),

#     # Define Exchange
#     "Exchange_direct": str(os.getenv("RABBITMQ_EX_0", default='exchange_direct_audio')),
#     "Exchange_8channels": str(os.getenv("RABBITMQ_EX_1", default='fanout_8channels')),
#     "Exchange_6channels": str(os.getenv("RABBITMQ_EX_2", default='fanout_6channels')),
#     "Exchange_vad_out": str(os.getenv("RABBITMQ_EX_3", default='fanout_vad_out')),
#     "Exchange_doa_out": str(os.getenv("RABBITMQ_EX_4", default='fanout_doa_out')),
#     "Exchange_filterdoa_out": str(os.getenv("RABBITMQ_EX_5", default='fanout_filterdoa_out')),
#     "Exchange_segmentation_out": str(os.getenv("RABBITMQ_EX_6", default='fanout_segmentation_out')),
#     "Exchange_vam_out": str(os.getenv("RABBITMQ_EX_7", default='fanout_vam_out')),
#     "Exchange_apm_out": str(os.getenv("RABBITMQ_EX_8", default='fanout_apm_out')),
#     "Exchange_transcription_out": str(os.getenv("RABBITMQ_EX_9", default='fanout_transcription_out')),
#     "Exchange_nlp_out": str(os.getenv("RABBITMQ_EX_10", default='fanout_nlp_out')),
    

#     # name queue
#     "Buffer_audio": str(os.getenv("BUFFERA", default="Buffer_audio")),
#     "Buffer_video": str(os.getenv("BUFFERV", default="Buffer_video")),
#     "Buffer_8to6": str(os.getenv("BUFFER1", default="Buffer_8to6")),
#     "Buffer_vad": str(os.getenv("BUFFER2", default="Buffer_vad")),
#     "Buffer_doa": str(os.getenv("BUFFER3", default="Buffer_doa")),
#     "Buffer_filterdoa": str(os.getenv("BUFFER4", default="Buffer_filterdoa")),
#     "Buffer_segmentation": str(os.getenv("BUFFER5", default="Buffer_segmentation")),
#     "Buffer_vam": str(os.getenv("BUFFER6", default="Buffer_vam")),
#     "Buffer_apm": str(os.getenv("BUFFER7", default="Buffer_apm")),
#     "Buffer_transcription": str(os.getenv("BUFFER8", default="Buffer_transcription")),
#     "Buffer_nlp": str(os.getenv("BUFFER9", default="Buffer_nlp")),

#     # name queue db 
#     "Buffer_apm_db": str(os.getenv("BUFFER10", default="Buffer_apm_db")),
#     "Buffer_vad_doa_db": str(os.getenv("BUFFER11", default="Buffer_vad_doa_db")),
#     "Buffer_transcription_db": str(os.getenv("BUFFER12", default="Buffer_transcription_db")),
#     "Buffer_nlp_db": str(os.getenv("BUFFER13", default="Buffer_nlp_db")),
#     "Buffer_segmentation_db": str(os.getenv("BUFFER14", default="Buffer_segmentation_db")),
# }

