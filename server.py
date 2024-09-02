from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from process import process_images
import os
import uuid
from model import db, File_status
from flask_migrate import Migrate 
from celery_config import celery_init_app
from util import validate_csv_format

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

PROCESSED_FOLDER = 'processed'
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Celery Setup
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://127.0.0.1:6379/0",
        result_backend="redis://127.0.0.1:6379/0",
    ),
)
celery = celery_init_app(app)

#Database Setup
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/upload", methods=['POST'] )
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
                
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.csv'):

        # Checking csv data format
        if not (is_valid := (result := validate_csv_format(file))[0]):
            return jsonify({'error': result[1]}), 400

        file.seek(0)

        if not os.path.exists(app.config['PROCESSED_FOLDER']):
            os.makedirs(app.config['PROCESSED_FOLDER'])

        filename = secure_filename(file.filename)
        request_id = str(uuid.uuid4())

        os.makedirs(app.config['PROCESSED_FOLDER']+ "\\" + request_id)

        file_path = os.path.join(app.config['PROCESSED_FOLDER'], request_id, request_id + '_' + filename)
        file.save(file_path)

        #Updating Database with the status
        file_status = File_status(id=request_id, original_file_path=os.path.abspath(file_path), status='Pending', final_file_path='')
        db.session.add(file_status)
        db.session.commit()

        #Calling Celery to process the image
        process_images.delay(request_id, file_path, app.config['PROCESSED_FOLDER']+"\\"+request_id, )

        return jsonify({'Request_id': request_id}), 200
        
    return jsonify({'error': 'Inavlid file format'}), 400

@app.route('/status', methods=['GET'])
def status():

    request_id = request.args.get('id')
    file_status = File_status.query.filter_by(id=request_id).first()
    if file_status:
        return jsonify({
            'Request_id': file_status.id,
            'Status': file_status.status,
            'Output': f"{file_status.final_file_path}"
        }), 200
    else:
        return jsonify({'error': 'Request ID not found'}), 404
    
if __name__ == "__main__":
    app.run()
