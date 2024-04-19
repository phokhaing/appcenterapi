#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : BOTIN POV                                      |
#  | EMAIL: botin.pov@gmail.com                            |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 30.5.2023.                                   |
#  +-------------------------------------------------------+
import json

# --------------------------------------------------------------------------------------
#   param 1st  FormData is the data that has format from client side as a formData format.
#   param 2nd  dataType have 2 type form to  ['formData', 'json']. Ex: f->j  , j->jk.
#   param 3rd  keyGetvalue  is key in json to ge value in json. j->jk.
# --------------------------------------------------------------------------------------


def convertToObject(formData, dataType, keyGetvalue=''):
    aspect_only = ['f->j', 'f->jk']
    if dataType not in aspect_only:
        return False

    data = {}
    for key, value in formData.items():
        if "[" in key and "]" in key:
            array_key = key[:key.index("[")]
            array_index = int(key[key.index("[") + 1:key.index("]")])

            if array_key not in data:
                data[array_key] = []

            while len(data[array_key]) <= array_index:
                data[array_key].append({})

            nested_key = key[key.index("].") + 2:]
            data[array_key][array_index][nested_key] = value if value != 'null' else None
        else:
            data[key] = value if value != 'null' else None

    # Dynamic conversion of flat fields to nested dictionaries
    converted_data = {}
    for key, value in data.items():
        keys = key.split('.')
        current_dict = converted_data
        for idx, k in enumerate(keys):
            if idx == len(keys) - 1:
                current_dict[k] = value
            else:
                if k not in current_dict:
                    current_dict[k] = {}
                current_dict = current_dict[k]

    if dataType == 'f->jk':
        # Convert data to JSON string and parse it
        try:
            converted_data = json.loads(formData.get(keyGetvalue, {}))
        except json.JSONDecodeError:
            return False
    # Return the converted data
    return converted_data
