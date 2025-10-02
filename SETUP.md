# DUAA Lesson Content Generator Setup

## Environment Variables Required

Create a `.env` file in the project root with the following variables:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Database Configuration
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/database_name

# Pipeline Configuration (if running main.py directly)
PIPELINE_INPUT={"run_type": "generate_lesson_content"}

# AWS Configuration (if using AWS services)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_DEFAULT_REGION=us-east-1
```

## Database Setup

1. Start PostgreSQL database:
```bash
docker run --name duaa_db -e POSTGRES_DB=duaa_db -e POSTGRES_USER=duaa -e POSTGRES_PASSWORD=your_password -p 5432:5432 -d postgres:latest
```

2. The questions table will be created automatically when the question generation runs.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install duaa_edtools package:
```bash
cd ../duaa_edtools
pip install -e .
```

## Usage

Run the main pipeline:
```bash
python -m src.main
```

## Question Generation

The question generation feature is automatically integrated into the main pipeline and will:
- Generate multiple choice questions for lesson topics
- Store questions in PostgreSQL database
- Use OpenAI GPT-3.5-turbo for question generation
