import shutil
import os

# Delets the 
class PythonPackageCleanUP():
    def __init__():
        pass

    def run():
        folders = ['dist', 'build', '*.egg-info']

        for folder in folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"Deleted {folder}")
            else:
                print(f"{folder} not found")
