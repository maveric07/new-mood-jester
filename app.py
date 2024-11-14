from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import cv2
from deepface import DeepFace
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set the upload folder path
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the uploads directory if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return "Hello World"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        img = cv2.imread(filepath)
        result = DeepFace.analyze(img,actions=['emotion'])
        return jsonify({'success': f'{result[0][ 'dominant_emotion' ]}'}), 200
    

