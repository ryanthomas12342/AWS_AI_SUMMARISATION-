from flask import Blueprint, jsonify, current_app, render_template,send_file,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
import boto3
import os
import io
from datetime import datetime
import stripe


STRIPE_PUBLIC_KEY=os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY=os.getenv('STRIPE_SECRET_KEY')
stripe.api_key=STRIPE_SECRET_KEY


dynamodb=boto3.resource('dynamodb',region_name='us-east-1')
payment_table=dynamodb.Table('user_payments')


payment_bp=Blueprint('payment_bp',__name__)

# @payment_bp.route('/create-checkout',methods=['POST'])
# @jwt_required()
# def create_cehckout():

#     try:
#         user_id=get_jwt_identity()

#         checkout_session=stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[]
#         )

@payment_bp.route('/check-payment',methods=['GET'])
@jwt_required()
def check_payment():

    try:
        user_id=get_jwt_identity()
        print("At the checking dynamodbtable part")


        response = payment_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='#status = :status',
    ExpressionAttributeValues={
        ':uid': str(user_id),
        ':status': 'completed'
    },
    ExpressionAttributeNames={
        '#status':'status'
    }

)

        print("this is the resp",response)

        has_paid=len(response['Items'])>0
        print(has_paid)
        return jsonify({'has_paid':has_paid}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    

@payment_bp.route('/create-checkout-session',methods=['POST'])
@jwt_required()
def create_checkout_session():

    print("hello")
    try:

        user_id=get_jwt_identity()

        checkout_session=stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data':{
                    'currency':'inr',
                    'product_data':{
                        'name':'Unlimited Download Acess',
                        'description':'One time payment for unlimited downloads'
                    },
                    'unit_amount':5000,

                },
                'quantity':1,
            }],
            mode='payment',
            success_url='http://localhost:5000/payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5000/payment/cancel',
            metadata={
                'user_id':user_id
            }
        )

        print(checkout_session.id)

        return jsonify({'url':checkout_session.url}),200
    except Exception as e:
        print(e)
        return jsonify({'error':str(e)}),500



@payment_bp.route('/success')
def success():
    try:
        print("hello")
        session_id=request.args.get('session_id')        
        session=stripe.checkout.Session.retrieve(session_id)

        if session.payment_status =='paid':
            payment_table.put_item(

                Item={
                    'user_id':session.metadata['user_id'],
                    'payment_id':session.id,
                    'amount':session.amount_total,
                    'status':'completed',
                    'timestamp':datetime.now().isoformat()


                }

            )

            return render_template('payment_success.html',message='Payment successfull.You can now go and download your summaries')
    except Exception as e:
        return render_template('payment_error.html',message=f'Payment uncessfull.Error : {str(e)}')
    


@payment_bp.route('/cancel')
def payment_cancel():

    return render_template('payment_success.html',message='Payment has been cancelled . Try again')
    
