import os
import importlib
import warnings
warnings.filterwarnings('ignore')

# Get the current package's directory
package_dir = os.path.dirname(__file__)

# Loop through all files in the package directory
for filename in os.listdir(package_dir):
    # Only import Python files (ignore __init__.py)
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # Remove the .py extension
        # Dynamically import the module
        importlib.import_module(f".{module_name}", package=__name__)