from lerobot.common.robot_devices.robots.utils import Robot
from PySide6.QtCore import QObject, Signal, Slot
from typing import Any, Dict


class RecordWorker(QObject):
    """
    Worker class for handling recording operations in a separate thread.

    This class manages the interaction with the robot and the main window
    during the recording process. Signals are used to update progress,
    images, and notify when the recording is finished.
    """

    progress = Signal(int)  # Signal for progress updates.
    image_update = Signal(
        int, object
    )  # Signal to send image updates (index and image data).
    finished = Signal()  # Signal emitted when recording is finished.

    def __init__(self, robot: Robot, main_window: Any, **kwargs: Dict) -> None:
        """
        Initialize the RecordWorker.

        :param robot: The robot instance used for recording.
        :param main_window: The main window instance to access recording methods.
        :param kwargs: Additional arguments for recording configuration.
        """
        super().__init__()
        self.robot = robot  # Robot instance for recording operations.
        self.main_window = (
            main_window  # Reference to the main window for invoking methods.
        )
        self.kwargs = kwargs  # Additional configuration parameters.

    @Slot()
    def run(self) -> None:
        """
        Start the recording process.

        Invokes the `record` method of the main window with the provided
        robot instance and configuration. Emits the `finished` signal upon
        completion or in case of an exception.
        """
        try:
            self.main_window.record(
                robot=self.robot, **self.kwargs
            )  # Call the recording method.
            self.finished.emit()  # Emit the finished signal upon successful completion.
        except Exception as e:
            print(
                f"Error during recording: {e}"
            )  # Log any exceptions during recording.
            self.finished.emit()  # Emit the finished signal even on failure.
