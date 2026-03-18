import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    """
    Lists the contents of a directory within the permitted working directory.

    This function is designed to be called by an LLM agent. It enforces a
    strict boundary — the agent can only list directories inside
    `working_directory`. Any attempt to list outside (e.g. via "../") is
    rejected. Each item in the directory is returned with its name, size
    in bytes, and whether it is itself a directory.

    Args:
        working_directory (str): The root directory the agent is allowed to
                                 read within. Acts as a sandbox/jail.
        directory (str):         Relative path to the target directory,
                                 resolved against working_directory.
                                 Defaults to "." (the working directory itself).

    Returns:
        str: A formatted multi-line string listing each item, e.g.:
                 - main.py: file_size=719 bytes, is_dir=False
                 - pkg: file_size=128 bytes, is_dir=True
             Returns an error string prefixed with "Error:" on failure.

    Examples:
        >>> get_files_info("calculator", ".")
        '- main.py: file_size=719 bytes, is_dir=False\\n- pkg: file_size=128 bytes, is_dir=True'

        >>> get_files_info("calculator", "/bin")
        'Error: Cannot list "/bin" as it is outside the permitted working directory'

        >>> get_files_info("calculator", "does_not_exist")
        'Error: "does_not_exist" is not a directory'
    """
    try:
        # Resolve the jail boundary to an absolute path.
        # e.g. "calculator" → "/home/adrian/project/calculator"
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize the full target path.
        # normpath collapses tricks like "../../etc" into their real form.
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Ensure the target is still inside the jail.
        # commonpath() returns the longest shared prefix of both paths.
        # If the agent tried to escape, the common path won't match the jail.
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Reject the request if the path is not a directory.
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Build the directory listing.
        # For each item, record its name, size in bytes, and whether it is a directory.
        # We need the full path (name) for os.path.getsize() and os.path.isdir()
        # to locate the item on disk — item alone is just a filename string.
        collector = []
        for item in os.listdir(target_dir):
            name = os.path.join(target_dir, item)
            file_size = os.path.getsize(name)
            is_dir = os.path.isdir(name)
            collector.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(collector)

    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
name="get_files_info",
description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
