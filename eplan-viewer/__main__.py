# -*- coding: utf-8 -*-
"""Module for daily verification

Example:
    none   

Attributes:
    none
"""

from pprint import pprint
from os import listdir, path, walk, environ
import hashlib, pandas
BLOCKSIZE = 65536
COMPANY_CODE = 'LTS'

schema = {
    'fields': [
        'file_base',
        'file_walkpath_relative',
        'file_path_relative',
        'sha2_hex',
        'recommended_name',
        'recommended_timestamp',
        ],
    'primary_key': [
        'file_path_relative',
        'sha2_hex',
        ],
    }

dir_data_user = path.join('C:\\' , 'Users', 'Public', 'EPLAN')
dir_data_template = path.join('C:\\', 'ProgramData', 'EPLAN')

def read(base_path, file_walkpath_relative):
    files_info = []
    file_total_walk_path = path.join(base_path, file_walkpath_relative)
    for directory, subdirs, files in walk(file_total_walk_path):
        for file_name in files:
            # Calculate hash of file
            hasher = hashlib.sha256()
            with open(path.join(directory, file_name), 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            # Join file info
            file_total_path = path.join(directory,file_name)
            files_info.append({
                'base_path': base_path,
                'file_walkpath_relative': file_walkpath_relative,
                'file_path_relative': path.relpath(file_total_path, file_total_walk_path),
                'sha2_hex': hasher.hexdigest(),
                })
    return(files_info)

def read_o_data(file_base=dir_data_template):
    files_info = []
    for file0 in listdir(file_base):
        element0=path.join(file_base, file0)
        if path.isdir(element0):
            for file1 in listdir(element0):
                element1=path.join(element0, file1)
                if path.isdir(element1):
                    for file2 in listdir(element1):
                        element2=path.join(element1, file2)
                        if path.isdir(element2):
                            walkpath_relative = path.relpath(element2, file_base)
                            files_info += read(file_base, walkpath_relative)
    return files_info

def read_user_data():
    return read(dir_data_user, 'Data')

if __name__ == '__main__':
    # Enumerating file sources
    #df = pandas.DataFrame()
    df = pandas.DataFrame()
    df = df.append(read_o_data())
    #df = df.append(read_user_data())
    with open('o_data.json', 'w') as afile:
        afile.write(df.to_json(orient='records'))
