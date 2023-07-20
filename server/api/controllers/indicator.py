from flask import request, jsonify, make_response
from database.models import Analysis
from bson.objectid import ObjectId
from mongoengine import ValidationError
import database.directdb as directdb
import utils.config as config
import pandas as pd
conf = config.CONFIG

from controllers.drawtodf import get_df, concat_df_apm, process_data_head

def create_indicator_measure(indicator_name):
    if request.method == "POST":
        # validar key
        try:
            key = request.get_json()["measures"]
            key = request.get_json()["start"]
            key = request.get_json()["end"]
            key = request.get_json()["id_analysis"]
        except KeyError:
            print("bad request, code 1")
            return jsonify({'message': 'Bad request, code 1'}), 400
        # validar id_analysis existe
        try:
            analysis = Analysis.objects(id=ObjectId(request.get_json()["id_analysis"])).first()
        except ValidationError:
            print("bad request, code 2")
            return jsonify({'message': 'Bad request, code 2'}), 400
        if analysis is None:
            return jsonify({'message': 'Analysis not found'}), 404
        # actualizar analysis agrgar indicador a la lista
        analysis.indicators.append(indicator_name)
        #eliminar duplicados
        analysis.indicators = list(set(analysis.indicators))
        analysis.save()
        # establecemos la conexión con la base de datos MongoDB
        db = directdb.connect()
        # seleccionamos la colección
        indicator = db[indicator_name]
        # get data from request
        data = request.get_json()
        # insert data in collection
        result = indicator.insert_one(data)
        return jsonify({'message': 'Indicator measure created'}), 200
    else:
        print("bad request, code 3")
        return jsonify({'message': 'Bad request, code 3'}), 400
    
def get_indicator_measure(indicator_name, id_analysis):
    if request.method == "GET":
        # establecemos la conexión con la base de datos MongoDB
        db = directdb.connect()
        indicator = db[indicator_name]
        results = indicator.find({"id_analysis": id_analysis})
        result = []
        for r in results:
            r["_id"] = str(r["_id"])
            result.append(r)
        return jsonify(result), 200
    else:
        print("bad request, code 3")
        return jsonify({'message': 'Bad request, code 3'}), 400
    
def download_indicator_measure_csv(indicator_name, id_analysis):
    if request.method == "GET":
        # establecemos la conexión con la base de datos MongoDB
        df = get_df(indicator_name, id_analysis)
        if indicator_name == "video_output":
            df = process_data_head(df)
        csv = df.to_csv(index=False, sep=';')
        response = make_response(csv)
        response.headers.set('Content-Type', 'text/csv')
        response.headers.set('Content-Disposition', 'attachment', filename='data.csv')
        return response
    else:
        print("bad request, code 3")
        return jsonify({'message': 'Bad request, code 3'}), 400