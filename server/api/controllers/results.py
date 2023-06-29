from flask import request, jsonify
import os


def get_results(id_analysis):
    if request.method == "GET":
        
        return jsonify("result"), 200
    else:
        return jsonify({'message': 'Bad request'}), 400



"""from flask import Blueprint, request, jsonify, send_from_directory
from flask_cors import cross_origin
import utils.config as config
import os
conf = config.CONFIG

results_bp = Blueprint('results', __name__)

# Cargar archivo de una actividad
@results_bp.route('/<string:id_process>/<string:filename>', methods=['POST'])
@cross_origin()
def upload(id_process, filename):
    if request.method == "POST":
        try:
            file_audio = request.files['archivo']
            file_path = os.path.join(os.getcwd(), "analysis", id_process, filename)
            file_audio.save(file_path)
            file_audio.close()
        except Exception as e:
            return jsonify({'message': 'Error uploading file'}), 500
        return jsonify({'message': 'File uploaded'}), 200

# Descargar archivo de una actividad
@results_bp.route('/<string:id_process>/<string:filename>', methods=['GET'])
@cross_origin()
def download(id_process, filename):
    if request.method == "GET":
        print(id_process, filename)
        print(os.path.join(os.getcwd(), "analysis", id_process))
        return send_from_directory(directory=os.path.join(os.getcwd(), "analysis", id_process), filename=filename, as_attachment=True)
    else:
        return jsonify({'message': 'Bad request'}), 400
    
# Borrar archivo de una actividad"""