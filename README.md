# PDF-to-Word 自动监控器（专业版） 
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/) [![许可证: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Watchdog](https://img.shields.io/badge/library-watchdog-orange)](https://pypi.org/project/watchdog/) [![pdf2docx](https://img.shields.io/badge/library-pdf2docx-green)](https://pypi.org/project/pdf2docx/)

一个高性能的 Python 工具，用于监控目录中的新 PDF 文件，并使用多线程处理自动将其转换为可编辑的 Word 文档（`.docx`）。

## 主要功能

- **实时监控**：利用 `watchdog` 通过操作系统级事件即时检测新文件。
- **多线程处理**：使用 `ThreadPoolExecutor` 并发处理多个转换任务，显著提高批量作业的吞吐量。
- **智能文件处理**：
  - 自动延迟，确保文件在写入完成后才进行处理。
  - 重复文件名保护，自动添加时间戳。
  - 转换成功后可选删除原始文件。
- **强大的日志记录**：全面的日志系统，用于审计和故障排除。
- **专业的命令行界面**：丰富的命令行界面，支持守护进程模式、单次运行模式和可配置的并发数。

## ️ 技术栈

- **Python 3**：核心逻辑。
- **Watchdog**：事件驱动的文件系统监控。
- **pdf2docx**：高保真 PDF 到 DOCX 转换引擎。
- **Concurrent.futures**：多线程性能优化。

## 安装

1. **克隆仓库**：
   ```bash
   git clone https://github.com/yourusername/pdf-to-word-monitor.git
   cd pdf-to-word-monitor
```

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

使用指南

快速开始（推荐）

双击 Start_Monitor.bat 启动工具。将您的 PDF 文件拖放到文件夹中，它们将自动转换！

手动使用（命令行）

```bash
# 监控当前目录
python pdf_monitor.py

# 监控指定目录
python pdf_monitor.py -d "C:/Users/Desktop/MyPDFs"
```

高级选项

```bash
# 使用 8 个线程运行，并在转换后删除原始 PDF 文件
python pdf_monitor.py --workers 8 --delete --daemon
```

参数 缩写 描述 默认值
--directory -d 监控路径 .
--output -o 输出目录 与输入目录相同
--workers  最大并发线程数 4
--delete  转换后删除 PDF False
--daemon  在后台持续运行 False
--single  处理现有文件后退出 False

日志记录

所有操作记录到 pdf_monitor.log。您可以实时监控进度：

```bash
tail -f pdf_monitor.log   # Linux/macOS
Get-Content pdf_monitor.log -Wait   # Windows PowerShell
```

⚖️ 许可证

根据 MIT 许可证分发。更多信息请参见 LICENSE。

为提高效率和自动化而生。 
由 yml582484-collab 用 ❤️ 制作

```