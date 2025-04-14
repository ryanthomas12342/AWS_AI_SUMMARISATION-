import boto3
import json
import requests

def lambda_handler(event, context):
    print(event)
    s3 = boto3.client('s3')

    # Get transcript details from the event
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    try:
        # Fetch transcript file from S3
        response = s3.get_object(Bucket=input_bucket, Key=object_key)
        transcript_data = json.loads(response['Body'].read().decode('utf-8'))
        transcript_text = transcript_data['results']['transcripts'][0]['transcript']

        # Send transcript to Mistral for summarization
        mistral_endpoint = "http://localhost:11434/api/generate"  # Adjust if different

        payload = {
            "model": "mistral",
            "prompt": f"""
You are an expert summarizer tasked with condensing transcripts into clear, actionable summaries. Format the summary pointwise using bullet points. Ensure the summary includes:

🗓️ Date and Time: Extract the meeting or call time.
👥 Participants: List all participants mentioned and their roles.
🔑 Key Discussion Points: Summarize the main topics discussed, highlighting any debates or alternate viewpoints.
📋 Action Items: Specify tasks assigned, responsible individuals, and deadlines.
💡 Decisions Made: Document decisions made, including the rationale behind them.
❓ Open Questions: Note any unresolved issues or follow-up questions raised during the conversation.

For phone calls, focus on client needs, challenges discussed, and proposed solutions. For meetings, emphasize collaboration, task delegation, and strategic decisions. Ensure the tone is professional and concise.

Transcript:
{transcript_text}
            """,
            "stream": True
        }

        summary = ""

        with requests.post(mistral_endpoint, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    content = chunk.get("response", "")
                    summary += content

        # Upload summary to S3
        output_bucket = 'audio-summary-output'
        summary_key = object_key.replace('transcripts/', 'summaries/').replace('.json', '.txt')

        s3.put_object(Bucket=output_bucket, Key=summary_key, Body=summary)

        return {'statusCode': 200, 'body': "Summary completed"}

    except Exception as e:
        print(f"Error processing transcript: {str(e)}")
        return {'statusCode': 500, 'body': f"Error: {str(e)}"}

# aws lambda update-function-code --function-name process_transcript_function --zip-file fileb://function.zip
