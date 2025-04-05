import requests
import json

def summarize_transcript(transcript_text):
    """
    Send a transcript to the local Mistral model and get a summary
    """
    endpoint = "http://localhost:11434/api/generate"
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

        Transcript:
        {transcript_text}
        """,
        "stream": True
    }

    try:
        summary = ""
        with requests.post(endpoint, json=payload, stream=True, timeout=120) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    summary += chunk.get("response", "")
        return summary
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Test the function with a sample transcript
    sample_transcript = "This is a test transcript."
    summary = summarize_transcript(sample_transcript)
    print("\n📝 Final Summary:\n")
    print(summary.strip())
