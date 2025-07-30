from duaa_edtools import config as duaa_config
from duaa_edtools.event_utils import load_event, save_event
from duaa_edtools.utils.ex_handler import exhandler
from duaa_edtools.utils.logger import logger
from duaa_edtools.utils.s3 import fetch_file_from_s3, write_file_to_s3, s3_file_exists
from duaa_edtools.utils.aws_secret_manager import get_aws_secrets
from duaa_edtools.utils import send_task_success

from .openai_utils.slide_generator import generate_lecture_slides_metadata

from pathlib import Path
from typing import Any, Dict
import pandas as pd
import json
import logging
import os


@exhandler
def main() -> None:
    event_name: str = "generate_lesson_content"
    logger.info(f"Starting slide metadata generation for event: {event_name}")
    config: Any = duaa_config.load_config(event_name)
    logger.debug(f"Loaded config: {config}")
    event: Dict[str, Any] = load_event(event_name, config)
    logger.debug(f"Loaded event: {event}")

    logger.info("Fetching extracted tg file from S3.")
    extracted_tg_file = fetch_file_from_s3(f"{config.LESSON_DIR}/resources/tg_extracted.md", "/tmp/tg_extracted.md")
    logger.info("Fetching lesson plan file from S3.")
    lesson_plan_file = fetch_file_from_s3(f"{config.LESSON_DIR}/lesson_plan.csv", "/tmp/lesson_plan.csv")
    
    logger.info("Reading lesson plan CSV.")
    lesson_plan_df = pd.read_csv(lesson_plan_file)
    lesson_plan = lesson_plan_df.to_dict(orient="records")[0]
    logger.debug(f"Lesson plan: {lesson_plan}")

    logger.info("Reading extracted tg file.")
    tg_text = Path(extracted_tg_file).read_text(encoding="utf-8")
    logger.info("Generating lecture slides metadata.")

    s3_slide_json_filepath = f"{config.EVENT_DIR}/slide_metadata.json"
    slides_json_path = "/tmp/slide_metadata.json"
    event['slides_metadata_file'] = s3_slide_json_filepath

    if 'slides_metadata_file' in event and s3_file_exists(event['slides_metadata_file']):
        logger.info(f"Slides metadata file already exists on S3: {event['slides_metadata_file']}. Exiting...")
    else:
        slides_json = generate_lecture_slides_metadata(tg_text, '', config.CLASS, lesson_plan['topic'])
        logger.info("Generated slides metadata.")
        logger.info(f"Saving slides metadata to {slides_json_path}.")
        with open(slides_json_path, "w", encoding="utf-8") as f:
            json.dump(slides_json, f, ensure_ascii=False, indent=2)
        logger.debug(f"Uploading slides metadata to S3: {s3_slide_json_filepath}")
        write_file_to_s3(slides_json_path, s3_slide_json_filepath)
        logger.info(f"Uploaded the slide metadata to S3 at {s3_slide_json_filepath}")

    save_event(config, event)
    send_task_success({
        "TIMESTAMP": config.TIMESTAMP,
        "CLASS": config.CLASS,
        "LESSON_NUMBER": config.LESSON_NUMBER,
        "SUBJECT_NAME": config.SUBJECT_NAME,
        "LANGUAGE": config.LANGUAGE,
    })

if __name__ == "__main__":

    logger.setLevel(logging.INFO)
    secrets = get_aws_secrets('duaa-openai-key')
    print("LOADED OPENAI_API_KEY", secrets.keys())

    for key, value in secrets.items():
        os.environ[key] = value

    main()