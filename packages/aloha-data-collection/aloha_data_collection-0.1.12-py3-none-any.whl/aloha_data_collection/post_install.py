import os
import subprocess
import sys
from pathlib import Path
from site import getsitepackages


def install_additional_packages():
    """Clone a specific commit of a GitHub repository and install its dependencies, and fix common issues."""
    repo_url = "https://github.com/huggingface/lerobot.git"
    clone_dir = Path.home() / "lerobot"  # Clone to the user's home directory
    commit_hash = "96c7052777aca85d4e55dfba8f81586103ba8f61"

    # Step 1: Clone the repository if it doesn't exist
    if not clone_dir.exists():
        print(f"Cloning repository from {repo_url} to {clone_dir}...")
        subprocess.check_call(["git", "clone", "--no-checkout", repo_url, str(clone_dir)])
    else:
        print(f"Repository already exists at {clone_dir}. Fetching the latest changes...")
        subprocess.check_call(["git", "fetch"], cwd=str(clone_dir))

    # Step 2: Checkout the specific commit
    print(f"Checking out commit {commit_hash}...")
    subprocess.check_call(["git", "checkout", commit_hash], cwd=str(clone_dir))

    # Step 3: Install the cloned repository with optional dependencies
    print(f"Installing lerobot with optional dependencies from {clone_dir}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", ".[intelrealsense,dynamixel]"], cwd=str(clone_dir))

    try:
        print("Uninstalling opencv-python to resolve camera issues...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "opencv-python"])
    except subprocess.CalledProcessError as e:
        print(f"Error uninstalling opencv-python: {e}. Continuing...")

    try:
        print("Installing OpenCV using Conda...")
        subprocess.check_call(["conda", "install", "-y", "-c", "conda-forge", "opencv=4.5.5"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing OpenCV via Conda: {e}. Continuing...")

    try:
        print("Installing ffmpeg using Conda to fix video encoding errors...")
        subprocess.check_call(["conda", "install", "-y", "-c", "conda-forge", "ffmpeg"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing ffmpeg via Conda: {e}. Continuing...")

def create_desktop_icon():
    """Create a desktop icon dynamically resolving the script path."""
    # Determine the site-packages directory
    site_packages_dir = next((Path(p) for p in getsitepackages() if Path(p).exists()), None)
    if not site_packages_dir:
        print("Site-packages directory not found.")
        return

    # Locate the run_mdc.sh script
    run_mdc_script_path = site_packages_dir / "aloha_data_collection/run_mdc.sh"
    if not run_mdc_script_path.exists():
        print(f"run_mdc.sh script not found at {run_mdc_script_path}")
        return

    # Define the desktop file content
    desktop_file_content = f"""
        [Desktop Entry]
        Version=1.0
        Type=Application
        Name=Aloha Data Collection
        Exec=/bin/bash -c "{run_mdc_script_path}"
        Icon={Path.home()}/.local/share/icons/aloha.png
        Terminal=false
        Categories=Utility;
        """

    # Write the desktop file
    desktop_file_path = Path.home() / ".local/share/applications/aloha_data_collection.desktop"
    desktop_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(desktop_file_path, "w") as desktop_file:
        desktop_file.write(desktop_file_content)

    # Copy the application icon (make sure it's packaged with your app)
    app_icon_path = Path(__file__).resolve().parent / "resources/aloha.png"
    icon_file_path = Path.home() / ".local/share/icons/aloha.png"
    if app_icon_path.exists():
        icon_file_path.parent.mkdir(parents=True, exist_ok=True)
        icon_file_path.write_bytes(app_icon_path.read_bytes())
        print(f"Icon copied to {icon_file_path}")
    else:
        print(f"Icon not found at {app_icon_path}, skipping icon copy.")

    print(f"Desktop icon created at {desktop_file_path}")

def main():
    install_additional_packages()
    create_desktop_icon()
    print("Post-installation tasks completed.")

if __name__ == "__main__":
    main()
