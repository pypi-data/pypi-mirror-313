import os
from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        # Print message to show the start of the installation process
        print("Starting installation...")

        try:
            # Run the default install process
            install.run(self)

            # Define the package directory (same directory as setup.py)
            package_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"Package directory: {package_dir}")

            # Define the path where the test file will be created
            test_file_path = os.path.join(package_dir, 'test_file.txt')

            # Print message to show where the file will be created
            print(f"Creating test file at: {test_file_path}")

            # Create a simple test file
            with open(test_file_path, 'w') as f:
                f.write("This is a test file created during installation.")

            print(f"Successfully created test_file.txt in {package_dir}")

        except Exception as e:
            # Print any error message that occurs during installation
            print(f"An error occurred: {e}")

# Setup function
setup(
    name='aminox',
    version='0.1',
    packages=['aminox'],  # Ensure you have a package folder named 'aminox'
    cmdclass={'install': CustomInstallCommand},  # Use the custom install command
)
