

import os


def create_and_write_file(filename: str, content: str):
    """Creates a new file and writes the given content to it. If the file exists, it is overwritten."""
    # Check if the file already exists, if so, delete it before creating a new one
    if os.path.exists(filename):
        os.remove(filename)
    
    # Open the file in write mode and write the content to it
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Result written to {filename}")


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