import os
import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None):

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file= os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args is not None:
            command.extend(args)  # pyright: ignore[reportArgumentType]
        subproc = subprocess.run(command, capture_output=True, check = False, text = True, timeout = 30)

        outplist = []
        if subproc.returncode != 0:
            outplist.append(f"Process exited with code {subproc.returncode}")

        if not subproc.stdout and not subproc.stderr:
            outplist.append("No output produced")

        if subproc.stdout:
            outplist.append(f"STDOUT:\n{subproc.stdout}")

        if subproc.stderr:
            outplist.append(f"STDERR:\n{subproc.stderr}")
        beb = "\n".join(outplist)
        return beb

    except Exception as e:
        return f"Error: executing Python file: {e}"
