import boto3
import os

s3_client=boto3.client('s3',region_name='ap-south-1')
polly_client=boto3.client('polly',region_name='ap-south-1')


def lambda_handler(event):
    try:
        record=event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']


        if not key.endswith('.txt'):
            return {'message':'Only txt files can be processes','statusCode':403};
        
        resp=s3_client.get_object(Bucket=bucket,Key=key)
        summary_text=resp['Body'].read().decode('utf-8')


        with polly_client.synthesize_speech(
            Text=summary_text,
            OutputFormat='mp3',
            VoiceId='Joanna',
        )['AudioStream'] as audio_bytes:
            
            audio_stream=audio_bytes.read()
            


        audio_key=key.replace('.txt','.mp3')
        audio_bucket=os.environ['AUDIO_BUCKET']

        s3_client.put_object(
            Bucket=audio_bucket,
            Key=audio_key,
            Body=audio_stream,
            ContentType='audio/mpeg'
        )
        print(f"Audio file saved: s3://{audio_bucket}/{audio_key}")
        return {'statusCode': 200, 'body': 'Audio files created successfully.'}




    except Exception as e:
        print(str(e))
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}
    



