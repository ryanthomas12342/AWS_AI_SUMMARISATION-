import boto3
import os

sqs=boto3.client('sqs',region_name='us-east-1')

response=sqs.create_queue(
    QueueName='transcript-processing-queue',
    Attributes={
        "DelaySeconds":"0",
        "VisibilityTimeout":"300",
        "MessageRetentionPeriod": "86400"  # 1 day
    }


)

queue_url=response['QueueUrl']

print(f"Queue created:{queue_url}")