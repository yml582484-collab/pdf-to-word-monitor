#!/usr/bin/env python3
"""
创建一个简单的测试PDF文件
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_test_pdf(filename="test.pdf"):
    """创建一个简单的测试PDF文件"""
    # 创建PDF文档
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # 添加标题
    c.setFont("Helvetica", 24)
    c.drawString(100, height - 100, "测试PDF文档")
    
    # 添加内容
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "这是一个用于测试PDF转Word功能的文件。")
    c.drawString(100, height - 180, "创建日期: 2026-02-24")
    c.drawString(100, height - 210, "作者: PDF转Word测试工具")
    
    # 添加一些示例文本
    sample_text = """
    这是一段示例文本，用于测试PDF到Word的转换。
    
    转换工具应该能够：
    1. 正确转换文本内容
    2. 保持基本的格式
    3. 处理中文和英文
    
    这是一个多段落的示例，用于测试段落转换。
    
    测试完成！
    """
    
    text_lines = sample_text.strip().split('\n')
    y_pos = height - 260
    for line in text_lines:
        if line.strip():
            c.drawString(100, y_pos, line.strip())
            y_pos -= 30
    
    # 保存PDF
    c.save()
    print(f"已创建测试PDF文件: {filename}")
    print(f"文件大小: 约1KB")

if __name__ == "__main__":
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "test.pdf"
    create_test_pdf(filename)