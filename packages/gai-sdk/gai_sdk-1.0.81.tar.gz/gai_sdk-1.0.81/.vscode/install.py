import subprocess
import os
import glob

def run_command(command):
    """Executes a shell command and returns the output and error if any."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr

def build_package():
    """Builds the package using poetry build and returns the path to the generated wheel file."""

    # Build the package
    stdout, stderr = run_command(["poetry", "build"])
    if stderr:
        print(f"Error during package build:{stderr}")
        return None
    print(stdout)

    # Find the wheel file in dist directory
    wheel_files = glob.glob('dist/*.whl')
    if wheel_files:
        # Assuming the latest built wheel file is the one we want (last modified)
        return max(wheel_files, key=os.path.getmtime)
    else:
        print("No wheel file found in dist directory.")
        return None

def install_wheel(wheel_path):
    """Installs a wheel file using pip."""
    if wheel_path:
        stdout, stderr = run_command(["pip", "install", wheel_path,"--force-reinstall"])
        if stderr:
            print(f"Error during wheel installation:{stderr}")
        else:
            print(f"Wheel installed successfully.\n{stdout}")
    else:
        print("Installation skipped as no wheel path was provided.")

def main():
    print("Starting the build process...")
    wheel_path = build_package()
    if wheel_path:
        print(f"[green]Wheel built at {wheel_path}. Starting installation...")
        os.system("which python")
        install_wheel(wheel_path)
    else:
        print("[red]Build failed or no wheel file was produced.")

if __name__ == "__main__":
    main()
