from setuptools import setup, find_packages
import os
from setuptools.command.install import install  # Import the 'install' class

import sysconfig

# Function to ensure PyQt5 is installed before running the custom logic
def ensure_pyqt5():
    try:
        import PyQt5
        print("PyQt5 is already installed.")
    except ImportError:
        print("PyQt5 is not installed. Installing now...")
        os.system("pip install PyQt5>=5.15")  # Install PyQt5 via pip

# Custom install command to run the logic
class CustomInstallCommand(install):
    def run(self):
        # Ensure dependencies are installed first
        ensure_pyqt5()

        # Proceed with the default installation
        super().run()

        try:
            import aminox
            print("Successfully imported aminox.")
        except Exception as e:
            print(f"Failed to import aminox: {e}")

# Setup configuration
setup(
    name='aminox',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python>=8.0',  # Ensure MySQL connector is installed
    ],
    cmdclass={'install': CustomInstallCommand},  # Use the custom install command
    description='A package to create PyQt5 Driver connector for MySQL integration automatically.',
    author='Med Amine El Ansari',
    author_email='aminemed.elansari@uic.ac.ma',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
