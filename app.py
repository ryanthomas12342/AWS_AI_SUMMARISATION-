from flask import Flask ,request,jsonify,render_template 

import boto3
import os
import threading
import worker
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)

s3 = boto3.client('s3')


@app.route("/")
def index():
    return "Audio Processsing Worklfow-Status:Running"



@app.route('/start_worker',methods=['POST'])
def start_worker():
    worker_thread=threading.Thread(target=worker.poll_sqs_queue)
    worker_thread.daemon=True
    worker_thread.start()
    return jsonify({
        "status":"Worker started sucessfully"
    })


if __name__ == '__main__':
    # Start the worker thread automatically when the app starts
    worker_thread = threading.Thread(target=worker.poll_sqs_queue)
    worker_thread.daemon = True
    worker_thread.start()
    
    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)