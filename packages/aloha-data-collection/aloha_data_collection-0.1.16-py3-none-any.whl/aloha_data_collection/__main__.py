from aloha_data_collection.ui.main_window import (
    MainWindow,
)
from PySide6.QtWidgets import QApplication
import sys


def main() -> None:
    """
    Entry point for the Aloha Data Collection application.

    This function initializes the QApplication, sets the application style,
    creates the main window, and starts the application's event loop.
    """
    app = QApplication(sys.argv)  # Create the application instance.
    app.setStyle("Fusion")  # Set the application style to 'Fusion'.

    window = MainWindow()  # Create the main window instance.
    window.showFullScreen()  # Show the main window in full-screen mode.
    # window.show()  # Uncomment to show the window in a normal mode.

    sys.exit(app.exec())  # Execute the application's event loop and exit cleanly.


if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly.
