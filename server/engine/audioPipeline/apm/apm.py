import numpy as np
import pandas as pd
import opensmile
import sys, os
import json
import config
import helpers
import wave
import audiofile
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = conf["apm_in_ex"]
type_exchange_in = conf["apm_in_ex_type"]
queue_in = conf["apm_in_q"]
exchange_out = conf["apm_out_ex"]
queue_out = conf["apm_out_q"]

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)
    #Declaracion de smile (Configurar en archivo)
    smile = opensmile.Smile(
        feature_set= 'IS10_paraling_compat.conf',
        #feature_set= 'EMOTIONAL SPEECH - EMODB\entrainment_config.conf',
        feature_level='func',
        loglevel=2,
        #logfile='smile.log',
    )

    def callback(ch, method, properties, body):
        if helpers.is_reset(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        
        frame_decodificado = helpers.encode(datos["data"], datos["format_byte"])
        data = np.frombuffer(frame_decodificado, dtype=np.int16)
        filename="temp.wav"
        waveFile= wave.open(filename, 'wb')
        waveFile.setnchannels(datos["channels"])
        waveFile.setsampwidth(datos["sampwidth"])
        waveFile.setframerate(datos["fps"])
        waveFile.writeframes(b''.join(data))
        waveFile.close()

        #data = np.resize(data, (int(len(data)/datos["channels"]),datos["channels"])).T
        signal, sampling_rate = audiofile.read(filename)
        #Procesamiento de señal
        
        result_df = smile.process_signal(
            signal,
            sampling_rate
        )
        
        #Declaracion de features y composicion
        features = [
            'F0final_sma_maxPos', 'F0final_sma_minPos', 'F0final_sma_amean' , 'F0final_sma_stddev',
            'pcm_loudness_sma_maxPos', 'pcm_loudness_sma_minPos', 'pcm_loudness_sma_amean', 'pcm_loudness_sma_stddev',
            'jitterLocal_sma_maxPos', 'jitterLocal_sma_minPos', 'jitterLocal_sma_amean', 'jitterLocal_sma_stddev',
            'jitterDDP_sma_maxPos', 'jitterDDP_sma_minPos', 'jitterDDP_sma_amean', 'jitterDDP_sma_stddev',
            'shimmerLocal_sma_maxPos', 'shimmerLocal_sma_minPos', 'shimmerLocal_sma_amean', 'shimmerLocal_sma_stddev',
            'F0final__Turn_numOnsets', 'F0final__Turn_duration'
        ]
        features_df = result_df[features]
        features_df = pd.Series.tolist(features_df)
        #Las traspaso a json
        features_json = {
            "F0final_sma_maxPos": float(result_df['F0final_sma_maxPos']),
            "F0final_sma_minPos": float(result_df['F0final_sma_minPos']),
            "F0final_sma_amean": float(result_df['F0final_sma_amean']),
            "F0final_sma_stddev": float(result_df['F0final_sma_stddev']),
            "pcm_loudness_sma_maxPos": float(result_df['pcm_loudness_sma_maxPos']),
            "pcm_loudness_sma_minPos": float(result_df['pcm_loudness_sma_minPos']),
            "pcm_loudness_sma_amean": float(result_df['pcm_loudness_sma_amean']),
            "pcm_loudness_sma_stddev": float(result_df['pcm_loudness_sma_stddev']),
            "jitterLocal_sma_maxPos": float(result_df['jitterLocal_sma_maxPos']),
            "jitterLocal_sma_minPos": float(result_df['jitterLocal_sma_minPos']),
            "jitterLocal_sma_amean": float(result_df['jitterLocal_sma_amean']),
            "jitterLocal_sma_stddev": float(result_df['jitterLocal_sma_stddev']),
            "jitterDDP_sma_maxPos": float(result_df['jitterDDP_sma_maxPos']),
            "jitterDDP_sma_minPos": float(result_df['jitterDDP_sma_minPos']),
            "jitterDDP_sma_amean": float(result_df['jitterDDP_sma_amean']),
            "jitterDDP_sma_stddev": float(result_df['jitterDDP_sma_stddev']),
            "shimmerLocal_sma_maxPos": float(result_df['shimmerLocal_sma_maxPos']),
            "shimmerLocal_sma_minPos": float(result_df['shimmerLocal_sma_minPos']),
            "shimmerLocal_sma_amean": float(result_df['shimmerLocal_sma_amean']),
            "shimmerLocal_sma_stddev": float(result_df['shimmerLocal_sma_stddev']),
            "F0final__Turn_numOnsets": float(result_df['F0final__Turn_numOnsets']),
            "F0final__Turn_duration": float(result_df['F0final__Turn_duration'])
        }
        #Le paso el json final a datos
        datos["features"] = features_json
        datos["data"] = helpers.decode(frame_decodificado, datos["format_byte"])

        # Publico en el exchange de apm
        channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(datos))

    channel.basic_consume(queue=queue_in, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)