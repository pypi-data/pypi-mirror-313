import os,sys,subprocess
import importlib
verbose=False
from importlib.metadata import distribution, PackageNotFoundError, distributions
import importlib.resources as pkg_resources
from pkg_resources import get_distribution,DistributionNotFound

def yellow(text):
    print(f"\033[33m{text}\033[0m")
def green(text):
    print(f"\033[32m{text}\033[0m")
def red(text):
    print(f"\033[31m{text}\033[0m")
def white(text):
    print(f"\033[0m{text}\033[0m")

def list_installed_packages():
    """List all installed packages and their versions."""
    for dist in distributions():
        white(f"{dist.metadata['Name']}=={dist.version}")

def check_installed_packages(required_packages):
    """Check if required packages are installed and accessible."""
    missing_packages = []
    for pkg in required_packages:
        try:
            dist = distribution(pkg)
            green(f"{pkg} is installed, version: {dist.version}")
        except PackageNotFoundError:
            red(f"{pkg} is NOT installed.")
            missing_packages.append(pkg)
    return missing_packages

def check_package_resources(package, resource_list):
    """Check if specific resources are available in the package."""
    missing_resources = []
    for resource in resource_list:
        if not pkg_resources.is_resource(package, resource):
            red(f"Resource {resource} in {package} is NOT available.")
            missing_resources.append(resource)
        else:
            green(f"Resource {resource} in {package} is available.")
    return missing_resources

def test_namespace_accessibility(namespaces):
    """Test accessibility of modules in specified namespaces."""
    missing_namespaces = []
    for namespace in namespaces:
        try:
            importlib.import_module(namespace)
            green(f"Namespace '{namespace}' is accessible.")
        except ModuleNotFoundError:
            red(f"Namespace '{namespace}' is NOT accessible.")
            missing_namespaces.append(namespace)
    return missing_namespaces

def test_poetry_virtualenvs():
    try:
        # Run the command and capture the output
        result = subprocess.run(["poetry", "config", "virtualenvs.create"], capture_output=True, text=True)
        
        # Check the output
        if 'true' in result.stdout.strip():
            red("Poetry is configured to create virtual environments, which is not expected.")
            exit(1)
        elif 'false' in result.stdout.strip():
            green("Configuration is correct: Poetry is not creating virtual environments.")
        else:
            red("Unexpected output or error: " + result.stdout)
            exit(1)
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess
        red("Failed to check Poetry configuration: " + str(e))
        exit(1)

def smoke_test():
    if verbose:
        yellow("List of installed packages:")
        list_installed_packages()

    test_poetry_virtualenvs()

    test_namespace_accessibility(["gai",
        "gai.scripts",
        "gai.lib.common",
        "gai.lib.server",
        "gai.ttt",
        "gai.tti",
        "gai.itt",
        "gai.rag",
        "gai.tts",
        ])

if __name__ == "__main__":
    smoke_test()
