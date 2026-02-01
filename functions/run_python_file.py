import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
  try:
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Will be True or False
    valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

    if valid_target_file_path == False:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file_path):
      return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith(".py"):
      return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file_path]

    if args is not None:
      command.extend(args)

    completed_process = subprocess.run(command, capture_output=True, timeout=30, text=True, cwd=working_dir_abs)
    
    output = []

    if completed_process.returncode != 0:
      output.append(f"Process exited with code {completed_process.returncode}")
    
    if completed_process.stdout == "":
      output.append(f"STDOUT:\nNo output produced.")
    else:
      output.append(f"STDOUT:\n{completed_process.stdout}")

    if completed_process.stderr == "":
      output.append(f"STDERR:\nNo ouput produced")
    else:
      output.append(f"STDERR:\n{completed_process.stderr}")
                    
    return "\n".join(output)
  except BaseException as e:
    return f"Error: exectuting Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
  name="run_python_file",
  description="Verifies status of .py file and attempts to run the programs it contains.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    required=["file_path"],
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Path to the target file, relative to the working directory."
      ),
      "args": types.Schema(
        type=types.Type.ARRAY,
        description="A list containing potential arguments to be passed. Will be 'None' if no args passed",
        items=types.Schema(
          type=types.Type.STRING,
          description="A stringified argument to be passed to a function call."
        )
      )
    }
  ),
)