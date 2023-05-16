"""-----------------------------------
Data manager for storage as json file
-----------------------------------"""

import os
import json
from pathlib import Path


# Default file path to store data
DIR_PATH  = Path(__file__).parent / "store"
FILE_PATH = DIR_PATH / "data.json"


def set_data(data={}):
    """ Save data in json file.
    """
    # Create directory if not exists
    if not os.path.isdir(DIR_PATH):
        os.makedirs(DIR_PATH)
    # Inserts data and creates a new json file with it
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'x') as file:
            data = json.dumps(data, indent=4)
            file.write(data)
            file.close()
    else:
    # Updates data with prior removal of existing json file
        with open(FILE_PATH, 'r+') as file:
            _data = json.load(file)
            _data.update(data)
            file.close()
            os.remove(FILE_PATH)
        with open(FILE_PATH, 'x') as file:
            json.dump(_data, file, indent=4)
            file.close()
    return True


def get_data(key=None, default=None):
    """ Get a value by key from the json file.
    """
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, 'r+') as file:
        content = file.read()
        if len(content) <= 2:
            return {}
        data = json.loads(content)
        if key == None:
            return data
        data = json.loads(content)
        return data.get(key, default)

