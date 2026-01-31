import os

def get_files_info(working_directory, directory="."):
  working_dir_abs = os.path.abspath(working_directory)
  target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

  # Will be True or False
  valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

  if valid_target_dir == False:
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  
  if not os.path.isdir(target_dir):
    return f'Error: "{directory}" is not a directory'
  
  dir_contents = os.listdir(target_dir)

  output = []

  for item in dir_contents:
    path = os.path.join(target_dir, item)
    output.append(f"- {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}")

  return "\n".join(output)

  
