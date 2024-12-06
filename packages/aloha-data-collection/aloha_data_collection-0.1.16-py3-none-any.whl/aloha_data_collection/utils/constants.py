from pathlib import Path

PACKAGE_ROOT = (
    Path(__file__).resolve().parent.parent
)  # Define the root directory of the package.

ALOHA_ROBOT_PATH = (
    PACKAGE_ROOT / "configs/robot/aloha.yaml"
)  # Path to the robot configuration YAML file.
ALOHA_TASK_PATH = (
    PACKAGE_ROOT / "configs/tasks.yaml"
)  # Path to the task configuration YAML file.

CALIBRATION_OVERRIDE = f"calibration_dir={PACKAGE_ROOT / 'configs/calibration/aloha_default'}"  # Path override for calibration.

DATA_ROOT = "data"  # Root directory for dataset storage.
