from flask import Flask
import utils.config as config
from flask_cors import CORS
from flasgger import Swagger
from database.db import initialize_db
from flask_cors import cross_origin

from controllers.activities import create_activity, get_activities, get_activity, delete_activity, get_activity_file
from controllers.analysis import create_analysis, get_analysis, get_analysis_by_id, delete_analysis
from controllers.results import get_results
from controllers.indicator import create_indicator_measure, get_indicator_measure, download_indicator_measure_csv
from controllers.charts import get_chart_segmentation, get_chart_vocal_activity, get_chart_apm, get_chart_head_sight, get_chart_graph
# config
data = config.CONFIG

import os
print(os.getcwd())

#async_mode = 'eventlet'
app = Flask(__name__)
swagger = Swagger(app)
cors = CORS(app)
print('mongodb://' + data["mongo_host"] + ':' + str(data["mongo_port"]) + '/' + data["mongo_db"])
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://' + data["mongo_host"] + ':' + str(data["mongo_port"]) + '/' + data["mongo_db"]
}

app.config['CORS_HEADERS'] = 'Content-Type'

initialize_db(app)

# create a new activity
@app.route('/activities', methods=['POST'])
@cross_origin()
def add_activitie_route():
    """
    Create a new activity
    This endpoint will create a new activity
    ---
    tags:
      - activities
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: The name of the activity
      - name: file_audio
        in: formData
        type: file
        required: true
        description: The audio file of the activity
      - name: file_video
        in: formData
        type: file
        required: true
        description: The video file of the activity
    responses:
      200:
        description: Activity created
      400:
        description: Error
    """
    return create_activity()

#get all activities
@app.route('/activities', methods=['GET'])
@cross_origin()
def get_activities_route():
    """
    Get all activities
    This endpoint will return all activities
    ---
    tags:
      - activities
    responses:
      200:
        description: Activities
      400:
        description: Error
    """
    return get_activities()

#get an activity
@app.route('/activities/<string:name>', methods=['GET'])
@cross_origin()
def get_activity_route(name):
    """
    Get an activity
    This endpoint will return an activity
    ---
    tags:
      - activities
    responses:
      200:
        description: Activity
      400:
        description: Error
    """
    return get_activity(name)

#delete an activity
@app.route('/activities/<string:name>', methods=['DELETE'])
@cross_origin()
def delete_activity_route(name):
    """
    Delete an activity
    This endpoint will delete an activity
    ---
    tags:
      - activities
    responses:
        200:
            description: Activity deleted
        400:
            description: Error
        505:
            description: Error
        """
    return delete_activity(name)

#get an activity file
@app.route('/activities/<string:name>/<string:filename>', methods=['GET'])
@cross_origin()
def get_activity_file_route(name, filename):
    """
    Get an activity file
    This endpoint will return an activity file
    ---
    tags:
      - activities
    responses:
      200:
        description: Activity file
      400:
        description: Error
    """
    return get_activity_file(name, filename)

#create a new analysis
@app.route('/analysis', methods=['POST'])
@cross_origin()
def add_analysis_route():
    """
    Create a new analysis
    This endpoint will create a new analysis
    ---
    tags:

        - analysis
    parameters:
        - name: name    
            in: formData    
            type: string                            
            required: true
            description: The name of the analysis
    """
    return create_analysis()

#get all analysis
@app.route('/analysis', methods=['GET'])
@cross_origin()
def get_analysis_route():
    """
    Get all analysis
    This endpoint will return all analysis
    ---
    tags:
      - analysis
    responses:
      200:
        description: Analysis
      400:
        description: Error
    """
    return get_analysis()

#get an analysis
@app.route('/analysis/<string:id_analysis>', methods=['GET'])
@cross_origin()
def get_analysis_name_route(id_analysis):
    """
    Get an analysis
    This endpoint will return an analysis
    ---
    tags:
      - analysis
    parameters:
      - id_analysis: id of the analysis
    responses:
      200:
        description: Analysis
      400:
        description: Error
    """
    return get_analysis_by_id(id_analysis)

#delete an analysis
@app.route('/analysis/<string:name>', methods=['DELETE'])
@cross_origin()
def delete_analysis_route(name):
    """
    Delete an analysis
    This endpoint will delete an analysis
    ---
    tags:
      - analysis
    responses:
        200:
            description: Analysis deleted
        400:
            description: Error
        505:
            description: Error
        """
    return delete_analysis(name)

# get results
@app.route('/results', methods=['GET'])
@cross_origin()
def get_results_route():
    """
    Get results
    This endpoint will return results
    ---
    tags:
      - results
    responses:
      200:
        description: Results
      400:
        description: Error
    """
    return get_results()

# create a new indicator measure
@app.route('/indicator-measure/<string:indicator_name>', methods=['POST'])
@cross_origin()
def add_indicator_measure_route(indicator_name):
    """
    Create a new indicator measure
    This endpoint will create a new indicator measure
    ---
    tags:
      - indicator-measure
    parameters:
      - indicator_name: name of the indicator
    responses:
      200:
        description: Indicator measure created
      400:
        description: Error
    """
    return create_indicator_measure(indicator_name)

# get indicator measure by id analysis
@app.route('/indicator-measure/<string:indicator_name>/<string:id_analysis>', methods=['GET'])
@cross_origin()
def get_indicator_measure_route(indicator_name, id_analysis):
    """
    Get indicator measure
    This endpoint will return indicator measure
    ---
    tags:
      - indicator-measure
    parameters:
      - indicator_name: name of the indicator
      - id_analysis: id of the analysis
    responses:
      200:
        description: Indicator measure
      400:
        description: Error
    """
    return get_indicator_measure(indicator_name, id_analysis)

# download csv indicator measure by id analysis 
@app.route('/indicator-measure/<string:indicator_name>/<string:id_analysis>/csv', methods=['GET'])
@cross_origin()
def download_indicator_measure_csv_route(indicator_name, id_analysis):
    """
    Download csv indicator measure
    This endpoint will download csv indicator measure
    ---
    tags:
      - indicator-measure
    parameters:
      - indicator_name: name of the indicator
      - id_analysis: id of the analysis
    responses:
      200:
        description: Indicator measure csv
      400:
        description: Error
    """
    return download_indicator_measure_csv(indicator_name, id_analysis)

# charts
@app.route('/chart/<string:chart_name>/<string:id_analysis>/', methods=['GET'])
@cross_origin()
def get_chart1_route(chart_name, id_analysis):
    if chart_name == "chart1":
      return get_chart_segmentation(id_analysis)  
    elif chart_name == "chart2":
      return get_chart_vocal_activity(id_analysis)  
    elif chart_name == "chart3":
      return get_chart_apm(id_analysis)  
    elif chart_name == "chart4":
      return get_chart_head_sight(id_analysis)
    elif chart_name == "chart5":
      return get_chart_graph(id_analysis)

# run server
@app.route('/')
def hello():
    return 'server is running'

if __name__ == '__main__':
    app.run(debug=data["api_debug"], host=data["api_host"], port=data["api_port"])