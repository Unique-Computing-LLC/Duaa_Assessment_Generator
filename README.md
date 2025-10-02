# DUAA Lesson Content Generator

A comprehensive lesson content generation system that creates educational slides and automatically generates multiple choice questions using OpenAI's GPT models.

## Features

- **Slide Generation**: Creates educational slides from lesson content
- **Question Generation**: Automatically generates multiple choice questions for lesson topics
- **Database Integration**: Stores questions in PostgreSQL with JSONB format
- **AWS Integration**: Supports S3 storage and AWS Secrets Manager
- **Pipeline Integration**: Seamlessly integrates with existing lesson generation workflow

## Question Generation Feature

The system automatically generates educational multiple choice questions for any topic:

- **AI-Powered**: Uses OpenAI GPT-3.5-turbo for intelligent question generation
- **Database Storage**: Questions stored in PostgreSQL with proper schema
- **JSONB Format**: Flexible storage format for question data
- **Error Handling**: Robust error handling ensures pipeline continues even if question generation fails

### Question Format

```json
{
  "question": "What is the capital of France?",
  "options": {
    "A": "London",
    "B": "Berlin", 
    "C": "Paris",
    "D": "Madrid"
  },
  "correct_answer": "C"
}
```

## Quick Start

1. **Setup Environment Variables** (see SETUP.md for details)
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Start Database**: Use Docker to run PostgreSQL
4. **Run Pipeline**: `python -m src.main`

## Database Schema

The system creates a `questions` table with the following structure:

```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_json JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration

See `SETUP.md` for detailed configuration instructions including:
- Environment variables
- Database setup
- AWS configuration
- Pipeline configuration

## Dependencies

- Python 3.7+
- PostgreSQL
- OpenAI API
- SQLAlchemy
- FastAPI (for API integration)

## License

See LICENSE file for details.
