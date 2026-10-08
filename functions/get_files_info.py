import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'

        if os.path.isdir(target_dir) == True:
            try:
                file_information = []
                file_list = os.listdir(target_dir)
                for file in file_list:
                    join_path = os.path.join(target_dir, file)
                    file_information.append(f"- {file}: file_size={os.path.getsize(join_path)} bytes, is_dir={os.path.isdir(join_path)}")
                joined_strings = "\n".join(file_information)

                #return f'Success: "{directory}" is within the working directory'
                return joined_strings
            except Exception as e:
                return f"Error: {e}"

    except Exception as error:
        return f"Error: {error}"
