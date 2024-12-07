

import os

def create_and_write_file(filename, content):
    """
    Create a new file with the specified content. If the file already exists,
    overwrite it to ensure the new content is written.
    Args:
        filename (str): Name of the file to create or overwrite.
        content (str): Content to write into the file.
    """
    try:
        # Check if the file exists and remove it to avoid appending
        if os.path.exists(filename):
            os.remove(filename)
        
        # Create and write content to the file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content written to {filename}")
    except Exception as e:
        print(f"An error occurred while creating/writing the file: {e}")



def typeOfFile(filepath: str):
    """Returns the type of the file based on its extension"""
    ex = ''
    filepath = filepath[::-1]  # Reverse the file path to access the file extension from the end
    for i in range(len(filepath)):
        if filepath[i] == '.':
            return ex[::-1]  # Return the file extension in its original order
        ex += filepath[i]
                   
def get_compiler(file_path: str):
    """Return the appropriate command to compile and run the file based on its extension."""
    
    # Split the file path to extract the file name and extension
    file_extension = file_path.split('.')[-1]

    # Define a mapping of file extensions to compilers
    compilers = {
        'py':'python',  # 'python3' for Unix-like, 'python' for Windows
        'js': 'node',
        'java': 'javac',
        'cpp': 'g++',  # for compiling C++
        'c': 'gcc',    # for compiling C
        'rb': 'ruby',
        'go': 'go run',
    }

    # Check if the file extension has a corresponding compiler
    if file_extension in compilers:
        return compilers[file_extension]
    else:
        raise ValueError(f"No compiler found for the file extension: .{file_extension}")
    
def extract_raw_code(code):
    """Extract the raw code by removing unwanted introductory text and triple backtick blocks."""
    if code.startswith("```") and code.endswith("```"):
        return code[3:-3].strip()  # Remove the first and last three characters (triple quotes)
    elif code.startswith("```"):
        return code[3:].strip()
    if code.endswith("```"):
        return code[:-3].strip()
    return code.strip()  # Return the original code if no triple quotes are found

def writeInFile(solution, file):
    """Overwrites the given file with the corrected solution."""
    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(solution)
            print(f"{file} has been rewritten with corrected code.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        

def get_test_code(filename):
    """Reads the full code of the given file and returns it."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
