# PDF 转 Word 自动监控工具 (专业版)
Python 3.6+

License: MIT

Watchdog

pdf2docx
这是一个基于 Python 的高性能实用工具，用于监控指定目录中的新 PDF 文件，并利用多线程处理技术自动将其转换为可编辑的 Word 文档 (.docx)。
## 🚀 核心特性
 * **实时监控**：利用 watchdog 借助操作系统级事件即时检测新文件。
 * **多线程处理**：使用 ThreadPoolExecutor 并发执行多个转换任务，显著提升批处理任务的吞吐量。
 * **智能文件处理**：
   * 自动延迟读取，确保文件在处理前已完全写入硬盘。
   * 重复文件名保护机制，自动为重名文件添加时间戳。
   * 支持转换成功后自动清理（删除）原始文件的选项。
 * **可靠的日志记录**：拥有全面的日志记录系统，方便进行任务审计和故障排除。
 * **专业的命令行接口 (CLI)**：功能丰富的命令行支持，包含守护进程模式、单次运行模式以及可自定义的并发线程数。
## 🛠️ 技术栈
 * **Python 3**：核心业务逻辑。
 * **Watchdog**：事件驱动的文件系统监控。
 * **pdf2docx**：高保真的 PDF 到 DOCX 转换引擎。
 * **Concurrent.futures**：多线程并发处理，优化性能。
## 📋 安装说明
 1. **克隆仓库**：
   ```bash
   git clone https://github.com/yourusername/pdf-to-word-monitor.git
   cd pdf-to-word-monitor
   
   ```
 2. **安装依赖包**：
```bash
    pip install -r requirements.txt
    ```

## 📖 使用指南

### 🚀 快速启动 (推荐)
双击 **`Start_Monitor.bat`** 即可启动该工具。
只需将您的 PDF 文件拖放到监控文件夹中，它们就会被自动转换！

### 手动运行 (命令行模式)
```bash
# 监控当前目录
python pdf_monitor.py

# 监控指定目录
python pdf_monitor.py -d "C:/Users/Desktop/MyPDFs"

```
### 高级选项
```bash
# 使用 8 个线程运行，并在转换成功后删除原始 PDF 文件
python pdf_monitor.py --workers 8 --delete --daemon

```
| 参数 | 简写 | 说明 | 默认值 |
|---|---|---|---|
| --directory | -d | 需要监控的路径 | . (当前目录) |
| --output | -o | 输出目录 | 与输入目录相同 |
| --workers |  | 最大并发线程数 | 4 |
| --delete |  | 转换后删除原 PDF 文件 | False |
| --daemon |  | 在后台持续运行 | False |
| --single |  | 处理完现有文件后直接退出 | False |
## 📝 日志记录
所有的运行操作都会被记录到 pdf_monitor.log 文件中。您可以实时监控处理进度：
```bash
tail -f pdf_monitor.log  # Linux/macOS
Get-Content pdf_monitor.log -Wait # Windows PowerShell

```
## ⚖️ 开源协议
本项目基于 MIT 协议分发。更多信息请参阅 LICENSE 文件。
*专为提升效率与自动化而开发。*
由 yml582484-collab 用 ❤️ 制作
```

```
