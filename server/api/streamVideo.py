import os, time, json, cv2
import database.directdb as directdb
import utils.config as config
import utils.helpers as helpers
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = conf["sv_in_ex"]
type_exchange_in = conf["sv_in_ex_type"]
queue_in = conf["sv_in_q"]
exchange_out = conf["sv_out_ex"]
queue_out = conf["sv_out_q"]

def VideoService():

    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"], conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

    def callback(ch, method, properties, data):
        data = json.loads(data)
        idAnalysis = data["id"]
        filename = data["filename"]
        # establecemos la conexión con la base de datos MongoDB
        result = directdb.getAnalysis(idAnalysis)
        print("idAct: ", result.get("id_activity"), "start: ", result.get("start"), "end: ", result.get("end"), "numParticipants", result.get("activity")[0].get("numParticipants"), flush=True)
        # send message to reset service
        channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body="ResetService")

        # Open video File
        file = os.path.join(os.getcwd(), "data", str(result.get("id_activity")), filename)
        if os.path.exists(file):
            cap = cv2.VideoCapture(file)
            # Check if camera opened successfully
            if (cap.isOpened()== False):
                print("Error opening video stream or file")
                return
            # Read until video is completed

            # get metadata of video
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            channels = cap.get(cv2.CAP_PROP_CHANNEL)
            frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

            # 
            identification = helpers.menssage(
                name=conf["sv_name"],
                id_device=idAnalysis,
                numUsers=result.get("activity")[0].get("numParticipants"),
                tipo="VIDEO",
                fps=fps,
                frames=frames,
                width=width,
                height=height,
                channels=channels,
                format_byte=conf["sv_format_byte"]
            )
            print("Process", idAnalysis, filename, flush=True)

            # Stream video
            start = 0 if result.get("start") is None else result.get("start")
            end = 0 if result.get("end") is None else result.get("end")
            delta_time = 1/fps
            start_time = time.time()
            next_time = start_time + delta_time
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, start*fps)
            while(cap.isOpened()):
                t = time.time()
                if t < next_time:
                    time.sleep(next_time - t)
                # Capture frame-by-frame
                ret, frame = cap.read()
                pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
                if ret == True:
                    identification["position"] = pos
                    identification["time"] = round(((pos - start) / fps)-delta_time,2)
                    is_success, im_buf_arr = cv2.imencode(".jpg", frame)
                    sdata_decoded = helpers.decode(im_buf_arr.tobytes(), identification["format_byte"])
                    identification["data"] = sdata_decoded
                    #Publicacion de data en json hacia la queue1
                    channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(identification))
                    start_time = next_time
                    next_time = start_time + delta_time
                    #print("[x] Sent frame in the time", identification["time"], "fps: ", identification["fps"], "pos: ", pos )
                    if pos/fps >= end:
                        break
                else:
                    break
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body="SaveService")

            cap.release()
            print("Process", idAnalysis, filename, "OK", flush=True)
        else:
            print("The file does not exist at the specified path",flush=True) 
            
    try:
        channel.basic_consume(queue=queue_in, on_message_callback=callback, auto_ack=True)
    
        print(' [*] Waiting for file. To exit press CTRL+C', flush=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted', flush=True)
    finally:
        channel.close()
        con.close()

if __name__ == '__main__':
    VideoService()


