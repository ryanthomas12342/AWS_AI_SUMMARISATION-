from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.services.worker import poll_sqs_queue
import threading

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@jwt_required()
def dashboard():
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))

        print("User is here ")

        print(user)
        
        if not user:
            print("User is not here ")
            return redirect(url_for('auth.login_page'))
            
        return render_template('dashboard.html', username=user.username)
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return redirect(url_for('auth.login_page'))



@dashboard_bp.route('/start_worker', methods=['POST'])
@jwt_required()
def start_worker():
    worker_thread = threading.Thread(target=poll_sqs_queue)
    worker_thread.daemon = True
    worker_thread.start()
    return jsonify({
        "status": "Worker started successfully"
    }) 