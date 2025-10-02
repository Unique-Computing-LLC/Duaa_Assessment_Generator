"""
Question Generation Module for DUAA Lesson Content Generator

This module generates multiple choice questions using OpenAI API and stores them
in the PostgreSQL database.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from openai import OpenAI
from sqlalchemy import create_engine, text, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logger = logging.getLogger(__name__)

# Database setup
Base = declarative_base()

class Question(Base):
    """SQLAlchemy model for questions table"""
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class QuestionGenerator:
    """Handles question generation and database operations"""
    
    def __init__(self, database_url: str, openai_api_key: str):
        """
        Initialize the question generator
        
        Args:
            database_url: PostgreSQL connection string
            openai_api_key: OpenAI API key
        """
        self.database_url = database_url
        self.openai_api_key = openai_api_key
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=openai_api_key)
        
        # Initialize database connection
        self.engine = None
        self.SessionLocal = None
        self._setup_database()
    
    def _setup_database(self) -> None:
        """Setup database connection and create tables if they don't exist"""
        try:
            self.engine = create_engine(self.database_url, future=True)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, future=True)
            
            # Create tables if they don't exist
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database connection established successfully")
            
        except SQLAlchemyError as e:
            logger.error(f"Database connection failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during database setup: {e}")
            raise
    
    def create_questions_table(self) -> None:
        """Create the questions table after the subjects table"""
        try:
            with self.engine.connect() as conn:
                # Check if questions table already exists
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'questions'
                    );
                """))
                
                table_exists = result.scalar()
                
                if not table_exists:
                    # Create the questions table
                    conn.execute(text("""
                        CREATE TABLE questions (
                            id SERIAL PRIMARY KEY,
                            question_json JSONB NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """))
                    conn.commit()
                    logger.info("Questions table created successfully")
                else:
                    logger.info("Questions table already exists")
                    
        except SQLAlchemyError as e:
            logger.error(f"Failed to create questions table: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating questions table: {e}")
            raise
    
    def generate_question_with_openai(self, topic: str) -> Dict[str, Any]:
        """
        Generate a multiple choice question using OpenAI API
        
        Args:
            topic: The topic for which to generate a question
            
        Returns:
            Dictionary containing question, options, and correct answer
        """
        try:
            prompt = f"""
            Generate a multiple choice question about the topic: "{topic}"
            
            The question should be:
            - Educational and relevant to the topic
            - Clear and concise
            - Have 4 options (A, B, C, D)
            - Have one correct answer
            - Be appropriate for students
            
            Return the response in the following JSON format:
            {{
                "question": "Your question here?",
                "options": {{
                    "A": "Option A text",
                    "B": "Option B text", 
                    "C": "Option C text",
                    "D": "Option D text"
                }},
                "correct_answer": "A"
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an educational content generator that creates high-quality multiple choice questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract and parse the JSON response
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            else:
                json_str = content
            
            question_data = json.loads(json_str)
            
            # Validate the response structure
            required_fields = ["question", "options", "correct_answer"]
            for field in required_fields:
                if field not in question_data:
                    raise ValueError(f"Missing required field: {field}")
            
            if not isinstance(question_data["options"], dict) or len(question_data["options"]) != 4:
                raise ValueError("Options must be a dictionary with exactly 4 items")
            
            if question_data["correct_answer"] not in question_data["options"]:
                raise ValueError("Correct answer must be one of the option keys")
            
            logger.info(f"Successfully generated question for topic: {topic}")
            return question_data
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating question: {e}")
            raise
    
    def save_question_to_db(self, question_data: Dict[str, Any]) -> int:
        """
        Save the generated question to the database
        
        Args:
            question_data: The question data to save
            
        Returns:
            The ID of the inserted question
        """
        try:
            session = self.SessionLocal()
            question = Question(question_json=question_data)
            session.add(question)
            session.commit()
            question_id = question.id
            session.close()
            
            logger.info(f"Question saved to database with ID: {question_id}")
            return question_id
            
        except SQLAlchemyError as e:
            logger.error(f"Database error saving question: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error saving question: {e}")
            raise
    
    def generate_and_save_question(self, topic: str) -> int:
        """
        Generate a question and save it to the database
        
        Args:
            topic: The topic for which to generate a question
            
        Returns:
            The ID of the inserted question
        """
        try:
            # Ensure questions table exists
            self.create_questions_table()
            
            # Generate question using OpenAI
            question_data = self.generate_question_with_openai(topic)
            
            # Save to database
            question_id = self.save_question_to_db(question_data)
            
            logger.info(f"Successfully generated and saved question for topic '{topic}' with ID: {question_id}")
            return question_id
            
        except Exception as e:
            logger.error(f"Failed to generate and save question for topic '{topic}': {e}")
            raise
    
    def close_connection(self) -> None:
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


def generate_questions_for_topic(topic: str, database_url: str, openai_api_key: str) -> int:
    """
    Convenience function to generate questions for a given topic
    
    Args:
        topic: The topic for which to generate questions
        database_url: PostgreSQL connection string
        openai_api_key: OpenAI API key
        
    Returns:
        The ID of the generated question
    """
    generator = None
    try:
        generator = QuestionGenerator(database_url, openai_api_key)
        question_id = generator.generate_and_save_question(topic)
        return question_id
    finally:
        if generator:
            generator.close_connection()


if __name__ == "__main__":
    # Example usage - Replace with your actual credentials
    DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/database_name"
    OPENAI_API_KEY = "your-openai-api-key-here"
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        question_id = generate_questions_for_topic("Mathematics", DATABASE_URL, OPENAI_API_KEY)
        print(f"Generated question with ID: {question_id}")
    except Exception as e:
        print(f"Error: {e}")
