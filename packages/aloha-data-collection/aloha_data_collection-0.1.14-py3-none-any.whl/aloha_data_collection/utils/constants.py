from pathlib import Path

# Constants used across the project

# Determine the root directory of the installed package
PACKAGE_ROOT: Path = Path(__file__).resolve().parent.parent

# Path to the YAML configuration file for the robot
ALOHA_ROBOT_PATH: Path = PACKAGE_ROOT / "configs/robot/aloha.yaml"

# Path to the YAML configuration file for tasks
ALOHA_TASK_PATH: Path = PACKAGE_ROOT / "configs/tasks.yaml"

# Path override for calibration configurations
CALIBRATION_OVERRIDE: str = f"calibration_dir={PACKAGE_ROOT / 'configs/calibration/aloha_default'}"

# Root directory for dataset storage
DATA_ROOT: str = "data"
