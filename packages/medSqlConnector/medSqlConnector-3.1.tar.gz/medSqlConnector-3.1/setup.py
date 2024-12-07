import sys
import os
from setuptools import setup
from setuptools.command.install import install
import sysconfig

class CustomInstallCommand(install):
    def run(self):
        # Print message to show the start of the installation process
        print("Starting installation...")

        try:
            # Run the default install process
            install.run(self)

            # Print the Python site-packages directory
            site_packages_path = sysconfig.get_paths()["purelib"]
            print(f"Site-packages path: {site_packages_path}")

            # Absolute path to the PyQt5 directory
            pyqt5_dir = os.path.join(site_packages_path, 'PyQt5')
            print(f"PyQt5 directory: {pyqt5_dir}")

            # Check if the directory exists
            if not os.path.exists(pyqt5_dir):
                print(f"Error: The PyQt5 directory does not exist at {pyqt5_dir}")
                return

            # Define the content for the mysql.py file
            mysql_py_content = """
import mysql.connector

def connect_to_mysql(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Connection failed: {e}")
        return None
"""

            # Define the path where the mysql.py file will be created
            mysql_file_path = os.path.join(pyqt5_dir, 'mysql.py')

            # Print message to show where the file will be created
            print(f"Creating mysql.py at: {mysql_file_path}")

            # Write the content to mysql.py in the PyQt5 folder
            with open(mysql_file_path, 'w') as f:
                f.write(mysql_py_content)

            print(f"Successfully created mysql.py in {pyqt5_dir}")

        except Exception as e:
            # Print any error message that occurs during installation
            print(f"An error occurred: {e}")

# Setup function
setup(
    name='medSqlConnector',
    version='3.1',
    packages=['medSqlConnector'],
    cmdclass={'install': CustomInstallCommand},  # Use the custom install command
)
