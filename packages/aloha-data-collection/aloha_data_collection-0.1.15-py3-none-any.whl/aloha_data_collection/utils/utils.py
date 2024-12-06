from aloha_data_collection.utils.constants import ALOHA_TASK_PATH
from functools import wraps
from lerobot.common.robot_devices.robots.utils import Robot
from PySide6.QtGui import QImage, QPainter
from typing import Optional, Callable, Any
import yaml


def load_task_config(file_path: str = ALOHA_TASK_PATH) -> Optional[dict]:
    """
    Load a YAML configuration file for tasks and return the parsed data as a dictionary.

    :param file_path: Path to the YAML configuration file. Defaults to ALOHA_TASK_PATH.
    :return: Parsed configuration data as a dictionary, or None if an error occurs.
    """
    try:
        with open(file_path, "r") as file:  # Open the file for reading.
            config_data = yaml.safe_load(file)  # Parse the YAML content.
        return config_data
    except FileNotFoundError:
        print(
            f"Error: The file '{file_path}' was not found."
        )  # Log file not found error.
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")  # Log YAML parsing error.
        return None


def set_image(widget: Any, image: Any) -> None:
    """
    Convert a BGR OpenCV image to RGB format and update the widget with the image.

    :param widget: The widget where the image will be displayed.
    :param image: The image data in OpenCV format (BGR).
    """
    widget.image = QImage(
        image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888
    ).rgbSwapped()  # Convert BGR to RGB and swap channels.
    widget.update()  # Trigger a paint event to refresh the widget.


def paintEvent(widget: Any, event: Any) -> None:
    """
    Handle the widget's paint event to draw an image if available.

    :param widget: The widget to be painted.
    :param event: The paint event object.
    """
    if (
        hasattr(widget, "image") and widget.image is not None
    ):  # Check if the widget has an image.
        painter = QPainter(widget)  # Create a painter for the widget.
        painter.drawImage(
            widget.rect(), widget.image
        )  # Draw the image in the widget's rectangle.


def safe_disconnect(func):
    """
    Decorator to safely disconnect a robot when an exception occurs.

    Ensures that if the decorated function raises an exception, the robot
    is properly disconnected before the exception is propagated.

    :param func: The function to decorate.
    :return: The decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        robot: Optional[object] = None  # Initialize robot as None.

        # Determine the Robot instance from the arguments by checking attributes.
        if len(args) > 0 and hasattr(args[0], "disconnect"):  # Check if the first argument has `disconnect`.
            robot = args[0]
        elif len(args) > 1 and hasattr(args[1], "disconnect"):  # Check if the second argument has `disconnect`.
            robot = args[1]
        else:
            raise ValueError(
                "An object with a `disconnect` method is required as an argument."
            )

        try:
            return func(*args, **kwargs)  # Execute the wrapped function.
        except Exception as e:
            if robot and getattr(robot, "is_connected", False):  # Disconnect the robot if connected.
                robot.disconnect()
            raise e  # Propagate the exception.

    return wrapper
