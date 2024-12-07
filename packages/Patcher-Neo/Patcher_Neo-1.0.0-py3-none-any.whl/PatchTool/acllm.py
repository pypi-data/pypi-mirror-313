import shlex
from subprocess import Popen, PIPE
from llm import autoCorrect_query, make_query
from func import create_and_write_file,typeOfFile
import os


def execute_and_return(cmd):
    """
    Execute the external command and get its exit code, stdout, and stderr.
    Args:
        cmd (str): The command to execute.
    Returns:
        tuple: A tuple containing (exitcode, stdout, stderr).
    """
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode  # Capture the exit code
    return exitcode, out.decode('utf-8'), err.decode('utf-8')  # Decode the output for better readability

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

def full_file(filepath: str):  # Use lowercase "filepath" to match Typer's default behavior
    """Main function to process the file."""
    # Read the code from the specified file
    code = get_test_code(filepath)
    if not code:
        print("No test code found.")
        exit(1)

    # Execute the code and capture stdout and stderr
    exit_code, out, err = execute_and_return(f"python {filepath}")
    print(f"Execution Output:\n{out}\n")
    print(f"Execution Errors:\n{err}\n")
    print(f"Exit Code: {exit_code}")

    if exit_code != 0:  # Handle errors if the exit code is non-zero
        print("Error detected. Processing...")
        query = f"Code:\n{code}\nError:\n{err}"
        corrected_code = autoCorrect_query(query=query)
        
        # Extract and print the corrected code
        trimmed_corrected_code = extract_raw_code(corrected_code)
        print("Corrected Code:\n", trimmed_corrected_code)
        
        # Save the corrected code back to the file
        writeInFile(trimmed_corrected_code, filepath)

    elif out.strip():  # Handle non-error output
        query_manual = "if there is any error shown in the output then return true otherwise false, just give me true or false no extra text"
        if_err_query = f"{out}\n{query_manual}"
        if_err = make_query(if_err_query)

        if if_err == "true":
            print("Detected potential error in output. Resolving it...")
            query = f"Code:\n{code}\nOutput:\n{out}"
            corrected_code = autoCorrect_query(query=query)
            
            # Extract and print the corrected code
            trimmed_corrected_code = extract_raw_code(corrected_code)
            print("Corrected Code:\n", trimmed_corrected_code)
            
            # Save the corrected code back to the file
            writeInFile(trimmed_corrected_code, filepath)
    else:
        print("No errors or issues detected in the script.")


def modif(filepath:str):
    code = get_test_code(filepath)
    
    if not code:
        print("No code found ! You can use query function to generate code --")
    
    modification = input("Things to modify in the code :")
    query_manaul = "modify the code according to the specific modifications and remember not to give any extraneous line or text other then the modified code this is very important remmeber this"
    result = make_query(code + modification + query_manaul)
    result = extract_raw_code(result)
    
    bool = input("Wanna write the changes [Yes/No]: ")
    fileType = typeOfFile(filepath)
    if bool == "Yes":
        writeInFile(result,filepath)
    elif bool== "No":
        create_and_write_file(f"output.{fileType}",result)
    else:
        while not bool:
            bool = input("Wanna write the changes [Yes/No]: ") 

def AddComments(filepath:str):
    code = get_test_code(filepath)
    
    if not code:
        print("No code found ! You can use query function to generate code --")
    
    query_manaul = "add commets to code where its not added and do not modify anything else other then that , make sure not to add extraneous code or any extraneous lines or any extraneous description from your side just provide me the code with comments added, make sure no extra text any kind of text just give me the code , dont add this line *Here is the code with added comments:*"
    result = make_query(code + query_manaul)
    result = extract_raw_code(result)
    
    bool = input("Wanna write the changes [Yes/No]: ")
    fileType = typeOfFile(filepath)
    if bool == "Yes":
        writeInFile(result,filepath)
    elif bool== "No":
        create_and_write_file(f"output.{fileType}",result)
    
        
def Query(filetype:str):
    query = input("Query: ")
    query_manual = "dont add any other test then the code please , make sure not to give any extraneous line other then the things query asks for, it means nothing extra rather then the desired answer,not extra comments should be added by your side just the code ntg else rember it its very important not to add any extra text"
    result = make_query(query + query_manual)
    result = extract_raw_code(result)
    # Generate a unique filename using the current timestamp and the given file type
    if not filetype.startswith('.'):
        filetype = '.' + filetype  # Ensure that fileType starts with a dot
    filename = f"output{filetype}"
    # Delete the file if it already exists (to ensure a new file is created)
    if os.path.exists(filename):
        os.remove(filename)
    # Write the result to the new file
    with open(filename, 'w') as file:
        file.write(result)
    print(f"Result written to {filename}")
