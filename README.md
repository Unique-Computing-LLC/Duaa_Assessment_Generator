# DUAA Assessment Generator

A comprehensive assessment generation system that creates educational content and automatically generates multiple choice questions using OpenAI's GPT models with a hierarchical problem management system.

## Features

- **Slide Generation**: Creates educational slides from lesson content
- **AI Question Generation**: Automatically generates multiple choice questions using OpenAI GPT-3.5-turbo
- **Problem Hierarchy Management**: 
  - Problem Libraries (Course Level)
  - Problem Collections (Day Level) 
  - Problem Banks (Lesson Level)
- **Database Integration**: PostgreSQL with proper relationships and JSONB storage
- **Local Step Functions**: Orchestrated workflow for question generation and assignment
- **AWS Integration**: Supports S3 storage and AWS Secrets Manager

## Problem Management System

The system organizes questions in a hierarchical structure:

```
Problem Library (Course Level)
└── Problem Collection (Day Level)
    └── Problem Bank (Lesson Level)
        └── Questions (with unique IDs)
```

### Database Schema

```sql
-- Problem Libraries (Course Level)
CREATE TABLE problem_libraries (
    id SERIAL PRIMARY KEY,
    library_id VARCHAR(36) UNIQUE NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    course_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Problem Collections (Day Level)
CREATE TABLE problem_collections (
    id SERIAL PRIMARY KEY,
    collection_id VARCHAR(36) UNIQUE NOT NULL,
    library_id VARCHAR(36) REFERENCES problem_libraries(library_id),
    day_id VARCHAR(50) NOT NULL,
    day_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Problem Banks (Lesson Level)
CREATE TABLE problem_banks (
    id SERIAL PRIMARY KEY,
    bank_id VARCHAR(36) UNIQUE NOT NULL,
    collection_id VARCHAR(36) REFERENCES problem_collections(collection_id),
    lesson_id VARCHAR(50) NOT NULL,
    lesson_name VARCHAR(200) NOT NULL,
    topic VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions with Problem Bank Assignment
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_id VARCHAR(36) UNIQUE,
    question_json JSONB NOT NULL,
    problem_bank_id VARCHAR(36) REFERENCES problem_banks(bank_id),
    topic VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Question Format

Generated questions follow this JSON structure:

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

1. **Setup Environment Variables**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export DATABASE_URL="postgresql+psycopg2://username:password@localhost:5432/database_name"
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Database**:
   ```bash
   docker run --name duaa_db -e POSTGRES_DB=duaa_db -e POSTGRES_USER=duaa -e POSTGRES_PASSWORD=your_password -p 5432:5432 -d postgres:latest
   ```

4. **Run the System**:
   ```bash
   # Test the system
   python test_system.py
   
   # Run main pipeline
   python -m src.main
   ```

## Usage

### Basic Question Generation

```python
from src.step_functions import execute_workflow

result = execute_workflow(
    course_id="MATH_101",
    course_name="Mathematics 101",
    day_id="DAY_001", 
    day_name="Day 1: Algebra",
    lesson_id="LESSON_001",
    lesson_name="Basic Algebra",
    topic="Algebra",
    num_questions=5
)
```

### Pipeline Integration

The question generation is automatically integrated into the main lesson generation pipeline and will:

1. Create problem hierarchy (Library → Collection → Bank)
2. Generate questions using OpenAI
3. Assign questions to the appropriate problem bank
4. Store everything in PostgreSQL

## Dependencies

- Python 3.7+
- PostgreSQL
- OpenAI API
- SQLAlchemy
- psycopg2-binary

## License

See LICENSE file for details.
