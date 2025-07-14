from unittest.mock import patch, MagicMock
import json
import pytest

from src.openai_utils import slide_generator

@patch("src.openai_utils.slide_generator.OpenAI")
def test_generate_lecture_slides_metadata_parses_json(mock_OpenAI):
    # Mock OpenAI response with direct JSON
    slides_dict = {
        "class_name": "ClassA",
        "lesson_name": "Lesson1",
        "slides": [
            {"title": "Slide 1", "image_prompt": ["Prompt"], "text": ["Some text"]}
        ]
    }
    mock_response = MagicMock()
    mock_response.output_text = json.dumps(slides_dict)
    mock_OpenAI.return_value.responses.create.return_value = mock_response

    result = slide_generator.generate_lecture_slides_metadata("tg", "lc", "ClassA", "Lesson1")
    assert result == slides_dict

@patch("src.openai_utils.slide_generator.OpenAI")
def test_generate_lecture_slides_metadata_parses_json_from_codeblock(mock_OpenAI):
    # Mock OpenAI response with JSON in a code block
    slides_dict = {
        "class_name": "ClassA",
        "lesson_name": "Lesson1",
        "slides": [
            {"title": "Slide 1", "image_prompt": ["Prompt"], "text": ["Some text"]}
        ]
    }
    codeblock = "```json\n" + json.dumps(slides_dict) + "\n```"
    mock_response = MagicMock()
    mock_response.output_text = codeblock
    mock_OpenAI.return_value.responses.create.return_value = mock_response

    result = slide_generator.generate_lecture_slides_metadata("tg", "lc", "ClassA", "Lesson1")
    assert result == slides_dict

@patch("src.openai_utils.slide_generator.OpenAI")
def test_generate_lecture_slides_metadata_returns_empty_on_invalid_json(mock_OpenAI):
    # Mock OpenAI response with invalid JSON
    mock_response = MagicMock()
    mock_response.output_text = "not a json"
    mock_OpenAI.return_value.responses.create.return_value = mock_response

    result = slide_generator.generate_lecture_slides_metadata("tg", "lc", "ClassA", "Lesson1")
    assert result == {}
