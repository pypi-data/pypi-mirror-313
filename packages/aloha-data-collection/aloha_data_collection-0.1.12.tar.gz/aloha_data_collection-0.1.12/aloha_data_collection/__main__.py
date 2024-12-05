import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QDialog,
    QVBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QMessageBox,
    QApplication,
)
from PySide6.QtCore import QThread, QObject, Signal, Slot, Qt, QRegularExpression
from PySide6.QtGui import QColor, QImage, QPainter, QAction, QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from aloha_data_collection.resources.app import Ui_MainWindow
from lerobot.common.utils.utils import init_hydra_config, log_say
from lerobot.common.robot_devices.robots.factory import make_robot
from lerobot.common.datasets.populate_dataset import add_frame, safe_stop_image_writer
import time
from concurrent.futures import ThreadPoolExecutor
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
    init_keyboard_listener,
    init_policy,
    reset_environment,
    sanity_check_dataset_name,
    stop_recording,
)
from functools import wraps
from typing import List
import yaml
from pathlib import Path
import os


# Get the root directory of the installed package
PACKAGE_ROOT = Path(__file__).resolve().parent

ALOHA_ROBOT_PATH = PACKAGE_ROOT / "configs/robot/aloha.yaml"
ALOHA_TASK_PATH = PACKAGE_ROOT / "configs/tasks.yaml"

calibration_override = (
    f"calibration_dir={PACKAGE_ROOT / 'configs/calibration/aloha_default'}"
)

DATA_ROOT = "data"


def load_task_config(file_path=ALOHA_TASK_PATH):
    """
    Load a YAML configuration file for tasks and return the parsed data as a dictionary.

    Args:
        file_path (str): Path to the YAML configuration file.

    Returns:
        dict: Parsed configuration data.
    """
    try:
        with open(file_path, "r") as file:
            config_data = yaml.safe_load(file)
        return config_data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None


def safe_disconnect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Initialize robot as None
        robot = None

        # Check if the first argument is an instance of MainWindow
        if len(args) > 0 and isinstance(args[0], MainWindow):
            # If the second argument is a Robot, assign it to `robot`
            if len(args) > 1 and isinstance(args[1], Robot):
                robot = args[1]
        # Otherwise, check if the first argument itself is a Robot
        elif len(args) > 0 and isinstance(args[0], Robot):
            robot = args[0]
        else:
            raise ValueError(
                "A Robot instance with a `disconnect` method is required as an argument."
            )

        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Only call `disconnect` if `robot` is set and connected
            if robot and robot.is_connected:
                robot.disconnect()
            raise e

    return wrapper


class RecordWorker(QObject):
    progress = Signal(int)  # Signal for progress updates
    # Signal to send images (index and image data)
    image_update = Signal(int, object)
    finished = Signal()  # Signal when recording is finished

    def __init__(self, robot, main_window, **kwargs):
        super().__init__()
        self.robot = robot
        self.main_window = main_window
        self.kwargs = kwargs

    @Slot()
    def run(self):
        try:
            self.main_window.record(robot=self.robot, **self.kwargs)
            self.finished.emit()  # Emit the finished signal when done
        except Exception as e:
            print(f"Error during recording: {e}")
            self.finished.emit()


def set_image(widget, image):
    # Convert BGR OpenCV image to RGB and store it
    widget.image = QImage(
        image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888
    ).rgbSwapped()
    widget.update()  # Trigger a paint event to refresh the widget


def paintEvent(widget, event):
    if hasattr(widget, "image") and widget.image is not None:
        painter = QPainter(widget)
        painter.drawImage(widget.rect(), widget.image)



class YamlHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        key_format = QTextCharFormat()
        key_format.setForeground(QColor("blue"))
        key_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r"^\s*[\w\-]+(?=\s*:)"), key_format))

        value_format = QTextCharFormat()
        value_format.setForeground(QColor("darkgreen"))
        self.highlighting_rules.append((QRegularExpression(r":\s*.*"), value_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("gray"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.thread = None  # Placeholder for the recording thread

        self.ui.pushButton_start_recording.clicked.connect(self.start_recording)

        robot_cfg = init_hydra_config(
            config_path=ALOHA_ROBOT_PATH, overrides=[calibration_override]
        )
        self.robot = make_robot(robot_cfg)

        # Set initial task
        self.selected_task = self.ui.comboBox_task_selection.currentText()
        self.ui.comboBox_task_selection.currentIndexChanged.connect(
            self.on_dataset_selection
        )

        self.ui.pushButton_start_recording.setEnabled(True)
        self.set_logs("Application started! Ready to record...")

        self.episode_count = self.ui.spinBox_episode_count.value()

        self.ui.pushButton_episode_count_plus.clicked.connect(
            lambda: self.update_episode_count(1)
        )

        self.ui.pushButton_episode_count_minus.clicked.connect(
            lambda: self.update_episode_count(-1)
        )

        self.tasks_config = load_task_config()

        self.populate_task_combobox()

        # Dynamically assign methods to each widget once
        self.camera_widgets = [
            self.ui.openGLWidget_camera_0,
            self.ui.openGLWidget_camera_1,
            self.ui.openGLWidget_camera_2,
            self.ui.openGLWidget_camera_3,
        ]

        for widget in self.camera_widgets:
            widget.set_image = lambda image, widget=widget: set_image(widget, image)
            widget.paintEvent = lambda event, widget=widget: paintEvent(widget, event)
            widget.image = None  # Initialize an attribute to store the image

        self.events = {}
        self.events["exit_early"] = False
        self.events["stop_recording"] = False
        self.events["rerecord_episode"] = False

        self.ui.pushButton_rerecord.clicked.connect(self.set_rerecord_episode)
        self.ui.pushButton_stop_recording.clicked.connect(self.set_stop_recording)

        self.ui.pushButton_rerecord.setEnabled(True)
        self.ui.pushButton_stop_recording.setEnabled(True)

        self.ui.actionRobot_Configuration.triggered.connect(self.edit_robot_config)
        self.ui.actionTask_Configuration.triggered.connect(self.edit_task_config)

        quit_action = QAction("Quit", self)  # Pass the correct parent
        quit_action.setShortcut("Ctrl+Q")  # Optional shortcut
        quit_action.triggered.connect(QApplication.quit)  # Connect to quit the application
        self.ui.menuQuit.addAction(quit_action)

    def edit_robot_config(self):
        self.open_edit_dialog("Edit Robot Configuration", ALOHA_ROBOT_PATH)

    def edit_task_config(self):
        self.open_edit_dialog("Edit Task Configuration", ALOHA_TASK_PATH)

    
    def open_edit_dialog(self, title, file_path):
        # Create a dialog for editing the file
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(800, 600)

        # Layout and Widgets
        layout = QVBoxLayout(dialog)
        text_edit = QPlainTextEdit(dialog)
        save_button = QPushButton("Save", dialog)
        cancel_button = QPushButton("Cancel", dialog)

        layout.addWidget(text_edit)
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)

        # Apply YAML syntax highlighting
        yaml_highlighter = YamlHighlighter(text_edit.document())

        # Load file content into the editor
        try:
            with open(file_path, "r") as file:
                content = file.read()
                text_edit.setPlainText(content)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"File not found: {file_path}")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")
            return

        # Handle Save Button Click
        def save_changes():
            try:
                # Parse YAML to validate changes before saving
                yaml.safe_load(text_edit.toPlainText())

                # Save changes to the file
                with open(file_path, "w") as file:
                    file.write(text_edit.toPlainText())
                QMessageBox.information(
                    self, "Success", f"Changes saved to {file_path}"
                )
                self.tasks_config = load_task_config()
                self.populate_task_combobox()
                dialog.accept()
            except yaml.YAMLError as e:
                QMessageBox.critical(self, "Error", f"Invalid YAML format: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

        # Handle Cancel Button Click
        def cancel_changes():
            dialog.reject()

        save_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(cancel_changes)

        dialog.exec()

    def set_rerecord_episode(self):
        self.set_logs("Re-record episode triggered")
        self.events["rerecord_episode"] = True
        self.events["exit_early"] = True

    def set_stop_recording(self):
        self.set_logs("Stop recording triggered")
        self.events["stop_recording"] = True
        self.events["exit_early"] = True

    def populate_task_combobox(self):
        # Clear existing items in the combobox
        self.ui.comboBox_task_selection.clear()

        # Populate combobox with task names from the YAML config
        if self.tasks_config and "tasks" in self.tasks_config:
            for task in self.tasks_config["tasks"]:
                task_name = task.get("task_name")
                if task_name:
                    self.ui.comboBox_task_selection.addItem(task_name)
        else:
            self.set_logs("No tasks found in the configuration file.")

    def get_task_parameters(self, task_name):
        # Find the task in the loaded configuration that matches the selected task
        if not self.tasks_config or "tasks" not in self.tasks_config:
            self.set_logs("Task configuration not found or tasks not defined.")
            return None

        for task in self.tasks_config["tasks"]:
            if task["task_name"] == task_name:
                return task  # Return the task configuration as a dictionary

        self.set_logs(f"Task '{task_name}' not found in configuration.")
        return None

    @Slot(int)
    def update_progress(self, value):
        # Update the progress bar from the signal
        self.ui.progressBar_recording_progress.setValue(value)

    @Slot(int, object)
    def update_image(self, index, image):
        if 0 <= index < len(self.camera_widgets):
            # Use set_image to update the widget image
            self.camera_widgets[index].set_image(image)

    def update_episode_count(self, change):
        self.episode_count += change
        if self.episode_count < 0:
            self.episode_count = 0
        self.ui.spinBox_episode_count.setValue(self.episode_count)

    def start_recording(self):
        task_config = self.get_task_parameters(self.selected_task)
        if not task_config:
            self.set_logs("Unable to find configuration for the selected task.")
            return

        # Set up the thread and worker with the task configuration
        self.thread = QThread()
        self.worker = RecordWorker(
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

        # Move the worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals for worker
        self.worker.progress.connect(self.update_progress)
        self.worker.image_update.connect(self.update_image)
        # Quit the thread after finishing
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)  # Cleanup worker
        self.thread.finished.connect(self.thread.deleteLater)  # Cleanup thread

        self.thread.started.connect(self.worker.run)
        self.thread.start()

        self.set_logs(f"Starting recording with {DATA_ROOT=}, {self.selected_task=}.")

    def on_dataset_selection(self, _):
        self.selected_task = self.ui.comboBox_task_selection.currentText()
        self.set_logs(f"Selected new task: {self.selected_task}")

    def set_logs(self, logs, clear=True):
        if not clear:
            logs = self.ui.textBrowser_log.toPlainText() + "\n" + logs
        self.ui.textBrowser_log.setText(logs)

    @safe_stop_image_writer
    def control_loop(
        self,
        robot,
        control_time_s=None,
        teleoperate=False,
        display_cameras=True,
        dataset=None,
        events=None,
        policy=None,
        device=None,
        use_amp=None,
        fps=None,
    ):
        # TODO(rcadene): Add option to record logs
        if not robot.is_connected:
            robot.connect()

        if events is None:
            events = {"exit_early": False}

        if control_time_s is None:
            control_time_s = float("inf")

        if teleoperate and policy is not None:
            raise ValueError("When `teleoperate` is True, `policy` should be None.")

        if dataset is not None and fps is not None and dataset["fps"] != fps:
            raise ValueError(
                f"The dataset fps should be equal to requested fps ({dataset['fps']} != {fps})."
            )

        timestamp = 0
        start_episode_t = time.perf_counter()
        while timestamp < control_time_s:
            start_loop_t = time.perf_counter()

            if teleoperate:
                observation, action = robot.teleop_step(record_data=True)

            if dataset is not None:
                add_frame(dataset, observation, action)

            if display_cameras:
                # Filter only the keys that contain images
                image_keys = [key for key in observation if "image" in key]

                for i, key in enumerate(image_keys[:4]):  # Limit to 4 cameras
                    image = observation[key].numpy()
                    # Convert BGR (OpenCV) to RGB format for Qt display
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    self.worker.image_update.emit(i, rgb_image)  # Emit image signal

            if fps is not None:
                dt_s = time.perf_counter() - start_loop_t
                busy_wait(1 / fps - dt_s)

            dt_s = time.perf_counter() - start_loop_t
            self.log_control_info(robot, dt_s, fps=fps)

            timestamp = time.perf_counter() - start_episode_t
            progress_value = int((timestamp / control_time_s) * 100)
            self.worker.progress.emit(progress_value)
            if events["exit_early"]:
                events["exit_early"] = False
                break

    def log_control_info(
        self, robot: Robot, dt_s, episode_index=None, frame_index=None, fps=None
    ):
        log_items = []
        if episode_index is not None:
            log_items.append(f"ep:{episode_index}")
        if frame_index is not None:
            log_items.append(f"frame:{frame_index}")

        def log_dt(shortname, dt_val_s):
            nonlocal log_items, fps
            info_str = f"{shortname}:{dt_val_s * 1000:5.2f} ({1/ dt_val_s:3.1f}hz)"
            if fps is not None:
                actual_fps = 1 / dt_val_s
                if actual_fps < fps - 1:
                    info_str = colored(info_str, "yellow")
            log_items.append(info_str)

        # total step time displayed in milliseconds and its frequency
        log_dt("dt", dt_s)

        # TODO(aliberts): move robot-specific logs logic in robot.print_logs()
        if not robot.robot_type.startswith("stretch"):
            for name in robot.leader_arms:
                key = f"read_leader_{name}_pos_dt_s"
                if key in robot.logs:
                    log_dt("dtRlead", robot.logs[key])

            for name in robot.follower_arms:
                key = f"write_follower_{name}_goal_pos_dt_s"
                if key in robot.logs:
                    log_dt("dtWfoll", robot.logs[key])

                key = f"read_follower_{name}_pos_dt_s"
                if key in robot.logs:
                    log_dt("dtRfoll", robot.logs[key])

            for name in robot.cameras:
                key = f"read_camera_{name}_dt_s"
                if key in robot.logs:
                    log_dt(f"dtR{name}", robot.logs[key])

        info_str = " ".join(log_items)
        logging.info(info_str)

    @safe_disconnect
    def record(
        self,
        robot: Robot,
        root: str,
        repo_id: str,
        pretrained_policy_name_or_path: str | None = None,
        policy_overrides: List[str] | None = None,
        fps: int | None = None,
        warmup_time_s=2,
        episode_time_s=10,
        reset_time_s=5,
        num_episodes=50,
        video=True,
        run_compute_stats=True,
        push_to_hub=True,
        tags=None,
        num_image_writer_processes=0,
        num_image_writer_threads_per_camera=4,
        force_override=False,
        display_cameras=True,
        play_sounds=True,
    ):
        policy = None
        device = None
        use_amp = None

        # Load pretrained policy
        if pretrained_policy_name_or_path is not None:
            policy, policy_fps, device, use_amp = init_policy(
                pretrained_policy_name_or_path, policy_overrides
            )

            if fps is None:
                fps = policy_fps
                logging.warning(
                    f"No fps provided, so using the fps from policy config ({policy_fps})."
                )
            elif fps != policy_fps:
                logging.warning(
                    f"There is a mismatch between the provided fps ({fps}) and the one from policy config ({policy_fps})."
                )

        # Create empty dataset or load existing saved episodes
        sanity_check_dataset_name(repo_id, policy)
        dataset = init_dataset(
            repo_id,
            root,
            force_override,
            fps,
            video,
            write_images=robot.has_camera,
            num_image_writer_processes=num_image_writer_processes,
            num_image_writer_threads=num_image_writer_threads_per_camera
            * robot.num_cameras,
        )

        if not robot.is_connected:
            robot.connect()

        # Execute a few seconds without recording to:
        # 1. teleoperate the robot to move it in starting position if no policy provided,
        # 2. give times to the robot devices to connect and start synchronizing,
        # 3. place the cameras windows on screen
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

        while True:
            if dataset["num_episodes"] >= num_episodes:
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

            # Execute a few seconds without recording to give time to manually reset the environment
            # Current code logic doesn't allow to teleoperate during this time.
            # TODO(rcadene): add an option to enable teleoperation during reset
            # Skip reset for the last episode to be recorded
            if not self.events["stop_recording"] and (
                (episode_index < num_episodes - 1) or self.events["rerecord_episode"]
            ):
                log_say("Reset the environment", play_sounds)
                reset_environment(robot, self.events, reset_time_s)

            if self.events["rerecord_episode"]:
                log_say("Re-record episode", play_sounds)
                self.events["rerecord_episode"] = False
                self.events["exit_early"] = False
                delete_current_episode(dataset)
                continue

            # Increment by one dataset["current_episode_index"]
            save_current_episode(dataset)

            if self.events["stop_recording"]:
                break

        log_say("Stop recording", play_sounds, blocking=True)
        stop_recording(robot=robot, display_cameras=display_cameras, listener=None)

        lerobot_dataset = create_lerobot_dataset(
            dataset, run_compute_stats, push_to_hub, tags, play_sounds
        )

        log_say("Exiting", play_sounds)
        return lerobot_dataset


def main():

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.showFullScreen()
    # window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
