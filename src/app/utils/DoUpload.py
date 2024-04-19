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


import datetime
import os

def doUploadFiles(files, defaultPath=""):
    if not files:
        return []  # No files provided, return an empty array

    staticPath = 'static/file_storage/'
    current_datetime = datetime.datetime.now()

    if not defaultPath:
        defaultPath = os.path.join(staticPath, 'default_store')
        folder_name = current_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f")
    else:
        defaultPath = os.path.join(staticPath, defaultPath)
        folder_name = ''

    folder_path = os.path.join(defaultPath, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    folderPathStore = folder_path.replace(staticPath, '', 1)
    if folderPathStore.endswith('/'):
        folderPathStore = folderPathStore[:-1]

    uploaded_files = []

    try:
        for file in files:
            # Append timestamp to the file name
            filename = f"{current_datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')}_{file.name}"
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            uploaded_file = {
                'upload_file_name': filename,
                'original_name': file.name,
                'file_type': file.content_type,
                'extension': os.path.splitext(file.name)[1],
                'file_size': file.size,
                'timestamp': int(current_datetime.timestamp()),
                'file_path': folderPathStore,
            }

            uploaded_files.append(uploaded_file)

    except Exception as e:
        for file in files:
            file_path = os.path.join(folder_path, file.name)
            if os.path.exists(file_path):
                os.remove(file_path)

        raise e

    return uploaded_files

def removeUploadedByName(file_path='', file_name=''):
    staticPath = 'static/file_storage/'
    folder_path = os.path.join(staticPath, file_path)
    file_path = os.path.join(folder_path, file_name)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            # raise("File does not exist:", file_path)
            return False
    except Exception as e:
        # print("An error occurred while removing the file:", str(e))
        return False
