import pytest
from unittest.mock import patch, MagicMock
import sys

# Patch sys.modules to allow import of main.py as a module
with patch.dict('sys.modules', {
    'duaa_edtools': MagicMock(),
    'duaa_edtools.config': MagicMock(),
    'duaa_edtools.event_utils': MagicMock(),
    'duaa_edtools.utils': MagicMock(),
    'duaa_edtools.utils.ex_handler': MagicMock(),
    'duaa_edtools.utils.logger': MagicMock(),
    'duaa_edtools.utils.s3': MagicMock(),
    'duaa_edtools.utils.aws_secret_manager': MagicMock(),
    'duaa_edtools.utils.send_task_success': MagicMock(),
    'src.openai_utils.slide_generator': MagicMock(),
}):
    import src.main as main_module

@pytest.fixture
def mock_dependencies(monkeypatch):
    # Mock config
    mock_config = MagicMock()
    mock_config.EVENT_DIR = "event_dir"
    mock_config.LESSON_DIR = "lesson_dir"
    mock_config.CLASS = "class"
    mock_config.TIMESTAMP = "timestamp"
    mock_config.LESSON_NUMBER = 1
    mock_config.SUBJECT_NAME = "subject"
    mock_config.LANGUAGE = "en"

    # Mock event
    mock_event = {}

    # Patch all external dependencies
    monkeypatch.setattr(main_module.duaa_config, "load_config", lambda event_name: mock_config)
    monkeypatch.setattr(main_module, "load_event", lambda event_name, config: mock_event)
    monkeypatch.setattr(main_module, "save_event", lambda config, event: None)
    monkeypatch.setattr(main_module, "send_task_success", lambda data: None)
    monkeypatch.setattr(main_module, "fetch_file_from_s3", lambda s3_path, local_path: local_path)
    monkeypatch.setattr(main_module, "s3_file_exists", lambda s3_path: False)
    monkeypatch.setattr(main_module, "write_file_to_s3", lambda local_path, s3_path: None)
    monkeypatch.setattr(main_module, "generate_lecture_slides_metadata", lambda tg, x, cls, topic: {"slides": []})

    # Patch pandas read_csv
    monkeypatch.setattr(main_module.pd, "read_csv", lambda path: MagicMock(to_dict=lambda orient: [{"topic": "topic"}]))

    # Patch Path.read_text
    monkeypatch.setattr(main_module.Path, "read_text", lambda self, encoding=None: "tg text")

    return mock_config, mock_event

# def test_main_creates_slide_metadata_when_not_exists(tmp_path, mock_dependencies, monkeypatch):
#     mock_config, mock_event = mock_dependencies
#     slides_json_path = tmp_path / "slide_metadata.json"

#     # Patch open to write to tmp_path
#     monkeypatch.setattr(main_module, "open", open, raising=False)
#     monkeypatch.setattr(main_module, "json", main_module.json)

#     # Run main
#     main_module.main()

#     # Check that slides_metadata_file is set in event
#     assert "slides_metadata_file" in mock_event
#     assert mock_event["slides_metadata_file"] == f"{mock_config.EVENT_DIR}/slide_metadata.json"

# def test_main_skips_generation_if_metadata_exists(mock_dependencies, monkeypatch):
#     mock_config, mock_event = mock_dependencies

#     # Patch s3_file_exists to return True
#     monkeypatch.setattr(main_module, "s3_file_exists", lambda s3_path: True)

#     # Run main
#     main_module.main()

#     # Should still set slides_metadata_file in event
#     assert "slides_metadata_file" in mock_event
