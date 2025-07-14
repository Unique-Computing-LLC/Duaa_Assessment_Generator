from duaa_edtools.slide_layouts.layouts import SLIDE_LAYOUTS
from openai import OpenAI
from .system_prompt import SYSTEM_PROMPT
from src.openai_utils.prompts import LECTURE_SLIDES_PROMPT
import json

def generate_lecture_slides_metadata(
    teacher_guidelines: str,
    lesson_content: str,
    class_name: str,
    lesson_name: str,
) -> dict:
    """
    Sends teacher_guidelines and lesson_content to OpenAI and returns lecture slide content in JSON format.
    """
    # Define a JSON schema for the model to follow
    json_schema = (
        "The output must strictly follow this JSON schema:\n"
        "{\n"
        '  "class_name": "<class name here>",\n'
        '  "lesson_name": "<lesson name here>",\n'
        '  "slides": [\n'
        "    {\"title\": \"...\", \"image_prompt\":[Prompt to create suitable image/images for the slide], \"text\": [minimal text required in the slides as per the class and age group] \"},\n"
        "    ...\n"
        "  ]\n"
        "}\n"
        "Do not include any text or explanation outside the JSON object."
    )

    system_prompt = SYSTEM_PROMPT.format(class_name=class_name, lesson_name=lesson_name, layout_templates=json.dumps(SLIDE_LAYOUTS))
    user_prompt = (
        f"{LECTURE_SLIDES_PROMPT.format(teacher_guidelines=teacher_guidelines)}\n\n"
    )

    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        # max_tokens=1500,
        # response_format = "json"
    )

    response.output_text

    try:
        slides_json = json.loads(response.output_text)
    except Exception:
        # If the model returns markdown or code block, try to extract JSON
        import re
        match = re.search(r'```json(.*?)```', response.output_text, re.DOTALL)
        if match:
            slides_json = json.loads(match.group(1).strip())
        else:
            slides_json = {}
    return slides_json