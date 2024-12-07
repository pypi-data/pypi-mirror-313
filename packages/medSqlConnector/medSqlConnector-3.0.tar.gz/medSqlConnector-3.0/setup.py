from setuptools import setup
from setuptools.command.install import install
import os
import sysconfig

class CustomInstallCommand(install):
    def run(self):
        # Run the default install process
        install.run(self)

        # Get the site-packages directory path
        site_packages_path = sysconfig.get_paths()["purelib"]
        pyqt5_dir = os.path.join(site_packages_path, 'PyQt5')

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

        # Write the content to mysql.py in the PyQt5 folder
        with open(mysql_file_path, 'w') as f:
            f.write(mysql_py_content)

        print(f"Successfully created mysql.py in {pyqt5_dir}")

# Setup function
setup(
    name='medSqlConnector',
    version='3.0',
    packages=['medSqlConnector'],
    cmdclass={'install': CustomInstallCommand},  # Use the custom install command
    # Add other setup.py configurations as needed
)
