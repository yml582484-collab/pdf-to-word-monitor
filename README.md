# PDF-to-Word Auto Monitor (Professional)

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Watchdog](https://img.shields.io/badge/library-watchdog-orange)](https://pypi.org/project/watchdog/)
[![pdf2docx](https://img.shields.io/badge/library-pdf2docx-green)](https://pypi.org/project/pdf2docx/)

A high-performance Python-based utility that monitors a directory for new PDF files and automatically converts them into editable Word documents (`.docx`) using multi-threaded processing.

## 🚀 Key Features

-   **Real-time Monitoring**: Leverages `watchdog` to detect new files instantly via OS-level events.
-   **Multi-threaded Processing**: Uses `ThreadPoolExecutor` to handle multiple conversions concurrently, significantly improving throughput for batch jobs.
-   **Intelligent File Handling**:
    -   Automatic delay to ensure files are fully written before processing.
    -   Duplicate filename protection with automatic timestamping.
    -   Optional original file cleanup after successful conversion.
-   **Robust Logging**: Comprehensive logging system for auditing and troubleshooting.
-   **Professional CLI**: Rich command-line interface with support for daemon mode, single-run mode, and configurable concurrency.

## 🛠️ Tech Stack

-   **Python 3**: Core logic.
-   **Watchdog**: Event-driven file system monitoring.
-   **pdf2docx**: High-fidelity PDF to DOCX conversion engine.
-   **Concurrent.futures**: Multi-threading for performance optimization.

## 📋 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/pdf-to-word-monitor.git
    cd pdf-to-word-monitor
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 📖 Usage Guide

### Basic Usage (Monitor current directory)
```bash
python pdf_monitor.py
```

### Monitor Specific Directory
```bash
python pdf_monitor.py -d "C:/Users/Desktop/MyPDFs" -o "C:/Users/Desktop/MyDocs"
```

### Batch Process Existing Files Only
```bash
python pdf_monitor.py --single -d "./input"
```

### Advanced Options
```bash
# Run with 8 threads and delete original PDFs after conversion
python pdf_monitor.py --workers 8 --delete --daemon
```

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `--directory` | `-d` | Path to monitor | `.` |
| `--output` | `-o` | Output directory | Same as input |
| `--workers` | | Max concurrent threads | `4` |
| `--delete` | | Delete PDF after conversion | `False` |
| `--daemon` | | Keep running in background | `False` |
| `--single` | | Process existing files and exit | `False` |

## 📝 Logging

All operations are logged to `pdf_monitor.log`. You can monitor the progress in real-time:
```bash
tail -f pdf_monitor.log  # Linux/macOS
Get-Content pdf_monitor.log -Wait # Windows PowerShell
```

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed for efficiency and automation.*
