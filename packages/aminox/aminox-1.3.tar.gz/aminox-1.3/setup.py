from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sysconfig

class CustomInstall(install):
    def run(self):
        install.run(self)
        self.execute(self.create_mysql_py, [], msg="Creating mysql.py")
    
    def create_mysql_py(self):
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

setup(
    name='aminox',
    version='1.3',
    packages=find_packages(),
    cmdclass={'install': CustomInstall},
    install_requires=[
        'mysql-connector-python>=8.0',
        'PyQt5>=5.15',
    ],
    description='A package to create PyQt5 Driver connector for MySQL integration automatically',
    author='Med Amine El Ansari',
    author_email='aminemed.elansari@uic.ac.ma',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)