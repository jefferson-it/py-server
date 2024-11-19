import json
import os

__dirname = os.path.dirname(os.path.abspath(__name__))

def overwrite_file(filepath: str, content: str):
    try:
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(content)
            file.close()

        return read_file(filepath)
    except: 
        print(f"OOPS! Error on write file {filepath}")


def write_file(filepath: str, content: str):
    try:
        exist = read_file(filepath)

        if exist: return exist

        with open(filepath, mode="a", encoding="utf-8") as file:
            file.write(content)
            file.close()

        return read_file(filepath)
    except: 
        print(f"OOPS! Error on write file {filepath}")

def read_file(filepath: str):
    try:
        file = open(filepath, mode="r", encoding="utf-8")
        return file.read()
    except: 
        print(f"OOPS! Error on open file {filepath}")


def read_json(filepath: str):
    file = read_file(filepath)
    
    if file: 
        return json.loads(file)
    else:
        return { }