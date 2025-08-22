import os

from makao_game import dictionaries as c_dict

def get_data_path() -> str:
    # os.path.dirname takes out file name from given path
    # os.path.abspath() ensures that path is always absolute as simple __file__ can sometimes return relative path
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, os.pardir))
    return os.path.join(project_root_dir, c_dict.DATA_DIR_NAME)

def colour_string(text: str, colour: str, bg_colour: str = '') -> str:
    """Returns string of text of specified colour in ASCII format."""

    if not text or not colour:
        raise ValueError('text cannot be empty')

    try:
        colored_text: str = f'{c_dict.ASCII_START}{c_dict.ASCII_COLOURS[colour]}'

        if bg_colour:
            colored_text += f';{c_dict.ASCII_COLOURS[bg_colour]}m'
        else:
            colored_text += 'm'
    except KeyError:
        raise KeyError(f'colour {colour} or {bg_colour} cannot be found')

    return colored_text + f'{text}{c_dict.ASCII_END}'
