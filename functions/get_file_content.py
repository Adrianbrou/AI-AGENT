import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    """
    Reads and returns the contents of a file within the permitted working directory.

    This function is designed to be called by an LLM agent. It enforces a
    strict boundary — the agent can only read files inside `working_directory`.
    Any attempt to read outside (e.g. via "../") is rejected. To prevent
    token overuse, reading is capped at MAX_CHARS characters. If the file
    exceeds this limit, a truncation notice is appended to the returned string.

    Args:
        working_directory (str): The root directory the agent is allowed to
                                 read within. Acts as a sandbox/jail.
        file_path (str):         Relative path to the target file, resolved
                                 against working_directory.

    Returns:
        str: The file contents (up to MAX_CHARS characters) on success, with
             an appended truncation message if the file was larger. Returns
             an error string prefixed with "Error:" on failure.

    Examples:
        >>> get_file_content("calculator", "main.py")
        'def main():...'

        >>> get_file_content("calculator", "/etc/passwd")
        'Error: Cannot read "/etc/passwd" as it is outside the permitted working directory'

        >>> get_file_content("calculator", "pkg/does_not_exist.py")
        'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
    """
    try:
        # Resolve the jail boundary to an absolute path.
        # e.g. "calculator" → "/home/adrian/project/calculator"
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize the full target path.
        # normpath collapses tricks like "../../etc/passwd" into their real form.
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Ensure the target is still inside the jail.
        # commonpath() returns the longest shared prefix of both paths.
        # If the agent tried to escape, the common path won't match the jail.
        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Reject the request if the path is not a regular file.
        # This catches missing files and accidental directory reads.
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read up to MAX_CHARS characters to avoid burning through LLM token limits.
        # The read head stops at MAX_CHARS — f.read(1) then checks if anything
        # remains. If it returns a character, the file was truncated.
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"



schema_get_content_info = types.FunctionDeclaration(
name="get_file_content",
description="Reads and returns the contents of a file within the permitted working directory.",
parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Reads and returns the contents of a file within the permitted working directory.",
            ),
        },
    ),
)
