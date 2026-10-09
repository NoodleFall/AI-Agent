import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
   try: # pyright: ignore[reportReturnType]
        working_dir_abs = os.path.abspath(working_directory)
        target_file= os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent = os.path.dirname(target_file)
        os.makedirs(parent, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
   except Exception as error:
       return f"Error: {error}"
