import os
import shutil
from distutils.sysconfig import get_python_lib

def install_sql_file():
    # Get the path to site-packages directory
    site_packages_path = get_python_lib()

    # Path where PyQt5 is installed (you can adjust this based on your specific setup)
    pyqt5_path = os.path.join(site_packages_path, 'PyQt5')

    if os.path.exists(pyqt5_path):
        # Path where sql.py will be copied
        target_path = os.path.join(pyqt5_path, 'sql.py')

        # Get the path of sql.py in the current package
        current_sql_path = os.path.join(os.path.dirname(__file__), 'medSqlConnector', 'sql.py')

        # Copy the sql.py file to the PyQt5 folder
        shutil.copy(current_sql_path, target_path)
        print(f"Successfully copied sql.py to {target_path}")
    else:
        print("PyQt5 directory not found, skipping file copy.")

if __name__ == "__main__":
    install_sql_file()
