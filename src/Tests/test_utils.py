import os
import pandas as pd
import tempfile
from src.utils.utils import read_csv_as_dict

def test_read_csv_as_dict(tmp_path):
    # Prepare a sample CSV file
    csv_content = "col1,col2\nval1,val2\nval3,val4\n"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # Call the function
    result = read_csv_as_dict(str(csv_file))

    # Check the result
    assert isinstance(result, list)
    assert result == [
        {"col1": "val1", "col2": "val2"},
        {"col1": "val3", "col2": "val4"}
    ]
