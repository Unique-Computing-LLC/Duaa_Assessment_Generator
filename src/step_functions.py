"""
Simplified Step Functions
"""
import os
import uuid
from .generate_questions import generate_questions_for_topic
from .problem_management import ProblemManager

def execute_workflow(course_id, course_name, day_id, day_name, lesson_id, lesson_name, topic, num_questions=5):
    """Execute complete question generation workflow"""
    database_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://username:password@localhost:5432/database_name")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        return {"success": False, "error": "OpenAI API key not found"}
    
    try:
        # Step 1: Create problem hierarchy
        pm = ProblemManager(database_url)
        hierarchy = pm.create_hierarchy(course_id, course_name, day_id, day_name, lesson_id, lesson_name, topic)
        bank_id = hierarchy["bank_id"]
        
        # Step 2: Generate questions
        question_ids = []
        for i in range(num_questions):
            try:
                question_id = generate_questions_for_topic(topic, database_url, openai_api_key)
                question_ids.append(question_id)
            except Exception as e:
                print(f"Failed to generate question {i+1}: {e}")
        
        # Step 3: Assign questions to bank
        assigned = 0
        for question_id in question_ids:
            if pm.assign_question(question_id, bank_id):
                assigned += 1
        
        return {
            "success": True,
            "hierarchy": hierarchy,
            "questions_generated": len(question_ids),
            "questions_assigned": assigned
        }
    except Exception as e:
        return {"success": False, "error": str(e)}