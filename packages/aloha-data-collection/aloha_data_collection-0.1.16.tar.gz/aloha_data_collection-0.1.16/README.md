
# **ALOHA Data Collection**

![Placeholder for Project Image](#)

---

## **Overview**

ALOHA Data Collection is a Python-based application designed for seamless and efficient robotic data collection. It provides an intuitive GUI to manage robot configurations, perform task recordings, and streamline data collection with advanced features like camera views, task management, and progress tracking.

---

## **Pre-Installation Setup**

Before installing the application, complete the following setup:

1. **Install Miniconda:**
   Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for your operating system.

2. **Create a Virtual Environment:**
   Use Miniconda to create a virtual environment:
   ```bash
   conda create -n aloha_env python=3.10 -y
   conda activate aloha_env
   ```

---

## **Installation**

Install ALOHA Data Collection directly using `pip`:

```bash
pip install aloha_data_collection
```

---

## **Post-Installation**

After installation, run the command to setup the following:
- Clones and installs required dependencies for `lerobot`.
- Resolves common issues with OpenCV and video encoding.
- Creates a desktop icon for launching the application.

```bash
post_install
```

---

## **Launching the Application**

### **Desktop Application**

After installation, a desktop shortcut named **ALOHA Data Collection** is available. Click on it to launch the application.

### **Command Line**

Alternatively, you can run the application directly from the terminal:

```bash
aloha_data_collection
```

---

## **Application Features**

### **1. Task Management**
- **Task Names:** Select predefined tasks from the dropdown menu.
- **Episodes:** Specify the number of episodes using the spin box. Adjust the count using the `+` and `-` buttons.

### **2. Recording Controls**
- **Start Recording:** Initiates data collection for the selected task.
- **Stop Recording:** Stops the current data collection session.
- **Re-Record:** Allows re-recording of the current episode if necessary.

### **3. Progress Tracking**
- A progress bar tracks the recording session in real-time, displaying completion percentage.

### **4. Camera Views**
- View multiple camera feeds in real-time during recording for better monitoring.

### **5. Configuration Management**
- **Edit Robot Configuration:** Modify the robot's YAML configuration for granular control.
- **Edit Task Configuration:** Adjust task-specific parameters via a YAML editor.

### **6. Quit Button**
- Use the Quit button in the menu to gracefully exit the application.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
