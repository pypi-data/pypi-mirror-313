from PySide6.QtWidgets import (
    QMainWindow,
    QDialog,
    QVBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QMessageBox,
    QApplication,
)
from PySide6.QtCore import QThread, Slot, Qt
from PySide6.QtGui import QImage, QAction
from aloha_data_collection.resources.app import Ui_MainWindow
from lerobot.common.utils.utils import init_hydra_config, log_say
from lerobot.common.robot_devices.robots.factory import make_robot
from lerobot.common.datasets.populate_dataset import add_frame, safe_stop_image_writer
import time
from lerobot.common.robot_devices.utils import busy_wait
from termcolor import colored
import cv2
import logging
from lerobot.common.robot_devices.robots.utils import Robot
from lerobot.common.datasets.populate_dataset import (
    create_lerobot_dataset,
    delete_current_episode,
    init_dataset,
    save_current_episode,
)
from lerobot.common.robot_devices.control_utils import (
    has_method,
    init_policy,
    reset_environment,
    sanity_check_dataset_name,
    stop_recording,
)
from functools import wraps
from typing import List
import yaml
import os

from aloha_data_collection.utils.constants import ALOHA_ROBOT_PATH,ALOHA_TASK_PATH,DATA_ROOT,CALIBRATION_OVERRIDE,PACKAGE_ROOT
from aloha_data_collection.utils.utils import load_task_config, paintEvent, set_image
from aloha_data_collection.workers.recorder import RecordWorker
from aloha_data_collection.workers.yaml import YamlHighlighter


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
        robot = None  # Initialize robot as None.

        # Determine the Robot instance from the arguments.
        if len(args) > 0 and isinstance(args[0], MainWindow):  # Check first argument for MainWindow.
            if len(args) > 1 and isinstance(args[1], Robot):  # Check second argument for Robot.
                robot = args[1]
        elif len(args) > 0 and isinstance(args[0], Robot):  # Check first argument for Robot.
            robot = args[0]
        else:
            raise ValueError(
                "A Robot instance with a `disconnect` method is required as an argument."
            )

        try:
            return func(*args, **kwargs)  # Execute the decorated function.
        except Exception as e:
            if robot and robot.is_connected:  # Disconnect the robot if connected.
                robot.disconnect()
            raise e  # Propagate the exception.

    return wrapper

class MainWindow(QMainWindow):
    """
    Main window class for the Aloha Data Collection application.

    This class initializes the user interface, handles user interactions,
    and manages robot recording tasks.
    """

    def __init__(self) -> None:
        """
        Initialize the main window, set up the UI, and configure event handlers.
        """
        super(MainWindow, self).__init__()  # Call the superclass constructor.
        self.ui = Ui_MainWindow()  # Initialize the UI.
        self.ui.setupUi(self)  # Set up the UI layout and widgets.

        self.thread = None  # Placeholder for the recording thread.

        # Connect the start recording button to the recording function.
        self.ui.pushButton_start_recording.clicked.connect(self.start_recording)

        # Initialize robot configuration.
        robot_cfg = init_hydra_config(
            config_path=ALOHA_ROBOT_PATH, overrides=[CALIBRATION_OVERRIDE]
        )
        self.robot = make_robot(robot_cfg)  # Create the robot instance.

        # Set initial task selection.
        self.selected_task = self.ui.comboBox_task_selection.currentText()
        self.ui.comboBox_task_selection.currentIndexChanged.connect(
            self.on_dataset_selection
        )  # Handle task selection changes.

        self.ui.pushButton_start_recording.setEnabled(True)  # Enable the start button.
        self.set_logs("Application started! Ready to record...")  # Log startup message.

        self.episode_count = self.ui.spinBox_episode_count.value()  # Get the episode count.

        # Connect buttons to update the episode count.
        self.ui.pushButton_episode_count_plus.clicked.connect(
            lambda: self.update_episode_count(1)
        )
        self.ui.pushButton_episode_count_minus.clicked.connect(
            lambda: self.update_episode_count(-1)
        )

        self.tasks_config = load_task_config()  # Load task configurations.

        self.populate_task_combobox()  # Populate the task selection combobox.

        # Dynamically assign methods to each camera widget.
        self.camera_widgets = [
            self.ui.openGLWidget_camera_0,
            self.ui.openGLWidget_camera_1,
            self.ui.openGLWidget_camera_2,
            self.ui.openGLWidget_camera_3,
        ]

        self.placeholder_path = PACKAGE_ROOT / "resources/no_video.jpg"  # Path to the placeholder image.
        self.placeholder_image = None  # Initialize placeholder image.

        self.initialize_image()  # Load and set up the placeholder image.

        # Event flags for recording tasks.
        self.events = {
            "exit_early": False,
            "stop_recording": False,
            "rerecord_episode": False,
        }

        # Connect buttons for re-recording and stopping recording.
        self.ui.pushButton_rerecord.clicked.connect(self.set_rerecord_episode)
        self.ui.pushButton_stop_recording.clicked.connect(self.set_stop_recording)

        # Enable re-recording and stop buttons.
        self.ui.pushButton_rerecord.setEnabled(True)
        self.ui.pushButton_stop_recording.setEnabled(True)

        # Connect menu actions for editing configurations.
        self.ui.actionRobot_Configuration.triggered.connect(self.edit_robot_config)
        self.ui.actionTask_Configuration.triggered.connect(self.edit_task_config)

        # Add a quit action to the menu.
        quit_action = QAction("Quit", self)  # Create the quit action.
        quit_action.setShortcut("Ctrl+Q")  # Assign a keyboard shortcut.
        quit_action.triggered.connect(QApplication.quit)  # Connect to quit the application.
        self.ui.menuQuit.addAction(quit_action)  # Add the quit action to the menu.

    def initialize_image(self) -> None:
        """
        Load and set a placeholder image for all camera widgets.

        This method attempts to load a placeholder image from the specified path
        and assigns it to the camera widgets. If the image cannot be loaded, 
        warnings or errors are printed to the console.
        """
        # Load and convert the placeholder image.
        if os.path.exists(self.placeholder_path):  # Check if the placeholder path exists.
            self.placeholder_image = cv2.imread(str(self.placeholder_path))  # Read the image from the path.
            if self.placeholder_image is not None:
                self.placeholder_image = cv2.cvtColor(
                    self.placeholder_image, cv2.COLOR_BGR2RGB
                )  # Convert image from BGR to RGB.
            else:
                print(f"Error: Unable to load placeholder image {self.placeholder_path}")  # Log an error if loading fails.
                return
        else:
            print(f"Warning: Placeholder image not found at {self.placeholder_path}")  # Log a warning if the path is invalid.
            return

        # Assign the placeholder image to all camera widgets.
        if self.placeholder_image is not None:  # Ensure the placeholder image was loaded.
            for widget in self.camera_widgets:  # Iterate over all camera widgets.
                qimage = QImage(
                    self.placeholder_image.data,
                    self.placeholder_image.shape[1],
                    self.placeholder_image.shape[0],
                    QImage.Format.Format_RGB888,
                )  # Convert OpenCV image to QImage.

                # Assign the converted QImage and related methods to the widget.
                widget.set_image = lambda image=qimage, widget=widget: set_image(widget, image)
                widget.paintEvent = lambda event, widget=widget: paintEvent(widget, event)
                widget.image = qimage  # Initialize the widget with the placeholder image.

                
    def edit_robot_config(self) -> None:
        """
        Open the robot configuration editor.

        This method opens a dialog allowing the user to edit the robot configuration YAML file.
        """
        self.open_edit_dialog("Edit Robot Configuration", ALOHA_ROBOT_PATH)  # Call the open_edit_dialog method.


    def edit_task_config(self) -> None:
        """
        Open the task configuration editor.

        This method opens a dialog allowing the user to edit the task configuration YAML file.
        """
        self.open_edit_dialog("Edit Task Configuration", ALOHA_TASK_PATH)  # Call the open_edit_dialog method.


    def open_edit_dialog(self, title: str, file_path: str) -> None:
        """
        Open a dialog for editing a configuration file.

        This method creates a dialog where the user can view and edit a specified configuration file.
        Changes are validated as YAML before saving.

        :param title: The title of the dialog window.
        :param file_path: The path to the configuration file to be edited.
        """
        self.initialize_image()  # Initialize placeholder images.

        # Create and configure the dialog window.
        dialog = QDialog(self)
        dialog.setWindowTitle(title)  # Set the title of the dialog.
        dialog.setWindowModality(Qt.ApplicationModal)  # Make the dialog modal.
        dialog.resize(800, 600)  # Set the dialog size.

        # Create layout and widgets.
        layout = QVBoxLayout(dialog)
        text_edit = QPlainTextEdit(dialog)  # Text editor for file content.
        save_button = QPushButton("Save", dialog)  # Button to save changes.
        cancel_button = QPushButton("Cancel", dialog)  # Button to cancel changes.

        layout.addWidget(text_edit)  # Add text editor to layout.
        layout.addWidget(save_button)  # Add save button to layout.
        layout.addWidget(cancel_button)  # Add cancel button to layout.

        # Apply YAML syntax highlighting to the text editor.
        yaml_highlighter = YamlHighlighter(text_edit.document())

        # Load the file content into the text editor.
        try:
            with open(file_path, "r") as file:  # Open the file for reading.
                content = file.read()  # Read the file content.
                text_edit.setPlainText(content)  # Display content in the text editor.
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"File not found: {file_path}")  # Show error message for missing file.
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")  # Show error message for other issues.
            return

        # Define the save action.
        def save_changes():
            try:
                yaml.safe_load(text_edit.toPlainText())  # Validate YAML format.

                # Save validated changes to the file.
                with open(file_path, "w") as file:
                    file.write(text_edit.toPlainText())
                QMessageBox.information(
                    self, "Success", f"Changes saved to {file_path}"
                )  # Show success message.
                self.tasks_config = load_task_config()  # Reload the task configuration.
                self.populate_task_combobox()  # Refresh the task selection combobox.
                dialog.accept()  # Close the dialog.
            except yaml.YAMLError as e:
                QMessageBox.critical(self, "Error", f"Invalid YAML format: {e}")  # Show error for invalid YAML.
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")  # Show error for save failure.

        # Define the cancel action.
        def cancel_changes():
            dialog.reject()  # Close the dialog without saving.

        # Connect buttons to their respective actions.
        save_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(cancel_changes)

        dialog.exec()  # Execute the dialog.


    def set_rerecord_episode(self) -> None:
        """
        Trigger re-recording of the current episode.

        Sets the appropriate event flags to indicate that the current episode 
        should be re-recorded and the recording process should exit early.
        """
        self.set_logs("Re-record episode triggered")  # Log the action.
        self.events["rerecord_episode"] = True  # Set re-recording flag.
        self.events["exit_early"] = True  # Indicate that the current recording should exit early.


    def set_stop_recording(self) -> None:
        """
        Stop the recording process.

        Sets the appropriate event flags to indicate that the recording process 
        should stop and exit early.
        """
        self.set_logs("Stop recording triggered")  # Log the action.
        self.events["stop_recording"] = True  # Set stop recording flag.
        self.events["exit_early"] = True  # Indicate that the current recording should exit early.


    def populate_task_combobox(self) -> None:
        """
        Populate the task selection combobox with tasks from the configuration file.

        Clears the existing items in the combobox and adds task names from the loaded
        YAML configuration. Logs a message if no tasks are found.
        """
        self.ui.comboBox_task_selection.clear()  # Clear existing items in the combobox.

        # Populate the combobox with task names from the configuration.
        if self.tasks_config and "tasks" in self.tasks_config:  # Check if tasks exist in the configuration.
            for task in self.tasks_config["tasks"]:  # Iterate over the tasks.
                task_name = task.get("task_name")  # Get the task name.
                if task_name:
                    self.ui.comboBox_task_selection.addItem(task_name)  # Add task name to the combobox.
        else:
            self.set_logs("No tasks found in the configuration file.")  # Log a message if no tasks are found.


    def get_task_parameters(self, task_name: str) -> dict | None:
        """
        Retrieve the configuration of a specific task by its name.

        Searches through the loaded task configuration to find a matching task
        by its name. Logs a message if the task or configuration is not found.

        :param task_name: The name of the task to search for.
        :return: The task configuration as a dictionary if found, otherwise None.
        """
        if not self.tasks_config or "tasks" not in self.tasks_config:  # Check if tasks are loaded.
            self.set_logs("Task configuration not found or tasks not defined.")  # Log error if config is missing.
            return None

        for task in self.tasks_config["tasks"]:  # Iterate over tasks in the configuration.
            if task["task_name"] == task_name:  # Check if the task name matches.
                return task  # Return the matching task configuration.

        self.set_logs(f"Task '{task_name}' not found in configuration.")  # Log message if task is not found.
        return None  # Return None if no match is found.


    @Slot(int)
    def update_progress(self, value: int) -> None:
        """
        Update the progress bar with the given value.

        This method is triggered by a signal to visually indicate progress during recording.

        :param value: The progress value to set (0-100).
        """
        self.ui.progressBar_recording_progress.setValue(value)  # Update the progress bar.


    @Slot(int, object)
    def update_image(self, index: int, image: object) -> None:
        """
        Update the image display for a specified camera widget.

        This method is triggered by a signal to update the displayed image
        for a specific camera widget.

        :param index: The index of the camera widget to update.
        :param image: The image data to display.
        """
        if 0 <= index < len(self.camera_widgets):  # Ensure the index is within range.
            self.camera_widgets[index].set_image(image)  # Update the image in the widget.


    def update_episode_count(self, change: int) -> None:
        """
        Update the episode count by a specified change value.

        Ensures the episode count does not go below zero and updates the corresponding UI element.

        :param change: The value to add to the current episode count.
        """
        self.episode_count += change  # Adjust the episode count.
        if self.episode_count < 0:  # Ensure the count does not go below zero.
            self.episode_count = 0
        self.ui.spinBox_episode_count.setValue(self.episode_count)  # Update the UI element.


    def start_recording(self) -> None:
        """
        Start the recording process for the selected task.

        This method initializes a QThread and a RecordWorker instance to manage
        the recording process. It retrieves the task configuration, sets up the worker,
        connects signals, and starts the recording process.

        :return: None
        """
        task_config = self.get_task_parameters(self.selected_task)  # Retrieve the task configuration.
        if not task_config:  # Handle missing configuration.
            self.set_logs("Unable to find configuration for the selected task.")  # Log an error.
            return

        # Initialize the thread and worker with the task configuration.
        self.thread = QThread()  # Create a new thread.
        self.worker = RecordWorker(  # Set up the recording worker.
            main_window=self,
            robot=self.robot,
            root=DATA_ROOT,
            repo_id=f"{task_config.get('hf_user')}/{self.selected_task}",
            fps=task_config.get("fps", 30),
            warmup_time_s=task_config.get("warmup_time_s", 3),
            episode_time_s=task_config.get("episode_length_s", 10),
            reset_time_s=task_config.get("reset_time_s", 5),
            num_episodes=self.episode_count,
            push_to_hub=task_config.get("push_to_hub", False),
        )

        # Move the worker to the thread.
        self.worker.moveToThread(self.thread)

        # Connect worker signals to relevant slots.
        self.worker.progress.connect(self.update_progress)  # Connect progress updates.
        self.worker.image_update.connect(self.update_image)  # Connect image updates.
        self.worker.finished.connect(self.thread.quit)  # Quit the thread when worker finishes.
        self.worker.finished.connect(self.worker.deleteLater)  # Clean up the worker.
        self.thread.finished.connect(self.thread.deleteLater)  # Clean up the thread.

        self.thread.started.connect(self.worker.run)  # Start the worker when the thread starts.
        self.thread.start()  # Start the thread.

        # Log the start of recording.
        self.set_logs(f"Starting recording with {DATA_ROOT=}, {self.selected_task=}.")  # Log recording details.


    def on_dataset_selection(self, _) -> None:
        """
        Handle changes in the selected dataset from the combobox.

        This method updates the currently selected task based on the user's selection
        in the combobox and logs the change.

        :param _: The current index of the combobox (unused).
        :return: None
        """
        self.selected_task = self.ui.comboBox_task_selection.currentText()  # Get the selected task name.
        self.set_logs(f"Selected new task: {self.selected_task}")  # Log the selection.


    def set_logs(self, logs: str, clear: bool = True) -> None:
        """
        Update the log display with a new log message.

        This method appends or replaces the content of the log display widget
        based on the `clear` parameter.

        :param logs: The log message to display.
        :param clear: Whether to clear existing logs before adding the new message.
        :return: None
        """
        if not clear:  # Append the new log to the existing content.
            logs = self.ui.textBrowser_log.toPlainText() + "\n" + logs
        self.ui.textBrowser_log.setText(logs)  # Update the log display.

    @safe_stop_image_writer
    def control_loop(
        self,
        robot: Robot,
        control_time_s: float | None = None,
        teleoperate: bool = False,
        display_cameras: bool = True,
        dataset: dict | None = None,
        events: dict | None = None,
        policy: object | None = None,
        device: object | None = None,
        use_amp: bool | None = None,
        fps: int | None = None,
    ) -> None:
        """
        Execute a control loop for the robot with optional teleoperation and data recording.

        This method performs the control operations for the robot, updates the display with camera images,
        and records data into a dataset if provided. It supports teleoperation and policy-based control.

        :param robot: The robot instance to control.
        :param control_time_s: The total duration for the control loop in seconds. Defaults to infinite.
        :param teleoperate: Whether to enable teleoperation. Defaults to False.
        :param display_cameras: Whether to display camera images. Defaults to True.
        :param dataset: A dataset dictionary to record observations and actions. Defaults to None.
        :param events: A dictionary of events controlling the loop behavior. Defaults to None.
        :param policy: A policy object for automated control. Defaults to None.
        :param device: The device to execute the policy on. Defaults to None.
        :param use_amp: Whether to use automatic mixed precision. Defaults to None.
        :param fps: The desired frames per second for the control loop. Defaults to None.
        :return: None
        """
        if not robot.is_connected:  # Connect the robot if not already connected.
            robot.connect()

        if events is None:  # Initialize events dictionary if not provided.
            events = {"exit_early": False}

        if control_time_s is None:  # Set control time to infinite if not specified.
            control_time_s = float("inf")

        if teleoperate and policy is not None:  # Validate teleoperation and policy usage.
            raise ValueError("When `teleoperate` is True, `policy` should be None.")

        if dataset is not None and fps is not None and dataset["fps"] != fps:  # Validate dataset FPS.
            raise ValueError(f"The dataset fps should be equal to requested fps ({dataset['fps']} != {fps}).")

        timestamp = 0
        start_episode_t = time.perf_counter()  # Record the start time of the episode.

        while timestamp < control_time_s:  # Run the loop until the specified control time.
            start_loop_t = time.perf_counter()  # Record the loop start time.

            if teleoperate:  # Perform teleoperation if enabled.
                observation, action = robot.teleop_step(record_data=True)

            if dataset is not None:  # Record data into the dataset if provided.
                add_frame(dataset, observation, action)

            if display_cameras:  # Display images from the robot's cameras.
                image_keys = [key for key in observation if "image" in key]  # Filter image-related keys.

                for i, key in enumerate(image_keys[:4]):  # Limit to the first 4 cameras.
                    image = observation[key].numpy()  # Extract image data.
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert image to RGB format.
                    self.worker.image_update.emit(i, rgb_image)  # Emit the updated image signal.

            if fps is not None:  # Enforce the desired frames per second.
                dt_s = time.perf_counter() - start_loop_t  # Calculate loop duration.
                busy_wait(1 / fps - dt_s)  # Wait to maintain the desired FPS.

            dt_s = time.perf_counter() - start_loop_t  # Measure the actual loop duration.
            self.log_control_info(robot, dt_s, fps=fps)  # Log control loop information.

            timestamp = time.perf_counter() - start_episode_t  # Update elapsed time.
            progress_value = int((timestamp / control_time_s) * 100)  # Calculate progress percentage.
            self.worker.progress.emit(progress_value)  # Update progress bar.

            if events["exit_early"]:  # Exit the loop early if the event is triggered.
                events["exit_early"] = False
                break


    def log_control_info(
        self,
        robot: Robot,
        dt_s: float,
        episode_index: int | None = None,
        frame_index: int | None = None,
        fps: int | None = None,
    ) -> None:
        """
        Log timing and performance information for the control loop.

        This method logs information about the control loop's execution time, including
        per-iteration duration and frequencies. It also logs device-specific timing metrics
        for leader arms, follower arms, and cameras.

        :param robot: The robot instance to retrieve log data from.
        :param dt_s: Duration of the control loop iteration in seconds.
        :param episode_index: The current episode index being recorded. Defaults to None.
        :param frame_index: The current frame index being processed. Defaults to None.
        :param fps: The desired frames per second for the control loop. Defaults to None.
        :return: None
        """
        log_items = []  # Collect log information as a list of strings.

        if episode_index is not None:  # Log episode index if provided.
            log_items.append(f"ep:{episode_index}")
        if frame_index is not None:  # Log frame index if provided.
            log_items.append(f"frame:{frame_index}")

        def log_dt(shortname: str, dt_val_s: float) -> None:
            """
            Add timing and frequency information to the log.

            :param shortname: A short description of the metric being logged.
            :param dt_val_s: The duration of the metric in seconds.
            """
            nonlocal log_items, fps
            info_str = f"{shortname}:{dt_val_s * 1000:5.2f}ms ({1 / dt_val_s:3.1f}hz)"  # Format duration and frequency.
            if fps is not None:  # Check for FPS consistency.
                actual_fps = 1 / dt_val_s
                if actual_fps < fps - 1:  # Highlight low FPS in yellow.
                    info_str = colored(info_str, "yellow")
            log_items.append(info_str)  # Add to the log.

        log_dt("dt", dt_s)  # Log total loop time.

        # Log device-specific timing metrics for robots other than "stretch".
        if not robot.robot_type.startswith("stretch"):
            # Log leader arm timings.
            for name in robot.leader_arms:
                key = f"read_leader_{name}_pos_dt_s"
                if key in robot.logs:
                    log_dt("dtRlead", robot.logs[key])

            # Log follower arm write and read timings.
            for name in robot.follower_arms:
                write_key = f"write_follower_{name}_goal_pos_dt_s"
                read_key = f"read_follower_{name}_pos_dt_s"
                if write_key in robot.logs:
                    log_dt("dtWfoll", robot.logs[write_key])
                if read_key in robot.logs:
                    log_dt("dtRfoll", robot.logs[read_key])

            # Log camera read timings.
            for name in robot.cameras:
                key = f"read_camera_{name}_dt_s"
                if key in robot.logs:
                    log_dt(f"dtR{name}", robot.logs[key])

        info_str = " ".join(log_items)  # Combine log items into a single string.
        logging.info(info_str)  # Log the information.

    @safe_disconnect
    def record(
        self,
        robot: Robot,
        root: str,
        repo_id: str,
        pretrained_policy_name_or_path: str | None = None,
        policy_overrides: List[str] | None = None,
        fps: int | None = None,
        warmup_time_s: int = 2,
        episode_time_s: int = 10,
        reset_time_s: int = 5,
        num_episodes: int = 50,
        video: bool = True,
        run_compute_stats: bool = True,
        push_to_hub: bool = True,
        tags: list | None = None,
        num_image_writer_processes: int = 0,
        num_image_writer_threads_per_camera: int = 4,
        force_override: bool = False,
        display_cameras: bool = True,
        play_sounds: bool = True,
    ) -> dict:
        """
        Record episodes of robot operation, optionally using a pretrained policy.

        This method initializes a dataset for recording robot observations and actions.
        It optionally applies a policy for automated operation, handles teleoperation,
        and manages episodes with reset and rerecord functionality.

        :param robot: The robot instance to operate and record.
        :param root: The root directory for storing datasets.
        :param repo_id: The Hugging Face repository ID for the dataset.
        :param pretrained_policy_name_or_path: Path to a pretrained policy (optional).
        :param policy_overrides: Overrides for policy configuration (optional).
        :param fps: Desired frames per second for the recording loop (optional).
        :param warmup_time_s: Duration of the warmup phase in seconds. Defaults to 2.
        :param episode_time_s: Duration of each episode in seconds. Defaults to 10.
        :param reset_time_s: Duration for resetting the environment between episodes. Defaults to 5.
        :param num_episodes: Number of episodes to record. Defaults to 50.
        :param video: Whether to record video during the episodes. Defaults to True.
        :param run_compute_stats: Whether to compute dataset statistics after recording. Defaults to True.
        :param push_to_hub: Whether to push the dataset to Hugging Face Hub. Defaults to True.
        :param tags: Tags for the dataset (optional).
        :param num_image_writer_processes: Number of processes for writing images. Defaults to 0.
        :param num_image_writer_threads_per_camera: Threads per camera for writing images. Defaults to 4.
        :param force_override: Whether to override existing datasets. Defaults to False.
        :param display_cameras: Whether to display camera feeds during recording. Defaults to True.
        :param play_sounds: Whether to play sounds during key events. Defaults to True.
        :return: A dictionary containing the recorded dataset information.
        """
        policy = None
        device = None
        use_amp = None

        # Load pretrained policy if provided
        if pretrained_policy_name_or_path is not None:
            policy, policy_fps, device, use_amp = init_policy(
                pretrained_policy_name_or_path, policy_overrides
            )

            if fps is None:  # Use policy FPS if not specified.
                fps = policy_fps
                logging.warning(f"No fps provided, using policy config FPS ({policy_fps}).")
            elif fps != policy_fps:  # Warn about FPS mismatch.
                logging.warning(f"FPS mismatch: provided ({fps}) vs policy ({policy_fps}).")

        # Create or load the dataset
        sanity_check_dataset_name(repo_id, policy)  # Validate dataset name.
        dataset = init_dataset(
            repo_id,
            root,
            force_override,
            fps,
            video,
            write_images=robot.has_camera,
            num_image_writer_processes=num_image_writer_processes,
            num_image_writer_threads=num_image_writer_threads_per_camera * robot.num_cameras,
        )

        if not robot.is_connected:  # Connect the robot if not already connected.
            robot.connect()

        # Warmup phase
        enable_teleoperation = True
        log_say("Warmup record", play_sounds)
        self.control_loop(
            robot=robot,
            events=self.events,
            teleoperate=enable_teleoperation,
            control_time_s=warmup_time_s,
            display_cameras=display_cameras,
            fps=fps,
        )

        if has_method(robot, "teleop_safety_stop"):  # Perform safety stop if supported.
            robot.teleop_safety_stop()

        # Recording loop
        while True:
            if dataset["num_episodes"] >= num_episodes:  # Stop if enough episodes recorded.
                break

            episode_index = dataset["num_episodes"]
            log_say(f"Recording episode {episode_index}", play_sounds)
            self.control_loop(
                dataset=dataset,
                robot=robot,
                events=self.events,
                control_time_s=episode_time_s,
                display_cameras=display_cameras,
                policy=policy,
                device=device,
                use_amp=use_amp,
                fps=fps,
                teleoperate=True,
            )

            # Reset phase
            if not self.events["stop_recording"] and (
                episode_index < num_episodes - 1 or self.events["rerecord_episode"]
            ):
                log_say("Reset the environment", play_sounds)
                reset_environment(robot, self.events, reset_time_s)

            # Handle rerecord event
            if self.events["rerecord_episode"]:
                log_say("Re-record episode", play_sounds)
                self.events["rerecord_episode"] = False
                self.events["exit_early"] = False
                delete_current_episode(dataset)  # Delete the current episode.
                continue

            save_current_episode(dataset)  # Save the current episode.

            if self.events["stop_recording"]:  # Exit loop if stop event is triggered.
                break

        log_say("Stop recording", play_sounds, blocking=True)
        stop_recording(robot=robot, display_cameras=display_cameras, listener=None)

        # Finalize dataset
        lerobot_dataset = create_lerobot_dataset(
            dataset, run_compute_stats, push_to_hub, tags, play_sounds
        )

        log_say("Exiting", play_sounds)
        return lerobot_dataset

