import os
import subprocess
import sys
from pathlib import Path
from site import getsitepackages


# ANSI color codes
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"


def install_additional_packages() -> None:
    """
    Clone a specific commit of the Hugging Face LeRobot repository,
    install its optional dependencies, and fix common issues like camera compatibility.
    """
    # Repository details
    repo_url: str = "https://github.com/huggingface/lerobot.git"
    clone_dir: Path = Path.home() / "lerobot"  # Target directory for cloning
    commit_hash: str = (
        "96c7052777aca85d4e55dfba8f81586103ba8f61"  # Specific commit to checkout
    )

    # Step 1: Clone the repository if not already cloned
    if not clone_dir.exists():
        print(
            f"{Colors.BLUE}Cloning repository from {repo_url} to {clone_dir}...{Colors.RESET}"
        )
        subprocess.check_call(
            [
                "git",
                "clone",
                "--no-checkout",
                repo_url,
                str(clone_dir),
            ]
        )
    else:
        print(
            f"{Colors.BLUE}Repository already exists at {clone_dir}. Fetching the latest changes...{Colors.RESET}"
        )
        subprocess.check_call(
            [
                "git",
                "fetch",
            ],
            cwd=str(clone_dir),
        )

    # Step 2: Checkout the specific commit
    print(f"{Colors.BLUE}Checking out commit {commit_hash}...{Colors.RESET}")
    subprocess.check_call(
        [
            "git",
            "checkout",
            commit_hash,
        ],
        cwd=str(clone_dir),
    )

    # Step 3: Install the repository with optional dependencies
    print(
        f"{Colors.BLUE}Installing lerobot with optional dependencies from {clone_dir}...{Colors.RESET}"
    )
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            ".[intelrealsense,dynamixel]",
        ],
        cwd=str(clone_dir),
    )
    print(
        f"{Colors.GREEN}Successfully installed lerobot and its dependencies!{Colors.RESET}"
    )

    # Step 4: Fix common issues by managing dependencies
    try:
        print(
            f"{Colors.BLUE}Uninstalling opencv-python to resolve camera issues...{Colors.RESET}"
        )
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "uninstall",
                "-y",
                "opencv-python",
            ]
        )
        print(f"{Colors.GREEN}Successfully uninstalled opencv-python!{Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(
            f"{Colors.RED}Error uninstalling opencv-python: {e}. Continuing...{Colors.RESET}"
        )

    try:
        print(f"{Colors.BLUE}Installing OpenCV using Conda...{Colors.RESET}")
        subprocess.check_call(
            [
                "conda",
                "install",
                "-y",
                "-c",
                "conda-forge",
                "opencv=4.5.5",
            ]
        )
        print(f"{Colors.GREEN}Successfully installed OpenCV via Conda!{Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(
            f"{Colors.RED}Error installing OpenCV via Conda: {e}. Continuing...{Colors.RESET}"
        )

    try:
        print(
            f"{Colors.BLUE}Installing ffmpeg using Conda to fix video encoding errors...{Colors.RESET}"
        )
        subprocess.check_call(
            [
                "conda",
                "install",
                "-y",
                "-c",
                "conda-forge",
                "ffmpeg",
            ]
        )
        print(f"{Colors.GREEN}Successfully installed ffmpeg via Conda!{Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(
            f"{Colors.RED}Error installing ffmpeg via Conda: {e}. Continuing...{Colors.RESET}"
        )


def create_desktop_icon() -> None:
    """
    Create a desktop icon for launching the Aloha Data Collection script,
    dynamically resolving the script path and copying the necessary icon.
    """
    # Step 1: Locate the site-packages directory
    site_packages_dir = next(
        (Path(p) for p in getsitepackages() if Path(p).exists()),
        None,
    )
    if not site_packages_dir:
        print(f"{Colors.RED}Site-packages directory not found.{Colors.RESET}")
        return

    # Step 2: Locate the run_mdc.sh script
    run_mdc_script_path = site_packages_dir / "aloha_data_collection/run_mdc.sh"
    if not run_mdc_script_path.exists():
        print(
            f"{Colors.RED}run_mdc.sh script not found at {run_mdc_script_path}{Colors.RESET}"
        )
        return

    # Step 3: Create the desktop entry file
    desktop_file_content: str = f"""
        [Desktop Entry]
        Version=1.0
        Type=Application
        Name=Aloha Data Collection
        Exec=/bin/bash -c "{run_mdc_script_path}"
        Icon={Path.home()}/.local/share/icons/aloha.png
        Terminal=false
        Categories=Utility;
    """
    desktop_file_path: Path = (
        Path.home() / ".local/share/applications/aloha_data_collection.desktop"
    )
    desktop_file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with open(
        desktop_file_path,
        "w",
    ) as desktop_file:
        desktop_file.write(desktop_file_content)

    # Step 4: Copy the application icon
    app_icon_path: Path = Path(__file__).resolve().parent / "resources/aloha.png"
    icon_file_path: Path = Path.home() / ".local/share/icons/aloha.png"
    if app_icon_path.exists():
        icon_file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        icon_file_path.write_bytes(app_icon_path.read_bytes())
        print(f"{Colors.GREEN}Icon copied to {icon_file_path}{Colors.RESET}")
    else:
        print(
            f"{Colors.RED}Icon not found at {app_icon_path}, skipping icon copy.{Colors.RESET}"
        )

    print(f"{Colors.GREEN}Desktop icon created at {desktop_file_path}{Colors.RESET}")


def main() -> None:
    """
    Perform post-installation tasks including package installation and desktop icon creation.
    """
    install_additional_packages()
    create_desktop_icon()
    print(
        f"{Colors.GREEN}Post-installation tasks completed successfully!{Colors.RESET}"
    )


if __name__ == "__main__":
    main()
