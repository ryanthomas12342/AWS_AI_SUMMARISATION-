from flask import Blueprint, render_template, redirect, url_for, jsonify
from app.services.worker import poll_sqs_queue
import threading

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@dashboard_bp.route('/')
def index():
    return redirect(url_for('auth.login_page'))

@dashboard_bp.route('/start_worker', methods=['POST'])
def start_worker():
    worker_thread = threading.Thread(target=poll_sqs_queue)
    worker_thread.daemon = True
    worker_thread.start()
    return jsonify({
        "status": "Worker started successfully"
    }) 