import json
import os

def get_run_type():
    inp = json.loads(os.environ['PIPELINE_INPUT'])
    return inp['RUN_TYPE']