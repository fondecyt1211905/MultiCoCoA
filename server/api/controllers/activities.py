import shutil, json
from flask import request, jsonify, Response, send_from_directory
from database.models import Activity, File
import os, wave, cv2

def create_activity():
    if request.method == "POST":
        activities = Activity.objects()
        name = str(request.form["name"])
        numParticipants = int(request.form["numParticipants"])
        if not name in activities:
            #crear actividad
            activity = Activity.objects.create(name=name, numParticipants=numParticipants)
            print(os.getcwd())
            id=str(activity.id)
            #crear carpeta con el id de la actividad
            os.makedirs(os.path.join(os.getcwd(),"data", id))
            #guardar archivos en la carpeta
            file_video = None
            file_audio = None
            try:
                file_audio = request.files['file_audio']
                file_audio.save(os.path.join(os.getcwd(),"data", id, "audio.wav"))
                # longitud del audio
                audio = wave.open(os.path.join(os.getcwd(),"data", id, "audio.wav"), 'r')
                frames = audio.getnframes()
                rate = audio.getframerate()
                duration = frames / float(rate)
                audio.close()
                #guardar longitud del audio
                audiofile = File(filename="audio.wav", type="audio", length=duration, frames=frames, rate=rate)
                activity.files.append(audiofile)
            except KeyError:
                pass
            except FileNotFoundError:
                return jsonify({'error': 'Error al subir actividad!'}), 400
            try:
                file_video = request.files['file_video']
                file_video.save(os.path.join(os.getcwd(),"data", id, "video.mp4"))
                # longitud del video
                cap = cv2.VideoCapture(os.path.join(os.getcwd(),"data", id, "video.mp4"))
                total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                duration = total_frame / fps
                cap.release()
                #guardar longitud del video
                videofile = File(filename="video.mp4", type="video", length=duration, frames=total_frame, fps=fps)
                activity.files.append(videofile)
            except KeyError:
                pass
            except FileNotFoundError:
                return jsonify({'error': 'Error al subir actividad!'}), 400
            activity.save()
            return jsonify({'message': 'Actividad subida correctamente' }), 200
        return jsonify({'message': 'Activity created'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_activities():
    if request.method == "GET":
        activities = Activity.objects()
        return activities.to_json(), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_activity(name):
    if request.method == "GET":
        # obtener primera actividad que coincida con el nombre
        try:
            activity = Activity.objects(name=name).first().to_json()
        except AttributeError:
            return jsonify({'message': 'Activity not found'}), 404
        return Response(activity, mimetype="application/json", status=200)
    else:
        return jsonify({'message': 'Bad request'}), 400
    
def delete_activity(name):
    if request.method == "DELETE":
        activity = Activity.objects(name=name).first()
        try:
            shutil.rmtree(os.path.join(os.getcwd(),"data", str(activity.id)))
        except FileNotFoundError:
            pass
        activity.delete()
        return jsonify({'message': 'Activity deleted'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_activity_file(name, filename):
    if request.method == "GET":
        activity = Activity.objects(name=name).first()
        if activity:
            for file in activity.files:
                if file.filename == filename:
                    return send_from_directory(os.path.join(os.getcwd(),"data", str(activity.id)), filename, as_attachment=True)
            return jsonify({'message': 'File not found'}), 404
        return jsonify({'message': 'Activity not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400
