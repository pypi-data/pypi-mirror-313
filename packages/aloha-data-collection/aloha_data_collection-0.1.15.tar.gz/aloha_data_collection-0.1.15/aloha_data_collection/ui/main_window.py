from aloha_data_collection.utils.constants import ALOHA_ROBOT_PATH,ALOHA_TASK_PATH,CALIBRATION_OVERRIDE, PACKAGE_ROOT,DATA_ROOT
from aloha_data_collection.utils.utils import load_task_config, paintEvent, set_image, safe_disconnect
from aloha_data_collection.workers.record_worker import RecordWorker
from aloha_data_collection.workers.yaml_highlighter import YamlHighlighter
from aloha_data_collection.resources.app import Ui_MainWindow
import cv2
from lerobot.common.datasets.populate_dataset import (
    add_frame,
    create_lerobot_dataset,
    delete_current_episode,
    init_dataset,
    safe_stop_image_writer,
    save_current_episode,
)
from lerobot.common.robot_devices.control_utils import (
    has_method,
    init_policy,
    reset_environment,
    sanity_check_dataset_name,
    stop_recording,
)
from lerobot.common.robot_devices.robots.factory import make_robot
from lerobot.common.robot_devices.robots.utils import Robot
from lerobot.common.robot_devices.utils import busy_wait
from lerobot.common.utils.utils import init_hydra_config, log_say
import logging
import os
from pathlib import Path 
from PySide6.QtCore import QThread, Slot, Qt
from PySide6.QtGui import QImage, QAction
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from termcolor import colored
import time
from typing import Optional, List, Dict, Any
import yaml


class MainWindow(QMainWindow):
    """
    Main window for managing GUI and interactions in the Aloha data collection application.
    """

    def __init__(self) -> None:
        """
        Initialize the main window, set up UI components, and configure robot settings.
        """
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.thread: Optional[QThread] = None  # Placeholder for the recording thread.

        self.ui.pushButton_start_recording.clicked.connect(self.start_recording)  # Connect start recording button.

        robot_cfg = init_hydra_config(config_path=ALOHA_ROBOT_PATH, overrides=[CALIBRATION_OVERRIDE])  # Load robot config.
        self.robot: Robot = make_robot(robot_cfg)  # Initialize the robot.

        self.selected_task: str = self.ui.comboBox_task_selection.currentText()  # Set initial task.
        self.ui.comboBox_task_selection.currentIndexChanged.connect(self.on_dataset_selection)  # Connect task selection.

        self.ui.pushButton_start_recording.setEnabled(True)  # Enable start recording button.
        self.set_logs("Application started! Ready to record...")  # Log application startup.

        self.episode_count: int = self.ui.spinBox_episode_count.value()  # Initialize episode count.

        self.ui.pushButton_episode_count_plus.clicked.connect(lambda: self.update_episode_count(1))  # Increase episodes.
        self.ui.pushButton_episode_count_minus.clicked.connect(lambda: self.update_episode_count(-1))  # Decrease episodes.

        self.tasks_config: Optional[Dict[str, Any]] = load_task_config()  # Load tasks configuration.
        self.populate_task_combobox()  # Populate task selection dropdown.

        self.camera_widgets: List[QWidget] = [  # List of camera widgets.
            self.ui.openGLWidget_camera_0,
            self.ui.openGLWidget_camera_1,
            self.ui.openGLWidget_camera_2,
            self.ui.openGLWidget_camera_3,
        ]

        self.placeholder_path: Path = PACKAGE_ROOT / "resources/no_video.jpg"  # Path to placeholder image.
        self.placeholder_image: Optional[np.ndarray] = None  # Placeholder image storage.
        self.initialize_image()  # Load and initialize placeholder image.

        self.events: Dict[str, bool] = {  # Dictionary to track recording events.
            "exit_early": False,
            "stop_recording": False,
            "rerecord_episode": False,
        }

        self.ui.pushButton_rerecord.clicked.connect(self.set_rerecord_episode)  # Connect re-record button.
        self.ui.pushButton_stop_recording.clicked.connect(self.set_stop_recording)  # Connect stop recording button.

        self.ui.pushButton_rerecord.setEnabled(True)  # Enable re-record button.
        self.ui.pushButton_stop_recording.setEnabled(True)  # Enable stop recording button.

        self.ui.actionRobot_Configuration.triggered.connect(self.edit_robot_config)  # Connect robot config menu.
        self.ui.actionTask_Configuration.triggered.connect(self.edit_task_config)  # Connect task config menu.

        quit_action = QAction("Quit", self)  # Create quit menu action.
        quit_action.setShortcut("Ctrl+Q")  # Add shortcut for quitting.
        quit_action.triggered.connect(QApplication.quit)  # Connect quit action to app exit.
        self.ui.menuQuit.addAction(quit_action)  # Add quit action to menu.


    def initialize_image(self) -> None:
        """
        Load and assign a placeholder image to all camera widgets.

        This method ensures that a default placeholder image is displayed in the
        camera widgets when no live feed is available.
        """
        if os.path.exists(self.placeholder_path):  # Check if the placeholder image path exists.
            self.placeholder_image = cv2.imread(str(self.placeholder_path))  # Load the placeholder image.
            if self.placeholder_image is not None:
                self.placeholder_image = cv2.cvtColor(self.placeholder_image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB.
            else:
                print(f"Error: Unable to load placeholder image {self.placeholder_path}")  # Log error if image loading fails.
                return
        else:
            print(f"Warning: Placeholder image not found at {self.placeholder_path}")  # Log warning if file not found.
            return

        if self.placeholder_image is not None:  # Proceed only if the placeholder image is loaded successfully.
            for widget in self.camera_widgets:  # Iterate through all camera widgets.
                qimage = QImage(
                    self.placeholder_image.data,
                    self.placeholder_image.shape[1],
                    self.placeholder_image.shape[0],
                    QImage.Format.Format_RGB888,
                )  # Create a QImage object from the placeholder image.

                widget.set_image = lambda image=qimage, widget=widget: set_image(widget, image)  # Assign set_image method.
                widget.paintEvent = lambda event, widget=widget: paintEvent(widget, event)  # Assign paintEvent method.

                widget.image = qimage  # Initialize the widget with the placeholder image.

                
    def edit_robot_config(self) -> None:
        """
        Open the robot configuration file in an editable dialog.

        This method allows the user to view and edit the robot configuration
        defined in the file located at ALOHA_ROBOT_PATH.
        """
        self.open_edit_dialog("Edit Robot Configuration", ALOHA_ROBOT_PATH)  # Open dialog with robot config path.


    def edit_task_config(self) -> None:
        """
        Open the task configuration file in an editable dialog.

        This method allows the user to view and edit the task configuration
        defined in the file located at ALOHA_TASK_PATH.
        """
        self.open_edit_dialog("Edit Task Configuration", ALOHA_TASK_PATH)  # Open dialog with task config path.


    
    def open_edit_dialog(self, title: str, file_path: Path) -> None:
        """
        Open a dialog window to edit a configuration file.

        The dialog allows the user to view and modify the contents of the specified
        configuration file. Changes are validated for YAML syntax before saving.

        :param title: The title of the dialog window.
        :param file_path: The path to the configuration file to be edited.
        """
        self.initialize_image()  # Refresh placeholder image before opening the dialog.

        dialog = QDialog(self)  # Create the dialog window.
        dialog.setWindowTitle(title)  # Set the dialog title.
        dialog.setWindowModality(Qt.ApplicationModal)  # Make the dialog modal.
        dialog.resize(800, 600)  # Set the dialog size.

        layout = QVBoxLayout(dialog)  # Create a vertical layout for the dialog.
        text_edit = QPlainTextEdit(dialog)  # Create a text editor for displaying the file content.
        save_button = QPushButton("Save", dialog)  # Create the Save button.
        cancel_button = QPushButton("Cancel", dialog)  # Create the Cancel button.

        layout.addWidget(text_edit)  # Add the text editor to the layout.
        layout.addWidget(save_button)  # Add the Save button to the layout.
        layout.addWidget(cancel_button)  # Add the Cancel button to the layout.

        yaml_highlighter = YamlHighlighter(text_edit.document())  # Apply YAML syntax highlighting to the text editor.

        try:
            with open(file_path, "r") as file:  # Attempt to open the file for reading.
                content = file.read()  # Read the file content.
                text_edit.setPlainText(content)  # Set the file content in the text editor.
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"File not found: {file_path}")  # Show an error message if file not found.
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")  # Show an error message for general exceptions.
            return

        def save_changes() -> None:
            """Handle the Save button click event to validate and save changes."""
            try:
                yaml.safe_load(text_edit.toPlainText())  # Validate YAML syntax.

                with open(file_path, "w") as file:  # Open the file for writing.
                    file.write(text_edit.toPlainText())  # Write the modified content to the file.
                QMessageBox.information(self, "Success", f"Changes saved to {file_path}")  # Show a success message.
                self.tasks_config = load_task_config()  # Reload the task configuration.
                self.populate_task_combobox()  # Update the task dropdown.
                dialog.accept()  # Close the dialog.
            except yaml.YAMLError as e:
                QMessageBox.critical(self, "Error", f"Invalid YAML format: {e}")  # Show an error message for YAML issues.
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")  # Show a general error message.

        def cancel_changes() -> None:
            """Handle the Cancel button click event to discard changes."""
            dialog.reject()  # Close the dialog without saving.

        save_button.clicked.connect(save_changes)  # Connect the Save button to the save_changes function.
        cancel_button.clicked.connect(cancel_changes)  # Connect the Cancel button to the cancel_changes function.

        dialog.exec()  # Execute the dialog.

    def set_rerecord_episode(self) -> None:
        """
        Trigger a re-recording of the current episode.

        Sets the appropriate flags in the events dictionary to indicate that the current
        episode should be re-recorded and the recording process should exit early.
        """
        self.set_logs("Re-record episode triggered")  # Log the re-record event.
        self.events["rerecord_episode"] = True  # Mark the re-record event as true.
        self.events["exit_early"] = True  # Indicate that the recording process should exit early.


    def set_stop_recording(self) -> None:
        """
        Stop the current recording session.

        Sets the appropriate flags in the events dictionary to indicate that the current
        recording session should stop and the process should exit early.
        """
        self.set_logs("Stop recording triggered")  # Log the stop recording event.
        self.events["stop_recording"] = True  # Mark the stop recording event as true.
        self.events["exit_early"] = True  # Indicate that the recording process should exit early.


    def populate_task_combobox(self) -> None:
        """
        Populate the task selection dropdown with tasks from the configuration file.

        Clears the existing items in the dropdown and adds task names defined in the
        loaded YAML configuration. Logs an error if no tasks are found.
        """
        self.ui.comboBox_task_selection.clear()  # Clear existing items in the dropdown.

        if self.tasks_config and "tasks" in self.tasks_config:  # Check if tasks exist in the configuration.
            for task in self.tasks_config["tasks"]:  # Iterate over tasks in the configuration.
                task_name = task.get("task_name")  # Extract the task name.
                if task_name:
                    self.ui.comboBox_task_selection.addItem(task_name)  # Add task name to the dropdown.
        else:
            self.set_logs("No tasks found in the configuration file.")  # Log a warning if no tasks are found.


    def get_task_parameters(self, task_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the configuration parameters for a specific task.

        This method searches the loaded tasks configuration for a task that matches
        the provided task name. If found, it returns the corresponding configuration
        dictionary. Logs an error and returns None if the task is not found or if
        the tasks configuration is missing.

        :param task_name: The name of the task to search for in the configuration.
        :return: A dictionary containing the task's configuration, or None if the task is not found.
        """
        if not self.tasks_config or "tasks" not in self.tasks_config:  # Check if tasks are loaded.
            self.set_logs("Task configuration not found or tasks not defined.")  # Log error if tasks are missing.
            return None

        for task in self.tasks_config["tasks"]:  # Iterate over the tasks in the configuration.
            if task["task_name"] == task_name:  # Check if the task name matches.
                return task  # Return the matching task's configuration.

        self.set_logs(f"Task '{task_name}' not found in configuration.")  # Log error if task not found.
        return None  # Return None if no matching task is found.


    @Slot(int)
    def update_progress(self, value: int) -> None:
        """
        Update the progress bar with the given progress value.

        :param value: The progress value (0-100) to set in the progress bar.
        """
        self.ui.progressBar_recording_progress.setValue(value)  # Update progress bar value.


    @Slot(int, object)
    def update_image(self, index: int, image: Any) -> None:
        """
        Update the specified camera widget with a new image.

        :param index: The index of the camera widget to update.
        :param image: The image data to display in the widget.
        """
        if 0 <= index < len(self.camera_widgets):  # Ensure the index is within bounds.
            self.camera_widgets[index].set_image(image)  # Update the widget image using set_image.


    def update_episode_count(self, change: int) -> None:
        """
        Update the episode count by a specified amount.

        Ensures that the episode count does not go below zero and updates
        the spinbox in the UI with the new value.

        :param change: The value to add to the current episode count.
        """
        self.episode_count += change  # Increment or decrement the episode count.
        if self.episode_count < 0:  # Ensure episode count doesn't go below zero.
            self.episode_count = 0
        self.ui.spinBox_episode_count.setValue(self.episode_count)  # Update the spinbox value in the UI.


    def start_recording(self) -> None:
        """
        Start the recording process for the selected task.

        This method initializes a worker and a thread to handle the recording process
        asynchronously. The task configuration is retrieved, and parameters like FPS,
        warmup time, episode time, and reset time are set based on the selected task.
        Signals are connected to update progress and handle images during recording.

        Logs an error and exits if the task configuration is not found.

        :return: None
        """
        task_config = self.get_task_parameters(self.selected_task)  # Get configuration for the selected task.
        if not task_config:  # Exit if no configuration is found.
            self.set_logs("Unable to find configuration for the selected task.")  # Log error message.
            return

        self.thread = QThread()  # Create a new thread for the worker.
        self.worker = RecordWorker(  # Initialize the worker with task-specific parameters.
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

        self.worker.moveToThread(self.thread)  # Move the worker to the newly created thread.

        self.worker.progress.connect(self.update_progress)  # Connect progress updates to UI.
        self.worker.image_update.connect(self.update_image)  # Connect image updates to UI.

        self.worker.finished.connect(self.thread.quit)  # Ensure the thread quits when the worker finishes.
        self.worker.finished.connect(self.worker.deleteLater)  # Cleanup the worker after finishing.
        self.thread.finished.connect(self.thread.deleteLater)  # Cleanup the thread after finishing.

        self.thread.started.connect(self.worker.run)  # Start the worker when the thread begins execution.
        self.thread.start()  # Begin the thread.

        self.set_logs(f"Starting recording with {DATA_ROOT=}, {self.selected_task=}.")  # Log the start of recording.


    def on_dataset_selection(self, _: int) -> None:
        """
        Handle the selection of a new task from the dropdown.

        Updates the `selected_task` attribute based on the current selection
        in the combo box and logs the selected task.

        :param _: The index of the newly selected item (unused).
        """
        self.selected_task = self.ui.comboBox_task_selection.currentText()  # Get the currently selected task.
        self.set_logs(f"Selected new task: {self.selected_task}")  # Log the selected task.


    def set_logs(self, logs: str, clear: bool = True) -> None:
        """
        Update the log display in the text browser widget.

        If `clear` is False, the new logs are appended to the existing log content.
        Otherwise, the text browser is cleared before displaying the new logs.

        :param logs: The message to display in the logs.
        :param clear: Whether to clear existing logs before setting the new message.
        """
        if not clear:  # Append logs to the existing content if `clear` is False.
            logs = self.ui.textBrowser_log.toPlainText() + "\n" + logs
        self.ui.textBrowser_log.setText(logs)  # Update the text browser with the logs.


    @safe_stop_image_writer
    def control_loop(
        self,
        robot: Robot,
        control_time_s: Optional[float] = None,
        teleoperate: bool = False,
        display_cameras: bool = True,
        dataset: Optional[Dict] = None,
        events: Optional[Dict[str, bool]] = None,
        policy: Optional[Any] = None,
        device: Optional[Any] = None,
        use_amp: Optional[bool] = None,
        fps: Optional[int] = None,
    ) -> None:
        """
        Execute the robot control loop for recording and processing.

        This method handles robot teleoperation, image display, dataset recording,
        and real-time feedback during a recording session. It also respects control
        events such as early exit.

        :param robot: The robot instance to control.
        :param control_time_s: The maximum duration of the control loop in seconds. Defaults to infinity.
        :param teleoperate: Whether to enable manual teleoperation for the robot.
        :param display_cameras: Whether to display camera feeds during the control loop.
        :param dataset: A dictionary for storing dataset frames (if applicable).
        :param events: A dictionary of control events like "exit_early" or "stop_recording".
        :param policy: The policy for automated control (if applicable).
        :param device: The device (e.g., CPU, GPU) for running the policy.
        :param use_amp: Whether to use automatic mixed precision for computations.
        :param fps: Frames per second for the control loop. If None, no FPS constraint is applied.
        """
        if not robot.is_connected:  # Ensure the robot is connected.
            robot.connect()

        if events is None:  # Initialize default events if not provided.
            events = {"exit_early": False}

        if control_time_s is None:  # Default control time to infinity if not specified.
            control_time_s = float("inf")

        if teleoperate and policy is not None:  # Validate conflicting options.
            raise ValueError("When `teleoperate` is True, `policy` should be None.")

        if dataset is not None and fps is not None and dataset["fps"] != fps:  # Validate dataset FPS consistency.
            raise ValueError(f"The dataset fps should match the requested fps ({dataset['fps']} != {fps}).")

        timestamp = 0
        start_episode_t = time.perf_counter()  # Start the episode timer.

        while timestamp < control_time_s:  # Loop until the control time expires or early exit is triggered.
            start_loop_t = time.perf_counter()  # Record the loop start time.

            if teleoperate:  # Perform teleoperation if enabled.
                observation, action = robot.teleop_step(record_data=True)

            if dataset is not None:  # Add observation and action to the dataset if recording.
                add_frame(dataset, observation, action)

            if display_cameras:  # Display images from camera feeds if enabled.
                image_keys = [key for key in observation if "image" in key]  # Filter image keys from observation.
                for i, key in enumerate(image_keys[:4]):  # Limit to 4 cameras.
                    image = observation[key].numpy()
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert BGR to RGB format for display.
                    self.worker.image_update.emit(i, rgb_image)  # Emit image signal to the UI.

            if fps is not None:  # Enforce FPS constraints if specified.
                dt_s = time.perf_counter() - start_loop_t
                busy_wait(1 / fps - dt_s)  # Wait to maintain the desired frame rate.

            dt_s = time.perf_counter() - start_loop_t  # Calculate loop duration.
            self.log_control_info(robot, dt_s, fps=fps)  # Log control loop timing information.

            timestamp = time.perf_counter() - start_episode_t  # Update the elapsed time since the episode started.
            progress_value = int((timestamp / control_time_s) * 100)  # Calculate progress as a percentage.
            self.worker.progress.emit(progress_value)  # Emit progress to the UI.

            if events["exit_early"]:  # Check for early exit event.
                events["exit_early"] = False  # Reset the event flag.
                break  # Exit the control loop.


    def log_control_info(
        self,
        robot: Robot,
        dt_s: float,
        episode_index: Optional[int] = None,
        frame_index: Optional[int] = None,
        fps: Optional[int] = None,
    ) -> None:
        """
        Log control loop timing and performance information.

        This method logs the duration of each control loop step, along with
        additional robot-specific timing data for leader arms, follower arms,
        and cameras. If FPS is provided, highlights if the actual FPS is lower
        than expected.

        :param robot: The robot instance being controlled.
        :param dt_s: The duration of the control loop step in seconds.
        :param episode_index: The index of the current episode, if applicable.
        :param frame_index: The index of the current frame, if applicable.
        :param fps: The target frames per second for the control loop.
        """
        log_items: List[str] = []  # List to hold log messages.

        if episode_index is not None:  # Add episode index to logs if provided.
            log_items.append(f"ep:{episode_index}")
        if frame_index is not None:  # Add frame index to logs if provided.
            log_items.append(f"frame:{frame_index}")

        def log_dt(shortname: str, dt_val_s: float) -> None:
            """
            Log duration and frequency information.

            Highlights the duration in milliseconds and the frequency in Hz. If FPS
            is specified, marks the log yellow if actual FPS is lower than expected.

            :param shortname: Short label for the duration type.
            :param dt_val_s: The duration value in seconds.
            """
            nonlocal log_items, fps
            info_str = f"{shortname}:{dt_val_s * 1000:5.2f} ({1 / dt_val_s:3.1f}hz)"
            if fps is not None:  # Highlight if actual FPS is below target.
                actual_fps = 1 / dt_val_s
                if actual_fps < fps - 1:
                    info_str = colored(info_str, "yellow")  # Use yellow for low FPS warning.
            log_items.append(info_str)  # Add to log items.

        log_dt("dt", dt_s)  # Log total step duration and frequency.

        # TODO: Move robot-specific log logic into robot.print_logs().
        if not robot.robot_type.startswith("stretch"):  # Skip specific logs for 'stretch' robots.
            for name in robot.leader_arms:  # Log timing data for leader arms.
                key = f"read_leader_{name}_pos_dt_s"
                if key in robot.logs:
                    log_dt("dtRlead", robot.logs[key])

            for name in robot.follower_arms:  # Log timing data for follower arms.
                key = f"write_follower_{name}_goal_pos_dt_s"
                if key in robot.logs:
                    log_dt("dtWfoll", robot.logs[key])

                key = f"read_follower_{name}_pos_dt_s"
                if key in robot.logs:
                    log_dt("dtRfoll", robot.logs[key])

            for name in robot.cameras:  # Log timing data for cameras.
                key = f"read_camera_{name}_dt_s"
                if key in robot.logs:
                    log_dt(f"dtR{name}", robot.logs[key])

        info_str = " ".join(log_items)  # Combine all log items into a single string.
        logging.info(info_str)  # Log the information.


    @safe_disconnect
    def record(
        self,
        robot: Robot,
        root: str,
        repo_id: str,
        pretrained_policy_name_or_path: Optional[str] = None,
        policy_overrides: Optional[List[str]] = None,
        fps: Optional[int] = None,
        warmup_time_s: int = 2,
        episode_time_s: int = 10,
        reset_time_s: int = 5,
        num_episodes: int = 50,
        video: bool = True,
        run_compute_stats: bool = True,
        push_to_hub: bool = True,
        tags: Optional[List[str]] = None,
        num_image_writer_processes: int = 0,
        num_image_writer_threads_per_camera: int = 4,
        force_override: bool = False,
        display_cameras: bool = True,
        play_sounds: bool = True,
    ) -> Dict:
        """
        Record episodes using the robot and save data to a dataset.

        This method handles teleoperation, policy execution, and data recording. It manages
        the dataset creation, robot warmup, episode recording, and reset phases. 

        :param robot: The robot instance to record with.
        :param root: The root directory for saving the dataset.
        :param repo_id: The ID of the repository to save or load the dataset from.
        :param pretrained_policy_name_or_path: Path or name of the pretrained policy (optional).
        :param policy_overrides: List of overrides for policy parameters (optional).
        :param fps: Frames per second for the recording. Defaults to None.
        :param warmup_time_s: Duration for robot warmup in seconds. Defaults to 2.
        :param episode_time_s: Duration for each episode in seconds. Defaults to 10.
        :param reset_time_s: Time for resetting the robot between episodes. Defaults to 5.
        :param num_episodes: Number of episodes to record. Defaults to 50.
        :param video: Whether to record video during the episodes. Defaults to True.
        :param run_compute_stats: Whether to compute statistics after recording. Defaults to True.
        :param push_to_hub: Whether to push the dataset to a repository. Defaults to True.
        :param tags: Tags to associate with the dataset (optional).
        :param num_image_writer_processes: Number of processes for image writing. Defaults to 0.
        :param num_image_writer_threads_per_camera: Threads per camera for image writing. Defaults to 4.
        :param force_override: Whether to force override existing dataset. Defaults to False.
        :param display_cameras: Whether to display camera feeds during recording. Defaults to True.
        :param play_sounds: Whether to play sounds during the process. Defaults to True.
        :return: The created dataset dictionary.
        """
        policy = None
        device = None
        use_amp = None

        # Load pretrained policy if provided
        if pretrained_policy_name_or_path:
            policy, policy_fps, device, use_amp = init_policy(pretrained_policy_name_or_path, policy_overrides)

            if fps is None:  # Use policy FPS if not provided
                fps = policy_fps
                logging.warning(f"No fps provided, using policy config FPS ({policy_fps}).")
            elif fps != policy_fps:  # Warn if FPS mismatch
                logging.warning(f"FPS mismatch: provided ({fps}) vs policy config ({policy_fps}).")

        # Validate and initialize the dataset
        sanity_check_dataset_name(repo_id, policy)
        dataset = init_dataset(
            repo_id=repo_id,
            root=root,
            force_override=force_override,
            fps=fps,
            video=video,
            write_images=robot.has_camera,
            num_image_writer_processes=num_image_writer_processes,
            num_image_writer_threads=num_image_writer_threads_per_camera * robot.num_cameras,
        )

        if not robot.is_connected:  # Ensure the robot is connected
            robot.connect()

        # Robot warmup phase
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

        if has_method(robot, "teleop_safety_stop"):
            robot.teleop_safety_stop()

        # Recording loop for episodes
        while True:
            if dataset["num_episodes"] >= num_episodes:  # Stop if the required number of episodes is recorded
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

            # Reset the environment between episodes
            if not self.events["stop_recording"] and (
                (episode_index < num_episodes - 1) or self.events["rerecord_episode"]
            ):
                log_say("Reset the environment", play_sounds)
                reset_environment(robot, self.events, reset_time_s)

            # Handle re-recording
            if self.events["rerecord_episode"]:
                log_say("Re-record episode", play_sounds)
                self.events["rerecord_episode"] = False
                self.events["exit_early"] = False
                delete_current_episode(dataset)
                continue

            # Save the current episode to the dataset
            save_current_episode(dataset)

            if self.events["stop_recording"]:  # Exit if stop recording is triggered
                break

        # Finalize recording
        log_say("Stop recording", play_sounds, blocking=True)
        stop_recording(robot=robot, display_cameras=display_cameras, listener=None)

        # Create and return the dataset
        lerobot_dataset = create_lerobot_dataset(
            dataset=dataset,
            run_compute_stats=run_compute_stats,
            push_to_hub=push_to_hub,
            tags=tags,
            play_sounds=play_sounds,
        )

        log_say("Exiting", play_sounds)
        return lerobot_dataset
