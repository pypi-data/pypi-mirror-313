import os

def create_file(file_path, content=""):
    """
    Create a file at the specified path with optional content.
    """
    with open(file_path, 'w') as file:
        file.write(content)

def create_flask_folder_structure(base_dir="."):
    """
    Create the Flask folder structure in the given directory.
    """
    folder_structure = {
        "app": ["__init__.py"],
        "configuration": ["__init__.py", ".env", "config.py"],
        "database": ["__init__.py", "models.py"],
        "logging": ["logger.py"],
        "routes": ["__init__.py", "route.py"],
        "utils": ["__init__.py", "utils.py"],
    }

    for folder, files in folder_structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            content = "" if file_name != ".env" else "# Add your environment variables here\n"
            create_file(file_path, content)

    run_file_path = os.path.join(base_dir, "run.py")
    create_file(run_file_path, "# Entry point for the Flask application\n")
    print("Flask folder structure created successfully!")
