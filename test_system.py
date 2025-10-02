#!/usr/bin/env python3
"""
Test the simplified question generation system
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.step_functions import execute_workflow

def test_system():
    """Test the complete system"""
    print("Testing DUAA Assessment Generator...")
    
    result = execute_workflow(
        course_id="MATH_101",
        course_name="Mathematics 101", 
        day_id="DAY_001",
        day_name="Day 1: Algebra",
        lesson_id="LESSON_001",
        lesson_name="Basic Algebra",
        topic="Algebra",
        num_questions=3
    )
    
    if result["success"]:
        print("✅ System test passed!")
        print(f"Generated: {result['questions_generated']} questions")
        print(f"Assigned: {result['questions_assigned']} questions")
        print(f"Bank ID: {result['hierarchy']['bank_id']}")
    else:
        print("❌ System test failed!")
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_system()
