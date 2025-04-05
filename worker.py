import boto3
import json
import time
import os
from model import summarize_transcript

# Initialize AWS clients
sqs = boto3.client('sqs', region_name='us-east-1')
s3 = boto3.client('s3')

# Queue URL - replace with your actual queue URL
QUEUE_URL = os.getenv("QUEUE_URL")
OUTPUT_BUCKET = os.getenv("OUTPUT_BUCKET")

def process_transcript(transcript_bucket, transcript_key):
    """Process a transcript and generate a summary using local Mistral model"""
    try:
        # Get transcript from S3
        response = s3.get_object(Bucket=transcript_bucket, Key=transcript_key)
        transcript_data = json.loads(response['Body'].read().decode('utf-8'))
        transcript_text = transcript_data['results']['transcripts'][0]['transcript']
        
        # Use the summarize_transcript function from model.py
        summary = summarize_transcript(transcript_text)
        
        if summary:
            # Save summary to S3
            summary_key = transcript_key.replace('transcripts/', 'summaries/').replace('.json', '.txt')
            s3.put_object(Bucket=OUTPUT_BUCKET, Key=summary_key, Body=summary)
            
            print(f"Summary saved to s3://{OUTPUT_BUCKET}/{summary_key}")
            return True
        else:
            print("Failed to generate summary")
            return False
    except Exception as e:
        print(f"Error processing transcript: {str(e)}")
        return False

def poll_sqs_queue():
    """Poll SQS queue for transcript messages"""
    print("Starting SQS polling...")
    while True:
        try:
            # Receive message from SQS queue with long polling
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                AttributeNames=['All'],
                MaxNumberOfMessages=1,
                MessageAttributeNames=['All'],
                WaitTimeSeconds=20  # Long polling
            )
            
            if 'Messages' in response:
                for message in response['Messages']:
                    print("Message received from SQS")
                    # Process the message
                    body = json.loads(message['Body'])
                    
                    # Extract S3 event details
                    s3_event = json.loads(body['Message']) if 'Message' in body else body
                    
                    if 'Records' in s3_event:
                        for record in s3_event['Records']:
                            if record['eventName'].startswith('ObjectCreated:'):
                                bucket = record['s3']['bucket']['name']
                                key = record['s3']['object']['key']
                                
                                print(f"Processing transcript: s3://{bucket}/{key}")
                                # Process the transcript
                                if process_transcript(bucket, key):
                                    # Delete the message from the queue
                                    sqs.delete_message(
                                        QueueUrl=QUEUE_URL,
                                        ReceiptHandle=message['ReceiptHandle']
                                    )
                                    print("Message processed and deleted from queue")
            
            # Small delay to prevent tight looping
            time.sleep(1)
        except Exception as e:
            print(f"Error polling SQS: {str(e)}")
            time.sleep(5)  # Longer delay on error

if __name__ == "__main__":
    # Replace with your actual account ID
    QUEUE_URL = QUEUE_URL.replace("YOUR_ACCOUNT_ID", os.environ.get("AWS_ACCOUNT_ID", ""))
    poll_sqs_queue()
