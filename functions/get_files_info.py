import os

def get_files_info(working_directory, directory="."):
    try:
        # Step 1: Lock in the "jail"
        # os.path.abspath() converts a relative path to a full absolute path.
        # e.g. "calculator" → "/home/adrian/project/calculator"
        # This is our boundary — the LLM cannot go outside this.
        working_dir_abs = os.path.abspath(working_directory)

        # Step 2: Build the full path to where the LLM wants to look
        # os.path.join() combines two paths safely: "/home/adrian/project/calculator" + "pkg"
        # os.path.normpath() collapses any tricks like "../" into the real path
        # e.g. "calculator/../" becomes "/home/adrian/project" (outside the jail)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Step 3: Check if target_dir is still inside the jail
        # os.path.commonpath() returns the longest shared prefix between two paths.
        # If target_dir is inside working_dir_abs, their common path == working_dir_abs.
        # If the LLM tried "../" to escape, the common path would be SHORTER → False.
        # valid_target_dir is just a boolean: True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        # Step 4: Guard — reject if outside the jail
        # valid_target_dir is the boolean. If False, return an error string.
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Step 5: Guard — reject if target_dir is not actually a directory on disk
        # os.path.isdir() checks the filesystem — is this path a directory?
        # We pass target_dir (the full path string), NOT valid_target_dir (the boolean).
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # TODO: iterate over target_dir and return the directory listing
        collector = []
        for item in os.listdir(target_dir):
            
            name = os.path.join(target_dir, item)
            file_size = os.path.getsize(name)
            is_dir = os.path.isdir(name)
            collector.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
            
        return "\n".join(collector)
    except Exception as e:
        return f"Error:{e}"
