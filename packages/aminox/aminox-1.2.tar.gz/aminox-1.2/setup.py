import os
import subprocess
import sys
import sysconfig
from setuptools import setup, find_packages
from setuptools.command.install import install

def ensure_pyqt5():
    """Ensure PyQt5 is installed."""
    try:
        import PyQt5
        print("PyQt5 is already installed.")
    except ImportError:
        print("PyQt5 is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5>=5.15"])

def create_mysql_py():
    """Create mysql.py in PyQt5 directory."""
    try:
        site_packages_path = sysconfig.get_paths()["purelib"]
        pyqt5_dir = os.path.join(site_packages_path, 'PyQt5')
        
        if not os.path.exists(pyqt5_dir):
            print(f"Error: PyQt5 directory not found at {pyqt5_dir}.")
            return
        
        mysql_file_path = os.path.join(pyqt5_dir, 'mysql.py')
        if os.path.exists(mysql_file_path):
            return
        
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
        with open(mysql_file_path, 'w') as f:
            f.write(mysql_py_content)
        print(f"Created {mysql_file_path}")
    except Exception as e:
        print(f"Error creating mysql.py: {e}")

class CustomInstallCommand(install):
    def run(self):
        # Ensure PyQt5 is installed
        ensure_pyqt5()
        
        # Install required dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python>=8.0"])
        
        # Create mysql.py file
        create_mysql_py()
        
        # Proceed with the default installation
        super().run()
        
        try:
            import aminox
            print("Successfully imported aminox.")
        except Exception as e:
            print(f"Failed to import aminox: {e}")

setup(
    name='aminox',
    version='1.2',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python>=8.0',
        'PyQt5>=5.15',
    ],
    cmdclass={'install': CustomInstallCommand},
    description='A package to create PyQt5 Driver connector for MySQL integration automatically.',
    author='Med Amine El Ansari',
    author_email='aminemed.elansari@uic.ac.ma',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)