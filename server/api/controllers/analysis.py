import shutil
from flask import request, jsonify
from database.models import Analysis, Activity
import utils.config as config
import utils.helpers as helpers
import database.directdb as directdb
import os, json
conf = config.CONFIG

def create_analysis():
    if request.method == "POST":
        data = request.get_json()
        idactivity = data["_id"]["$oid"]
        activity = Activity.objects.get(id=idactivity)
        #crear analisis
        analysis = Analysis.objects.create(id_activity=activity, start=int(data["start"]), end=int(data["end"]))
        id=str(analysis.id)
        #crear carpeta con el id del analisis
        path = os.path.join(os.getcwd(),"analysis", id)
        os.makedirs(path, exist_ok=True)
        # Connection
        con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"], conf["rabbitmq_timeout"])

        # Declare
        channel.exchange_declare(exchange=conf["api_exchange"], exchange_type=conf["api_exchange_type"])
        
        def message(id,filename):
            return {
                "id": id,
                "filename": filename
            }

        # Create queue
        for file in data["files"]:
            if file['type'].lower() == "audio":
                channel.basic_publish(exchange=conf["api_exchange"], routing_key=conf["api_out_audio"], body=json.dumps(message(id,file["filename"])))
            if file['type'].lower() == "video":
                channel.basic_publish(exchange=conf["api_exchange"], routing_key=conf["api_out_video"], body=json.dumps(message(id,file["filename"])))
        
        con.close()
        analysis.save()
        return jsonify({'message': 'Analysis request sent' }), 200
    else:
        return jsonify({'message': 'Bad request'}), 400
    
# listar analisis y agregar actividad
def get_analysis():
    if request.method == "GET":
        analysis = Analysis.objects()
        result = []
        for a in analysis:
            try:
                activity = Activity.objects.get(id=a.id_activity.id)
            except:
                activity = None
            result.append({
                "id": str(a.id),
                "id_activity": str(a.id_activity.id),
                "start": a.start,
                "end": a.end,
                "time": a.time,
                "name": activity.name if activity else None
            })
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

# listar analisis por id
def get_analysis_by_id(id):
    if request.method == "GET":
        analysis = Analysis.objects.get(id=id)

        activity = Activity.objects.get(id=analysis.id_activity.id)
        result ={
                "id": str(analysis.id),
                "id_activity": str(analysis.id_activity.id),
                "start": analysis.start,
                "end": analysis.end,
                "time": analysis.time,
                "indicators": analysis.indicators,
                "name": activity.name
            }
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

# Eliminar analisis
def delete_analysis(id):
    if request.method == "DELETE":
        analysis = Analysis.objects.get(id=id)
        #eliminar carpeta con el id del analisis
        path = os.path.join(os.getcwd(),"analysis", id)
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass
        db = directdb.connect()
        for indicator_name in analysis.indicators:
            indicator = db[indicator_name]
            indicator.delete_many({"id_analysis": id})
        analysis.delete()
        return jsonify({'message': 'Analysis deleted'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400