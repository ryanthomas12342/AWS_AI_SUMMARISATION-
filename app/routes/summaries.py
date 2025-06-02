from flask import Blueprint, jsonify, current_app, render_template,send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.routes.payment import check_payment
import boto3
import os
import io

# Change blueprint name to avoid conflict with URL prefix
summaries_bp = Blueprint('summaries_bp', __name__)

OUTPUT_BUCKET = os.getenv('OUTPUT_BUCKET')
s3 = boto3.client('s3', region_name='ap-south-1')



@summaries_bp.route('/', methods=['GET'])
@jwt_required()
def list_summaries():
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        print(f"User ID from token - type: {type(user_id)}, value: {user_id}")
        
        # Convert string ID to integer if needed
        if isinstance(user_id, str):
            user_id = int(user_id)
            print(f"User ID after conversion - type: {type(user_id)}, value: {user_id}")
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        prefix = f'users/{user_id}/summaries/'
        response = s3.list_objects_v2(Bucket=OUTPUT_BUCKET, Prefix=prefix)

        summaries = []
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                filename = key.split('/')[-1]
                last_modified = obj['LastModified'].isoformat()
                size = round(obj['Size']/1024, 2)

                summaries.append({
                    "key": key,
                    "filename": filename,
                    "last_modified": last_modified,
                    "size": size
                })

        print(f"Rendering template with summaries: {summaries}")  # Debug print
        return render_template('summaries.html', summaries=summaries, username=user.username)
    
    except Exception as e:
        current_app.logger.error(f"Error listing summaries: {str(e)}")
        return jsonify({'error': f'Failed to list summaries: {str(e)}'}), 500



@summaries_bp.route('/download/<path:summary_key>')
@jwt_required()
def download_summary(summary_key):

    print(f"downloading summary file {summary_key}")

    try:

        response,status_code=check_payment()

        resp=response.get_json()

        if status_code!=200 or not resp.get('has_paid'):
            return jsonify({'error':'Payment required'}),403
        bucket_name=os.getenv('OUTPUT_BUCKET')
        response=s3.get_object(Bucket=bucket_name,
                               Key=f'{summary_key}')
        
        return send_file(
            io.BytesIO(response['Body'].read()),
            mimetype='text/plain',
            as_attachment=True,
                        download_name=f'{summary_key}.txt'

        )
        
        return jsonify({"Error":"the summary file as not founf"}),403
    
    except Exception as e:
        current_app.logger.error(f"Error donwloading the summary file :{str(e)}")
        return jsonify({"erorr":"failed to downlaod the summary file "}),500

    




        



            




                



