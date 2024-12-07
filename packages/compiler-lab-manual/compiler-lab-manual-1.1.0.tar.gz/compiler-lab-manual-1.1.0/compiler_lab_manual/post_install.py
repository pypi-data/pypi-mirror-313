import os
import shutil

def copy_lab_manuals():
    """Copy lab manuals to the current working directory."""
    package_dir = os.path.dirname(__file__)
    source_dir = os.path.join(package_dir, 'lab_manuals')
    target_dir = os.getcwd()

    try:
        if not os.path.exists(source_dir):
            print("Lab manuals directory not found!")
            return

        for file_name in os.listdir(source_dir):
            full_file_name = os.path.join(source_dir, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, target_dir)
                print(f"Copied {file_name} to {target_dir}")

        print("Lab manuals have been copied successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
