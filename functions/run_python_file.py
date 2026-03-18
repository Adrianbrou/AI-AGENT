import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    """
    Execute a Python file within a permitted working directory.

    Args:
        working_directory (str): The root directory the file must reside in.
        file_path (str): Relative path to the Python file to execute.
        args (list, optional): Additional arguments to pass to the script.

    Returns:
        str: STDOUT/STDERR output, or an error message if execution fails.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Security check: prevent path traversal outside working directory
        if not os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Validate the file exists and is a regular file
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Ensure the file is a Python file
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            text=True
        )

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            return "No output produced"
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the permitted working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to execute",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments to pass to the Python script",
            ),
        },
    ),
)