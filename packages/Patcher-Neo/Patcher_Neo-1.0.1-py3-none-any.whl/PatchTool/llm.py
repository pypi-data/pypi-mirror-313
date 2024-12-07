import os
from groq import Groq

def get_key(filename):
    """Reads the first line of a text file and returns it."""
    try:
        with open(filename, 'r') as file:
            first_line = file.readline().strip()  # Read and strip whitespace
            return first_line
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Load the API key from the file
#GROQ_API_KEY = get_key("key.txt")

# Initialize the Groq client with the API key
client = Groq(api_key="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")

def autoCorrect_query(query):
    # Updated query to ensure that the order of the code remains the same as the original
    query_manual = """Please correct the code by removing all errors and ensuring that it functions as intended.
Do not add any comments to the reply at all from your side. Do not include the phrase "Here is the corrected code:" at the beginning.
Do not wrap the code in triple single quotes (''' ''') or any other quote marks.
Do not remove any necessary parts of the code. Ensure that the code performs its intended functionality.
Provide the **full corrected code** as output **without** adding any comments, explanations, or extraneous text.
Ensure that all functions, variables, function calls, and any other necessary functionality are included and intact.
Make sure the output is in pure code format, with no comment lines or unnecessary modifications to the structure of the code.
Ensure the order and structure of the code in the corrected version is **exactly the same** as the original code, keeping 
the code in the same sequence, without altering the sequence of function definitions, variables, or function calls.
Ensure that the **number of lines of code in the corrected version** remain **exactly the same** as in the original code, 
**with no lines added or removed**. The number of lines in the corrected code must be identical to the original code.
Preserve all **internal comments** **(comments that already existed in the original code)**.
**Do not add any new comments**. Ensure that **spaces** are preserved, and no unnecessary formatting changes are made.
If any comments are added by the LLM, **they must be removed**, but **existing comments** in the code should remain intact.
"""
    
    
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": query + query_manual,
        }],
        model="llama3-8b-8192",  # Adjust to the appropriate model
    )

    # Safeguard: Strip extra whitespace and ensure the content is returned as expected
    response = chat_completion.choices[0].message.content.strip()
    
    # Ensure the full code is returned, checking if there is any sign of truncation
    if response.endswith('...'):
        print("Warning: The response may be incomplete. Please verify the full code.")
        print(response)
    return response



def make_query(query):
    # Updated query to ensure that the order of the code remains the same as the original
    
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": query,
        }],
        model="llama3-8b-8192",  # Adjust to the appropriate model
    )

    # Safeguard: Strip extra whitespace and ensure the content is returned as expected
    response = chat_completion.choices[0].message.content.strip()
    
    # Ensure the full code is returned, checking if there is any sign of truncation
    if response.endswith('...'):
        print("Warning: The response may be incomplete. Please verify the full code.")
    return response