#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : BOTIN POV                                      |
#  | EMAIL: botin.pov@gmail.com                            |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 01.7.2023.                                   |
#  +-------------------------------------------------------+

def array_to_string(arr):
    if not arr:  # Handle empty list or None
        return ''

    # Extracting the 'id' values from the dictionaries in the list
    ids = [str(d.get('id', '')) for d in arr]

    # Joining the 'id' values into a comma-separated string
    string_representation = ','.join(ids)

    return string_representation


def string_to_array(string_representation):
    if not string_representation:  # Handle empty string or None
        return []

    # Splitting the string into a list of 'id' values
    id_list = string_representation.split(',')

    # Creating a list of dictionaries with 'id' properties
    arr = [{'id': int(id)} for id in id_list if id.isdigit()]  # Handle non-numeric id values

    return arr


# Example usage:
#
# from app.utils.ArrayStringConverterByID import  string_to_array, array_to_string
#
# co_borrower = [{'id': 15}, {'id': 13}]
#
# string_representation = array_to_string(co_borrower)
# print(string_representation)  # Output: "15,13"
#
# co_borrower = string_to_array(string_representation)
# print(co_borrower)  # Output: [{'id': 15}, {'id': 13}]
