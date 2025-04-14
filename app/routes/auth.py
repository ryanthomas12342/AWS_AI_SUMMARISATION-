from flask import Blueprint,request,jsonify,render_template

from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.models.user import User
from app import db

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


    

@auth_bp.route('api/login',methods=['POST'])
def login():
    data=request.get_json()
    username =data.get('username')
    password=data.get('password')

    if not (username and password):
        return jsonify({"msg":"THe requried feilds weren't provided"}),400

    user=User.query.filter_by(username=username).first()

    if not user or not  user.check_password(password):
        return jsonify({"msg":"You have provided an invalid password or username"}),401
    
    access_token=create_access_token(identity=str(user.id))
    return jsonify({"token": access_token, "user_id": str(user.id), "username": user.username}), 200



@auth_bp.route('/profile')
@jwt_required()
def profile():

    user_id=get_jwt_identity()
    user=User.query.get(user_id)

    return jsonify({"username":user.username,"email":user.email}),200


