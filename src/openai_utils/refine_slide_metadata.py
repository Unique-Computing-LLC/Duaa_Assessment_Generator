from duaa_edtools.utils.s3 import fetch_file_from_s3, write_file_to_s3, s3_file_exists
from duaa_edtools.slide_layouts.layouts import SLIDE_LAYOUTS


from .slide_refinement_system_prompt import SYSTEM_PROMPT
from .llm import get_json_from_llm
from .llm_response_models import Slide
from src.openai_utils.prompts import SLIDE_REFINEMENT_PROMPT
import json

def refine_slide_metadata(
    event, config
) -> dict:
    """
    Sends teacher_guidelines and lesson_content to OpenAI and returns lecture slide content in JSON format.
    """

    s3_slide_metadata_file = config.EVENT_DIR + "/slide_metadata.json"
    slide_metadata_file_path = "/tmp/slide_metadata.json"
    fetch_file_from_s3(s3_slide_metadata_file, slide_metadata_file_path)

    with open(slide_metadata_file_path, "r", encoding="utf-8") as f:
        slide_deck_metadata = json.load(f)

    slide_metadata = slide_deck_metadata['slides'][int(config.SLIDE_NO)]
    system_prompt = SYSTEM_PROMPT.format(layout_templates=json.dumps(SLIDE_LAYOUTS))

    user_prompt = (
        f"{SLIDE_REFINEMENT_PROMPT.format(slide_metadata=slide_metadata, slide_refinement_prompt=config.END_USER_PROMPT)}\n\n"
    )

    slides_json = get_json_from_llm(
        schema=Slide,
        prompts=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
    )

    updated_slide_deck_metadata = slide_deck_metadata

    updated_slide_deck_metadata['slides'][int(config.SLIDE_NO)] = slides_json.model_dump()

    updated_metadata_path = "/tmp/updated_slide_metadata.json"
    with open(updated_metadata_path, "w", encoding="utf-8") as f:
        json.dump(updated_slide_deck_metadata, f, ensure_ascii=False, indent=2)

    print("REFINED SLIDE METADATA:", slides_json.model_dump_json(indent=2))

    write_file_to_s3(updated_metadata_path, s3_slide_metadata_file)
    print("file uploaded to S3.")
    return {
        "SLIDE_NO": config.SLIDE_NO,
        "USER_PROMPT": config.END_USER_PROMPT,
        "UPDATED_SLIDE_METADATA_FILE": s3_slide_metadata_file,
    }