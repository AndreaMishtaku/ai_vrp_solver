import pandas as pd

def save_file(file_path, content):
    try:
        with open(file_path, "w", encoding="utf-8", errors='replace') as file:
            file.write(content)
    except IOError as e:
        print(f"Error saving file: {e}")

def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors='replace') as file:
            content = file.read()
        return content
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def read_excel_file(file, columns):
    try:
        df = pd.read_excel(file)
        darray = df[columns].values
        return darray 
    except IOError as e:
        print(f"Error reading file: {e}")
        return None