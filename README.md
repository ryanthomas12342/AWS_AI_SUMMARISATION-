# Audio Transcription and Summarization Service

A comprehensive Flask-based web application that provides audio transcription and intelligent summarization services using AWS services and Mistral AI.

## 🔄 Features

### Core Functionality

- Audio file upload and processing (MP3, WAV formats)
- Automatic transcription of audio files
- AI-powered summarization using Mistral model
- User authentication and authorization
- Payment integration for premium features
- Secure file storage and management

### AWS Services Integration

- **Amazon S3**:
  - Raw audio storage
  - Transcript storage
  - Summary storage
- **Amazon Transcribe**:
  - For Converting Audio to Text
- **Amazon SQS**:
  - Message queue for processing transcripts
  - Asynchronous processing workflow
- **Amazon DynamoDB**:
  - User payment tracking
  - Transaction management
- **AWS Lambda**:
  - Serverless transcript processing
  - Event-driven architecture

### AI/ML Features

- Local Mistral model integration for summarization
- Structured summary format including:
  - Date and Time
  - Participants and Roles
  - Key Discussion Points
  - Action Items
  - Decisions Made
  - Open Questions

## 🛠️ Technical Stack

### Backend

- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Flask-JWT-Extended (Authentication)
- Flask-Bcrypt (Password hashing)
- Flask-CORS (Cross-Origin Resource Sharing)

### AWS Services

- S3 for file storage
- SQS for message queuing
- DynamoDB for payment tracking
- Lambda for serverless processing

### AI/ML

- Mistral AI for text summarization
- Custom prompt engineering for structured summaries

## 📋 Prerequisites

- Python 3.x
- AWS Account with appropriate permissions
- Mistral AI model running locally
- Virtual environment (recommended)

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key
FLASK_DEBUG=True
JWT_SECRET_KEY=your-jwt-secret-key

# AWS Configuration
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-south-1
S3_BUCKET=your-bucket-name
UPLOAD_BUCKET=your-upload-bucket
OUTPUT_BUCKET=your-output-bucket
SQS_QUEUE_URL=your-queue-url

# Database Configuration
DATABASE_URL=your-database-url

# Payment Configuration
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
```

## 🚀 Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up AWS services:

   - Create S3 buckets for upload and output
   - Set up SQS queue
   - Configure DynamoDB table
   - Set up Lambda function

5. Start the application:

```bash
python wsgi.py
```

