import os
import shutil

def read_file(file_path):
    """Reads the content of a file and returns it."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()  # Read the file content
            print(f"Content of '{file_path}':\n{content}")  # Print the content
            return content  # Return the content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None  # Return None if file does not exist
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None for any other error


def write_file(file_path, content):
    """Writes the given content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)  # Write the content to the file
            print(f"Content written to '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def get_current_directory():
    """Returns the current working directory."""
    current_directory = os.getcwd()  # Get the current working directory
    print(f"Current Directory: {current_directory}")  # Print the current directory
    return  current_directory  # Return the current directory

def delete_file(file_path):
    """Deletes the specified file."""
    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

def copy_file(source_path, destination_path):
    """Copies a file from source to destination."""
    try:
        shutil.copy2(source_path, destination_path)
        print(f"Copied file from {source_path} to {destination_path}")
    except FileNotFoundError:
        print(f"Source file not found: {source_path}")
    except Exception as e:
        print(f"Error copying file: {e}")

def move_file(source_path, destination_path):
    """Moves a file from source to destination."""
    try:
        shutil.move(source_path, destination_path)
        print(f"Moved file from {source_path} to {destination_path}")
    except FileNotFoundError:
        print(f"Source file not found: {source_path}")
    except Exception as e:
        print(f"Error moving file: {e}")