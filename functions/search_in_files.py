import os
from google.genai import types


def search_in_files(working_directory, pattern, directory="."):
    """
    Search for a text pattern across all files in a directory recursively.

    Args:
        working_directory (str): The sandboxed root directory.
        pattern (str): The string to search for.
        directory (str): Subdirectory to search in, relative to working_directory.

    Returns:
        str: Matching lines with file path and line number, or an error string.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            return f'Error: Cannot search "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        results = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            if pattern in line:
                                relative_path = os.path.relpath(file_path, working_dir_abs)
                                results.append(f"{relative_path}:{line_num}: {line.rstrip()}")
                except Exception:
                    continue

        if not results:
            return f'No matches found for "{pattern}"'

        return "\n".join(results)

    except Exception as e:
        return f"Error: {e}"


schema_search_in_files = types.FunctionDeclaration(
    name="search_in_files",
    description="Search for a text pattern across all files in a directory recursively, returning matching lines with file path and line number",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "pattern": types.Schema(
                type=types.Type.STRING,
                description="The text pattern to search for",
            ),
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory to search in, relative to working directory (default is working directory itself)",
            ),
        },
        required=["pattern"],
    ),
)