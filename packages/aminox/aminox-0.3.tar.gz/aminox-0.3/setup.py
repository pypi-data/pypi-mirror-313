from setuptools import setup
from setuptools.command.install import install
import subprocess
import sys

# Custom install command that installs PyQt5 first
class CustomInstallCommand(install):
    def run(self):
        # First, install PyQt5
        print("Installing PyQt5...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
            print("PyQt5 installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing PyQt5: {e}")
            return

        # Now run the normal install process for aminox
        install.run(self)

setup(
    name='aminox',
    version='0.3',
    packages=['aminox'],
    cmdclass={'install': CustomInstallCommand},  # Use the custom install command
)
