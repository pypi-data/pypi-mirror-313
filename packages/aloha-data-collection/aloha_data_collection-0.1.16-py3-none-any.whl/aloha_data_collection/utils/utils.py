import yaml
from PySide6.QtGui import QImage, QPainter
from aloha_data_collection.utils.constants import ALOHA_TASK_PATH


def set_image(widget: object, image: object) -> None:
    """
    Convert a BGR OpenCV image to RGB format and update the widget with the image.

    :param widget: The widget where the image will be displayed.
    :param image: The image data in OpenCV format (BGR).
    """
    widget.image = QImage(
        image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888
    ).rgbSwapped()  # Convert BGR to RGB and swap channels.
    widget.update()  # Trigger a paint event to refresh the widget.


def paintEvent(widget: object, event: object) -> None:
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


def load_task_config(file_path: str = ALOHA_TASK_PATH) -> dict | None:
    """
    Load a YAML configuration file for tasks and return the parsed data as a dictionary.

    :param file_path: Path to the YAML configuration file. Defaults to ALOHA_TASK_PATH.
    :return: Parsed configuration data as a dictionary, or None if an error occurs.
    """
    try:
        with open(file_path, "r") as file:  # Open the file for reading.
            config_data = yaml.safe_load(file)  # Parse the YAML content.
        return config_data  # Return the parsed data.
    except FileNotFoundError:
        print(
            f"Error: The file '{file_path}' was not found."
        )  # Log file not found error.
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")  # Log YAML parsing error.
        return None
