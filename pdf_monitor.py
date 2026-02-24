#!/usr/bin/env python3
"""
PDF转Word自动监控工具
监控指定目录，当有PDF文件被放入时，自动将其转换为Word文档
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    from pdf2docx import Converter
except ImportError as e:
    print(f"Error: Missing dependency. Please run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('pdf_monitor.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class PDFHandler(FileSystemEventHandler):
    """处理PDF文件事件的处理器"""
    
    def __init__(self, watch_dir: str, output_dir: Optional[str] = None, 
                 delete_original: bool = False, max_workers: int = 4):
        """
        初始化PDF处理器
        
        Args:
            watch_dir: 监控的目录
            output_dir: Word文档输出目录（如果为None，则输出到原目录）
            delete_original: 转换成功后是否删除原始PDF文件
            max_workers: 并发转换的最大线程数
        """
        self.watch_dir = Path(watch_dir)
        self.output_dir = Path(output_dir) if output_dir else self.watch_dir
        self.delete_original = delete_original
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"PDF监控器已初始化 (线程池大小: {max_workers})")
        logger.info(f"监控目录: {self.watch_dir.absolute()}")
        logger.info(f"输出目录: {self.output_dir.absolute()}")
    
    def on_created(self, event):
        """当文件被创建时触发"""
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix.lower() == '.pdf':
                logger.info(f"检测到新的PDF文件: {file_path.name}")
                # 提交到线程池异步处理
                self.executor.submit(self._delayed_convert, file_path)

    def _delayed_convert(self, pdf_path: Path):
        """延迟转换以确保文件完全写入"""
        # 等待文件完全写入（特别是大文件）
        time.sleep(2)
        self.convert_pdf_to_word(pdf_path)
    
    def convert_pdf_to_word(self, pdf_path: Path):
        """
        将PDF转换为Word文档
        
        Args:
            pdf_path: PDF文件路径
        """
        if not pdf_path.exists():
            return

        # 生成输出文件名（保持相同文件名，扩展名改为.docx）
        word_filename = pdf_path.stem + '.docx'
        word_path = self.output_dir / word_filename
        
        # 如果目标文件已存在，添加时间戳
        if word_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            word_filename = f"{pdf_path.stem}_{timestamp}.docx"
            word_path = self.output_dir / word_filename
        
        logger.info(f"正在转换: {pdf_path.name} -> {word_path.name}")
        
        start_time = time.time()
        try:
            # 转换PDF到Word
            cv = Converter(str(pdf_path))
            cv.convert(str(word_path), start=0, end=None)
            cv.close()
            
            elapsed_time = time.time() - start_time
            logger.info(f"转换成功: {word_path.name} (耗时: {elapsed_time:.2f}s)")
            
            # 检查文件大小，确保转换成功
            if word_path.exists() and word_path.stat().st_size > 0:
                # 如果需要，删除原始PDF文件
                if self.delete_original:
                    try:
                        pdf_path.unlink()
                        logger.info(f"已清理原始文件: {pdf_path.name}")
                    except Exception as e:
                        logger.error(f"无法清理原始文件: {e}")
            else:
                logger.warning(f"警告: 生成的文件可能损坏: {word_path.name}")
                
        except Exception as e:
            logger.error(f"转换失败: {pdf_path.name} | 错误信息: {str(e)}")
            
            # 清理可能创建的不完整文件
            if word_path.exists():
                try:
                    word_path.unlink()
                except:
                    pass


def setup_argument_parser():
    """设置命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='监控目录并自动将PDF转换为Word文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python pdf_monitor.py                           # 监控当前目录
  python pdf_monitor.py -d D:\\pdfs               # 监控指定目录
  python pdf_monitor.py -d D:\\pdfs -o D:\\docs    # 指定输出目录
  python pdf_monitor.py --delete                  # 转换后删除原始PDF
  python pdf_monitor.py --daemon                  # 后台运行模式
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help='要监控的目录路径（默认：当前目录）'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Word文档输出目录（默认：与输入目录相同）'
    )
    
    parser.add_argument(
        '--delete',
        action='store_true',
        help='转换成功后删除原始PDF文件'
    )
    
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='后台运行模式（持续监控）'
    )
    
    parser.add_argument(
        '--single',
        action='store_true',
        help='单次处理模式（处理当前目录现有PDF后退出）'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='并发转换的最大线程数（默认：4）'
    )
    
    return parser


def convert_existing_pdfs(directory: str, output_dir: Optional[str], 
                          delete_original: bool = False, max_workers: int = 4):
    """转换目录中已存在的所有PDF文件"""
    dir_path = Path(directory)
    output_path = Path(output_dir) if output_dir else dir_path
    
    # 确保输出目录存在
    output_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"正在扫描目录中的现有PDF文件: {dir_path.absolute()}")
    
    pdf_files = list(dir_path.glob("*.pdf")) + list(dir_path.glob("*.PDF"))
    
    if not pdf_files:
        logger.info("未找到待处理的PDF文件")
        return
    
    logger.info(f"找到 {len(pdf_files)} 个PDF文件，开始批量处理...")
    
    # 初始化处理器用于转换
    handler = PDFHandler(str(dir_path), str(output_path), delete_original, max_workers)
    
    # 使用线程池并发处理现有文件
    for pdf_file in pdf_files:
        handler.executor.submit(handler.convert_pdf_to_word, pdf_file)
    
    # 等待所有任务完成
    handler.executor.shutdown(wait=True)
    logger.info("现有文件批量处理完成")


def main():
    """主函数"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # 打印欢迎信息
    print("=" * 60)
    print("PDF转Word自动监控工具 (Professional Version)")
    print("=" * 60)
    print(f"监控目录: {Path(args.directory).absolute()}")
    if args.output:
        print(f"输出目录: {Path(args.output).absolute()}")
    print(f"并发线程: {args.workers}")
    print(f"清理原件: {args.delete}")
    print("按 Ctrl+C 停止监控")
    print("=" * 60)
    
    # 检查目录是否存在
    watch_dir = Path(args.directory)
    if not watch_dir.exists():
        print(f"错误: 目录不存在 - {watch_dir.absolute()}")
        sys.exit(1)
    
    # 如果指定了单次模式，处理现有文件后退出
    if args.single:
        convert_existing_pdfs(args.directory, args.output, args.delete, args.workers)
        print("单次处理完成，程序退出")
        sys.exit(0)
    
    # 处理现有PDF文件（在开始监控之前）
    convert_existing_pdfs(args.directory, args.output, args.delete, args.workers)
    
    # 设置监控器
    event_handler = PDFHandler(args.directory, args.output, args.delete, args.workers)
    observer = Observer()
    observer.schedule(event_handler, args.directory, recursive=False)
    
    try:
        # 启动监控
        observer.start()
        logger.info(f"开始监控目录: {watch_dir.absolute()}")
        print(f"监控已启动，正在监控 {watch_dir.absolute()}")
        print("请将PDF文件放入上述目录，系统将自动转换为Word文档")
        print("日志文件: pdf_monitor.log")
        
        # 持续运行（除非在非后台模式下）
        if args.daemon:
            # 后台模式，无限循环
            while True:
                time.sleep(1)
        else:
            # 前台模式，等待用户中断
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n正在停止监控...")
                
    except Exception as e:
        logger.error(f"监控器运行时出错: {e}")
        print(f"错误: {e}")
    finally:
        observer.stop()
        observer.join()
        logger.info("监控器已停止")
        print("监控已停止")


if __name__ == "__main__":
    main()