import os


def write_file(working_directory, file_path, content):
    """
    Writes content to a file within the permitted working directory.

    This function is designed to be called by an LLM agent. It enforces a
    strict boundary — the agent can only write files inside `working_directory`.
    Any attempt to write outside (e.g. via "../") is rejected. If parent
    directories are missing, they are created automatically.

    Args:
        working_directory (str): The root directory the agent is allowed to
                                 write within. Acts as a sandbox/jail.
        file_path (str):         Relative path to the target file, resolved
                                 against working_directory.
        content (str):           The string content to write to the file.
                                 Overwrites existing content if the file exists.

    Returns:
        str: A success message with character count on success, or an error
             string prefixed with "Error:" on failure.

    Examples:
        >>> write_file("calculator", "notes.txt", "hello world")
        'Successfully wrote to "notes.txt" (11 characters written)'

        >>> write_file("calculator", "/etc/passwd", "hacked")
        'Error: Cannot write "/etc/passwd" as it is outside the permitted working directory'

        >>> write_file("calculator", "pkg", "data")
        'Error: Cannot write to "pkg" as it is a directory'
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
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        # Reject writes to existing directories — we can only write to files.
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create any missing parent directories.
        # exist_ok=True means this is a no-op if they already exist.
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Write the content, overwriting the file if it already exists.
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"