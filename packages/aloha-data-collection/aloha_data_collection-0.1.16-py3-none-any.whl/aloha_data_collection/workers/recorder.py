from PySide6.QtCore import QObject, Signal, Slot


class RecordWorker(QObject):
    """
    Worker class for managing recording operations in a separate thread.

    This class handles interactions with the robot and the main window during the recording
    process, emitting signals for progress updates, image data, and completion status.
    """

    progress = Signal(int)  # Signal for progress updates.
    image_update = Signal(
        int, object
    )  # Signal to send image updates (index and image data).
    finished = Signal()  # Signal emitted when recording is finished.

    def __init__(self, robot: object, main_window: object, **kwargs: dict) -> None:
        """
        Initialize the RecordWorker.

        :param robot: The robot instance used for recording.
        :param main_window: The main window instance to access recording methods.
        :param kwargs: Additional arguments for recording configuration.
        """
        super().__init__()  # Initialize the QObject base class.
        self.robot = robot  # Store the robot instance.
        self.main_window = main_window  # Store the main window instance.
        self.kwargs = kwargs  # Store additional recording configuration.

    @Slot()
    def run(self) -> None:
        """
        Start the recording process.

        This method calls the `record` method of the main window with the provided robot instance
        and configuration. Emits the `finished` signal upon successful completion or in case of an error.
        """
        try:
            self.main_window.record(
                robot=self.robot, **self.kwargs
            )  # Invoke the recording method.
            self.finished.emit()  # Emit the finished signal upon successful completion.
        except Exception as e:
            print(
                f"Error during recording: {e}"
            )  # Log any exceptions that occur during recording.
            self.finished.emit()  # Emit the finished signal even if an error occurs.
