import os

def write_file(working_directory, file_path, content):
  working_dir_abs = os.path.abspath(working_directory)
  target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

  # Will be True or False
  valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

  if valid_target_file_path == False:
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
  if os.path.isdir(file_path):
    return f'Error: Cannot write to "{file_path}" as it is a directory'
  
  os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

  with open(target_file_path, 'w') as f:
    f.write(content)

  return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

