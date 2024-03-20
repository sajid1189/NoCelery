import os


def filepath_to_module(filepath):
    # Convert the file path to the platform-specific separator
    filepath = os.path.normpath(filepath)

    # Get the base filename without the extension
    module_name = os.path.splitext(os.path.basename(filepath))[0]

    # Get the directory path and convert it to a module path
    dir_path = os.path.dirname(filepath)
    module_path = dir_path.replace(os.path.sep, ".")

    # Return the module name and path
    return f"{module_path}.{module_name}"

