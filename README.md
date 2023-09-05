# System Monitoring Tool

This README provides instructions on how to set up and run the System Monitor project, a graphical user interface (GUI) tool developed using Python's Tkinter library. The System Monitor offers various functionalities for monitoring your system's performance, including CPU and Memory statistics, Disk I/O, Network I/O, Process management, and Keyboard monitoring.

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the System Monitor](#running-the-system-monitor)
  - [Tabs Overview](#tabs-overview)
- [Customization](#customization)
- [Additional Features](#additional-features)
- [Keyboard Monitoring](#keyboard-monitoring)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following requirements met:

1. **Python**: Make sure you have Python installed on your machine. You can download it from [Python's official website](https://www.python.org/downloads/).

### Installation

Follow these steps to set up the System Monitor project:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/vikas-mshra/Linux-Task-Manager.git
   ```

2. Navigate to the project directory in your terminal:

   ```bash
   cd Linux-Task-Manager
   ```

3. Switch to the root user. You may need administrative privileges to monitor system performance and processes:

   ```bash
   sudo su
   ```
4. Install the required Python packages if not already installed:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the System Monitor

To run the System Monitor, follow these steps:

1. Open a terminal and navigate to the project directory:

   ```bash
   cd /path/to/Linux-Task-Manager
   ```

2. Ensure you are in the root user mode:

   ```bash
   sudo su
   ```

3. Execute the following command to start the System Monitor:

   ```bash
   python3 index.py
   ```

### Tabs Overview

The System Monitor provides the following tabs for monitoring your system:

- **System Performance**: Displays CPU and Memory statistics.

- **Disk I/O**: Shows disk performance metrics.

- **Network I/O**: Lists all TCP and UDP connections, along with program names, port numbers, usernames, and more.

- **Processes**: Provides a list of all running processes in the system. You can search among them.

- **Keyboard Monitor**: Monitors user keypresses. To enable it, follow the instructions [here](https://github.com/vikas-mshra/keyboard-logger#readme).

## Customization

You can customize the System Monitor in the following ways:

1. **Interval Time**: Modify the interval time to track processes and statistics more frequently. You can adjust this in the UI itself.

2. **Search Functionality**: Use the search feature in the Network I/O and Processes tabs to quickly find specific programs or processes.

3. **Task Manager**: Utilize the task manager to track the keys pressed by the user.

## Additional Features

- The System Monitor allows you to monitor and manage your system's performance conveniently.

- You can easily switch between different tabs to access specific information.

- Customize the refresh rate and search for processes or programs.

## Keyboard Monitoring

To enable keyboard monitoring, please follow the instructions provided [here](https://github.com/vikas-mshra/keyboard-logger#readme).

---

Feel free to explore and use the System Monitor to keep an eye on your system's performance. If you encounter any issues or have suggestions for improvement, please don't hesitate to open an issue or submit a pull request. Enjoy monitoring your system!