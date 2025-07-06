from classes import dictionaries as c_dict
import os

def get_data_path() -> str:
    # os.path.dirname takes out file name from given path
    # os.path.abspath() ensures that path is always absolute as simple __file__ can sometimes return relative path
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, os.pardir))
    return os.path.join(project_root_dir, c_dict.DATA_DIR_NAME)