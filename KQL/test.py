import os

# List files and directories in the current directory
current_directory_contents = os.listdir('.')
print(current_directory_contents)


# List files and directories in a specific directory
specific_directory_contents = os.listdir('../python')
print(specific_directory_contents)


# Get the current working directory
current_working_directory = os.getcwd()
print(current_working_directory)


# Create a new directory
os.mkdir('new_directory')


# Remove a directory
os.rmdir('new_directory')


# Check if a file exists
file_exists = os.path.isfile('file.txt')
print(file_exists)

# Check if a directory exists
directory_exists = os.path.isdir('directory')
print(directory_exists)


# Rename a file or directory
os.rename('old_name.txt', 'new_name.txt')


# Remove a file
os.remove('file_to_remove.txt')


# Get the value of an environment variable
path = os.getenv('PATH')
print(path)