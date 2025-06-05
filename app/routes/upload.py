from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import boto3
import os
import json
from dotenv import load_dotenv
load_dotenv()

upload_bp = Blueprint('upload', __name__)

UPLOAD_BUCKET = os.getenv('UPLOAD_BUCKET')

@upload_bp.route('/uploadaudio', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        userid = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({"msg": "No file was uploaded"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"msg": "No selected file"}), 400
            
        current_app.logger.info(f"Received file: {file.filename}, Content Type: {file.content_type}")

        # Validate file type
        allowed_extensions = {'mp3', 'wav'}
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return jsonify({"msg": "File format not supported. Please upload MP3 or WAV files only"}), 400

        try:
            # Initialize S3 client
            s3 = boto3.client('s3',region_name='ap-south-1')
            
            filename = secure_filename(file.filename)
            
            s3_key = f'users/{userid}/audio/{filename}'
            
            current_app.logger.info(f"Attempting S3 upload to bucket: {UPLOAD_BUCKET}, key: {s3_key}")
            
            # Upload to S3
            
            resp=s3.put_object(Bucket=UPLOAD_BUCKET, Key=s3_key, Body=file)
            print(resp)    



            
            current_app.logger.info(f"File uploaded successfully to S3: {s3_key}")
            
            return jsonify({
                "msg": "File uploaded successfully",
                "filename": filename,
                "s3_key": s3_key
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"S3 upload error: {str(e)}")
            return jsonify({"msg": "Error uploading file to storage", "error": str(e)}), 500
            
    except Exception as e:
        current_app.logger.error(f"Upload route error: {str(e)}")
        return jsonify({"msg": "Server error", "error": str(e)}), 500



