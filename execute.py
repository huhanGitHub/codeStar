import os
import subprocess
import jsonlines
from tqdm import tqdm
import sys
from glob import glob

import re
import ast
import json
import zipfile
import base64
import shutil
from pprint import pprint

def extract_test(file_contents,function_name):
    """
    Extracts the content after a specified function in a given Python script using the ast module.

    Parameters:
    file_contents (str): The contents of the Python script.
    function_name (str): The name of the function after which the content is to be extracted.

    Returns:
    str: The content of the script after the specified function, or a message if the function is not found.
    """
    try:
        # Parsing the file contents into an AST
        tree = ast.parse(file_contents)

        # Finding the end line number of the specified function
        function_end_line = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                function_end_line = node.end_lineno
                break

        if function_end_line is not None:
            # Splitting the file contents into lines
            lines = file_contents.splitlines()

            # Extracting the content after the specified function
            return "\n".join(lines[function_end_line:]).strip()
        else:
            return "Function not found in the script."
    except Exception as e:
        return f"Error processing the script: {e}"


def extract_content(file_path):
    data = {}
    with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('def'):
                    # Extract the function name
                    start = line.find('def') + 4  # 'def ' has 4 characters
                    end = line.find('(')
                    if end != -1:
                        function_name = line[start:end].strip()
                        if function_name.startswith("f_"):
                            data["task_id"] = function_name
                            break
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip("\n")

        # Extracting the docstring if present
        docstring_start = content.find('"""')
        docstring_end = content.find('"""', docstring_start + 3)
        data["prompt"] = content[:docstring_end + 3]
        tree = ast.parse(content)
        function_end_line = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                function_end_line = node.end_lineno
                break

        if function_end_line is not None:
            lines = content.splitlines()
            function_start_line = content[:docstring_end + 3].count('\n') + 1
            data["canonical_solution"] = "\n".join(lines[function_start_line:function_end_line])
        else:
            data["canonical_solution"] = ""
    data["test"] = extract_test(content,function_name)
    return data


def run_all_cases():
    # split = sys.argv[1]
    # path = sys.argv[2]

    path = r'./data/ming/'
    split = r'./batch_test/'
    if not os.path.isdir(split):
        os.mkdir(split)

    fail_case_log = os.path.join(split, 'failed_case_log.txt')
    fail_count = 0
    with open(f"{split}_split.jsonl", "w") as f:
        # Run the script and capture the output
        with open(fail_case_log, "w") as fp:
            # find all python files in after directory
            python_files = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    if '.py' in file:
                        # if 'after' in root:
                        #     python_files.append(os.path.join(root, file))
                        python_files.append(os.path.join(root, file))

            print('there are %d test cases' % len(python_files))
            prefix = 'path:'
            script_directory = os.path.dirname(os.path.abspath(__file__))
            for file in tqdm(python_files):
                try:
                    result = subprocess.run(
                        ["python", file], capture_output=True, text=True, timeout=30,
                        cwd=script_directory  # Set the working directory to the current script's directory
                    )
                    # Output and error messages
                    error_message = result.stderr
                    if "FAILED" in error_message:
                        fail_count += 1
                        fp.write(prefix + file)
                        fp.write(
                            "\n\n\"\"\"\n\n" + error_message + "\n\n\"\"\"\n\n##################################################\n\n")
                    else:
                        data = extract_content(file)
                        f.write(json.dumps(data))
                        f.write("\n")
                except:
                    fail_count += 1
                    fp.write(prefix + file)
                    fp.write(
                        "\n\n\"\"\"\n\n" + "TIMEOUT" + "\n\n\"\"\"\n\n##################################################\n\n")

    print('there are %d failed cases' % fail_count)


def run_failed_cases(fail_case_log):
    prefix = 'path:'
    execute_files = []
    fail_count = 0
    with open(fail_case_log, "r") as f:
        lines = f.readlines()

        for line in lines:
            if line.startswith(prefix):
                path = line[5:].replace('\n', '')
                execute_files.append(path)

    print('there are %d test cases' % len(execute_files))
    new_fail_case_log = fail_case_log[:-4] + '_' + '.txt'
    script_directory = os.path.dirname(os.path.abspath(__file__))
    with open(new_fail_case_log, "w") as fp:
        for file in tqdm(execute_files):
            try:
                result = subprocess.run(
                    ["python", file], capture_output=True, text=True, timeout=30,
                    cwd=script_directory  # Set the working directory to the current script's directory
                )
                # Output and error messages
                error_message = result.stderr
                prefix = 'path:'
                if "FAILED" in error_message:
                    print("\n" + file)
                    fail_count += 1
                    fp.write(prefix + file)
                    fp.write(
                        "\n\n\"\"\"\n\n" + error_message + "\n\n\"\"\"\n\n##################################################\n\n")
                else:
                    data = extract_content(file)
                    # f.write(json.dumps(data))
                    # f.write("\n")
            except TimeoutError:
                fail_count += 1
                fp.write(prefix + file)
                fp.write(
                    "\n\n\"\"\"\n\n" + "TIMEOUT" + "\n\n\"\"\"\n\n##################################################\n\n")

    print('there are %d failed cases' % fail_count)


def removeBefore():
    path = r'/Users/hhuu0025/PycharmProjects/codeStar/data/apieval_example'
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == 'before':
                os.remove(os.path.join(root, dir))


def unit_script_test():
    # Assuming this function is in the script that you're running
    script_to_run = r'/Users/hhuu0025/PycharmProjects/codeStar/data/ming/f_473_ming.py'

    # Get the directory of the current script (the one containing this function)
    script_directory = os.path.dirname(os.path.abspath(__file__))
    print(script_directory)
    try:
        # Run the target script in the current script's directory
        result = subprocess.run(
            ["python", script_to_run], capture_output=True, text=True, timeout=30,
            cwd=script_directory  # Set the working directory to the current script's directory
        )

        # Print output and error messages
        print("Output:", result.stdout)
        print("Error:", result.stderr)

        # Check the script's execution status
        if result.returncode == 0:
            print("Script executed successfully.")
        else:
            print(f"Script execution failed with return code: {result.returncode}")
    except subprocess.TimeoutExpired as e:
        print("Script timed out:", e)
        print("Partial Standard Output:", e.stdout)
        print("Partial Standard Error:", e.stderr)


if __name__ == '__main__':
    # run_all_cases()
    fail = r'/Users/hhuu0025/PycharmProjects/codeStar/test/failed_case_log.txt'
    # run_failed_cases(fail)
    # removeBefore()

    unit_script_test()