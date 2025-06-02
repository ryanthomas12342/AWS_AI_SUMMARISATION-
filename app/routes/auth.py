from flask import Blueprint,request,jsonify,render_template

from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity, set_access_cookies, unset_jwt_cookies
from app.models.user import User
from app import db, bcrypt

#blueprint for auth routes 
auth_bp=Blueprint('auth',__name__)


@auth_bp.route('/signup',methods=['GET'])
def signup_page():
    return render_template('signup.html')

@auth_bp.route('/login',methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_bp.route('api/register',methods=['POST'])
def register():
    data=request.get_json()

    # Check if user already exists

    username =data.get('username')
    email=data.get('email')
    password=data.get('password')

    if not username or  not email or not password :
        return jsonify({"msg":"the required credentials werent provided"}),400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg":"Username or email aldready exists"}),409
    new_user=User(username=username,email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg":"Usser create sucessfully"}),201


    

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Create access token with string user ID
        access_token = create_access_token(identity=str(user.id))
        print(f"Created access token: {access_token[:20]}...")  # Debug print
        
        # Create response
        response = jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
        
        # Set cookie directly
        response.set_cookie(
            'access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=3600
        )

        print(response)
        
        print("Cookie set in response")  # Debug print
        return response

    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'An error occurred during login'}), 500

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response

@auth_bp.route('/profile')
@jwt_required()
def profile():

    user_id=get_jwt_identity()
    user=User.query.get(user_id)

    return jsonify({"username":user.username,"email":user.email}),200


