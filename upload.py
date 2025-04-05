import boto3

print("Initializing S3 client...")
s3 = boto3.client('s3', region_name='us-east-1')

# Define bucket and file details
bucket_name = 'audio-processing-raw'
file_path = 'upload/resources_RC_Conversation_Sample.mp3'
s3_key = 'resources_RC_Conversation_Sample.mp3'  # Key to store in S3

print("Starting file upload...")
try:
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"✅ File uploaded successfully to s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"❌ Upload failed: {e}")
