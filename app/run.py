import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.worker import poll_sqs_queue
import threading
from flask import render_template, redirect, url_for, jsonify

from app.models.user import db



app=create_app()





@app.route("/")
def index():
    return redirect(url_for('auth.login_page'))
@app.route('/start_worker', methods=['POST'])
def start_worker():
    worker_thread = threading.Thread(target=poll_sqs_queue)
    worker_thread.daemon = True
    worker_thread.start()
    return jsonify({
        "status": "Worker started successfully"
    })

def create_worker_thread():
    worker_thread = threading.Thread(target=poll_sqs_queue)
    worker_thread.daemon = True
    worker_thread.start()
    return worker_thread

if __name__ == '__main__':
    # Create the Flask application
    

    with app.app_context():
        db.create_all()


    
    # Start the worker thread
    worker_thread = create_worker_thread()
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000) 