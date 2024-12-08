from flask import Flask, json, request, jsonify, render_template
import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import dpdc_amr.utils
from werkzeug.utils import secure_filename
from dpdc_amr.testMyML import getModel,examine
from dpdc_amr.digitExtractions import getYoloModel, extract_digits
from waitress import serve



app = Flask(__name__, template_folder='./templates')


app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 16 MB

model = getModel()
yModel = getYoloModel()


app.secret_key = "caircocoders-ednalan"



UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static\\uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/batch_proc')
def batch_proc():
    return render_template('batch_proc.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files')

    imgflg=False
    if 'imgflg' in request.form:
        imgflg=True

    errors = {}
    success = False
    messages=[]

    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                result=examine(model,os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except Exception as e:
                print('Error in Image Classification!')
                errors['message'] = 'Error in Image Classification!'
                resp = jsonify(errors)
                resp.status_code = 500
                return resp
            obj= dpdc_amr.utils.Message(filename=filename, cls=result,reading='',img='')
            if result=='Meter':
                try:
                    digits,b64=extract_digits(yModel, os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                              0.4,imgflg)
                except:
                    print('Error in Reading!')
                    errors['message'] = 'Error in Reading!'
                    resp = jsonify(errors)
                    resp.status_code = 500
                    return resp

                obj.reading=digits
                obj.img=b64
            messages.append(obj.__dict__)
            success = True
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : messages})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


@app.route('/upload_batch', methods=['POST'])
def upload_batch():
    # check if the post request has the file part
    if 'files' not in request.files:
        resp = jsonify({'message': 'No file part in the request!'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files')



    imgflg = False
    if 'imgflg' in request.form:
        imgflg = True

    errors = {}
    success = False
    messages = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                result = examine(model, os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except Exception as e:
                result='Error'

            obj = dpdc_amr.utils.Message(filename=filename, cls=result, reading='', img='')
            if result == 'Meter':
                try:
                    digits, b64 = extract_digits(yModel, os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                                 0.4, imgflg)
                except:
                    print('Error in Reading!')
                    digits='Error'
                    b64=''

                obj.reading = digits
                obj.img = b64
            messages.append(obj.__dict__)
            success = True
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message': messages})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp






if __name__ == '__main__':
    app.run(debug=True)


def main():
    print("Server has started!")
    print("* Running on http://127.0.0.1:5151")
    serve(app, host='0.0.0.0', port=5151)