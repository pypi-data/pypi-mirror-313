import sys,nox
import toml

def extract_version_from_toml(file_path):
    with open(file_path, 'r') as toml_file:
        data = toml.load(toml_file)
        return data['tool']['poetry']['version']

# Test for missing files and directories in packages
@nox.session(python=["3.10"])
def smoke_test(session):
    """Session to verify the installation and importability of gai.lib"""

    # This is a hack to install a non-editable local package for completeness testing
    version=extract_version_from_toml("pyproject.toml")
    print(f"Testing version {version}")
    session.run("rm", "-rf", "dist", external=True)
    session.run("poetry", "build", external=True)
    session.run("pip", "install", f"dist/gai_sdk-{version}.tar.gz","-qq",external=True)

    # Proceed with smoke test
    session.run("python", "smoke_test.py")
