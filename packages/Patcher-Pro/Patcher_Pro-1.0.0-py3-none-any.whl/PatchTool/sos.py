import requests
import shlex
from subprocess import Popen, PIPE
import webbrowser
from acllm import make_query
import re
import ast
from func import typeOfFile,get_compiler

def extract_array_from_string(input_string):
    # Use regular expression to extract the portion that looks like a list
    match = re.search(r'\[.*\]', input_string, re.DOTALL)  # re.DOTALL allows dot to match newlines
    if match:
        array_string = match.group(0)  # Extract the matched string
        try:
            # Convert the array string into an actual Python list using ast.literal_eval
            return ast.literal_eval(array_string)
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing array: {e}")
            return None
    else:
        print("No array found in the input string.")
        return None

def execute_and_return(cmd):
    """Execute the external command and get its exitcode, stdout, and stderr."""
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


def make_request(query):
    """Search for solutions to the query on Stack Overflow."""
    print("Searching for " + query)
    try:
        resp = requests.get(f"https://api.stackexchange.com/2.2/search?order=desc&tagged=python&sort=activity&intitle={query}&site=stackoverflow")
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Stack Overflow API: {e}")
        return None


def get_urls(json_dict):
    """Extract URLs of the first 3 answered Stack Overflow posts."""
    if not json_dict or "items" not in json_dict:
        print("No relevant results found on Stack Overflow.")
        return
    
    url_list = []
    count = 0
    for i in json_dict['items']:
        if i["is_answered"]:
            url_list.append(i["link"])
        count += 1
        if count == 3:  # Limit to 3 URLs
            break
    for i in url_list:
        webbrowser.open(i)


def extract_error_message(err):
    """Extracts the error message from the stderr output."""
    return err.decode("utf-8").strip().split("\r\n")[-1]


def extract_output_message(out):
    """Extracts potential output errors from the stdout."""
    return out.decode("utf-8").strip()


def get_test_code(filename):
    """Reads the full code of the given file and returns it."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


def main(filepath:str):

    compiler = get_compiler(filepath)
    
    # Get the code from test.py
    test_code = get_test_code(filepath)
    if not test_code:
        print("No test code found.")
        exit(1)

    # Execute the code and capture stdout and stderr
    out, err = execute_and_return(f"{compiler} {filepath}")

    # If there's an error in stderr, process it
    error_message = extract_error_message(err)

    if error_message:
        print(f"Error Message: {error_message}")

        # Split the error message to create specific queries
        filter_out = error_message.split(":")
        print(filter_out)
        # Make requests to Stack Overflow for solutions
        json1 = make_request(filter_out[0])
        json2 = make_request(filter_out[1])
        json = make_request(error_message)

        # Open URLs from Stack Overflow
        get_urls(json1)
        get_urls(json2)
        get_urls(json)

    else:
        # If there is no error in stderr, check if output has something to search
        output_message = extract_output_message(out)
        if output_message:
            print(f"Output Message: {output_message}")
            response = make_query("""Please provide an array of detailed and precise search strings that can be used to search for solutions to the errors in the following output message. 
            The search strings should be directly extracted from the output message, specifically targeting error codes, status codes, URLs, file paths, specific error messages, exception names, and key phrases indicating the failure. 
            Each string should focus on a unique aspect of the error or failure, ensuring all relevant error details are included. 
            Return the search strings in an array format. 
            Only include error-related strings — no extra text or explanation.
            """ + output_message)

            keywords = extract_array_from_string(response)
            # Perform the search using the output message
            for key in keywords:
                get_urls(make_request(key))
        else:
            print("No errors or relevant output found.")

def sso(filepath:str):
    main(filepath)
