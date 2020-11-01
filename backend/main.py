from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file
import hydrology
import json
import os
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = "userdata"


class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/custom_data', methods=['GET', 'POST'])
def file_upload():
    target="userdata"
    if not os.path.isdir(target):
        os.mkdir(target)
    try:
        infil = request.files['infil'] 
        forma = infil.filename.split('.')[1] 
        infil.save("/".join([target,"infil."+forma]))
        infil = "/".join([target,"infil."+forma])
    except:
        infil = None
    try:
        soil = request.files['soil']
        forma = soil.filename.split('.')[1] 
        soil.save("/".join([target,"soil."+forma]))
        soil = "/".join([target,"soil."+forma])
    except:
        soil = None
    rain = request.form['rain']
    dem = request.files['dem']
    forma = dem.filename.split('.')[1] 
    dem.save("/".join([target,"dem."+forma]))
    dem = "/".join([target,"dem."+forma])
    filename = hydrology.custom_hydrology(rain, dem, infil, soil)
    if isinstance(filename, list):
        return "An error occured",200
    return send_file(filename, mimetype='image/jpg'), 200
@app.route('/get_map', methods=['GET'])
def runner():
    # needs city and date as param
    centre, bbox, matrix = hydrology.map_hydrology("mumbai", "05-11-2020")
    if len(matrix) == 0:
        return jsonify({"err": "An unexpected error occured"}), 500
    else:
        return jsonify({"centre": centre, "bbox": bbox, "mat": matrix.tolist()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
