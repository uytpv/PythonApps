#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from pathlib import Path
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """Parser HTML để trích xuất text"""
    
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_content = False
    
    def handle_starttag(self, tag, attrs):
        # Bỏ qua nội dung của script và style tags
        if tag in ('script', 'style', 'meta', 'link'):
            self.skip_content = True
    
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip_content = False
        # Thêm newline sau các block tags
        if tag in ('p', 'div', 'br', 'li', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            if self.text and self.text[-1] != '\n':
                self.text.append('\n')
    
    def handle_data(self, data):
        if not self.skip_content:
            text = data.strip()
            if text:
                self.text.append(text)
                self.text.append(' ')
    
    def get_text(self):
        """Trả về text đã trích xuất"""
        result = ''.join(self.text)
        # Làm sạch khoảng trắng thừa
        result = re.sub(r'\n\s*\n', '\n\n', result)  # Loại bỏ dòng trống liên tiếp
        result = re.sub(r' +', ' ', result)  # Loại bỏ khoảng trắng thừa
        result = result.strip()
        return result

def extract_text_from_html(html_file):
    """
    Trích xuất text từ file HTML và lưu vào file txt.
    
    Args:
        html_file (str): Đường dẫn đến file HTML
    """
    # Kiểm tra file có tồn tại không
    html_path = Path(html_file)
    if not html_path.exists():
        print(f"Lỗi: File '{html_file}' không tồn tại")
        sys.exit(1)
    
    if not html_path.suffix.lower() == '.html':
        print(f"Lỗi: File phải có đuôi .html")
        sys.exit(1)
    
    try:
        # Đọc file HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML và trích xuất text
        parser = TextExtractor()
        parser.feed(html_content)
        text = parser.get_text()
        
        # Tạo tên file output
        output_file = html_path.stem + '.txt'
        output_path = html_path.parent / output_file
        
        # Lưu text vào file .txt với encoding UTF-8
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✓ Thành công! Text đã được trích xuất vào: {output_file}")
        
    except UnicodeDecodeError:
        print(f"Lỗi: Không thể đọc file HTML với encoding UTF-8")
        sys.exit(1)
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Cách sử dụng: python main.py <filename.html>")
        print("Ví dụ: python main.py page.html")
        sys.exit(1)
    
    html_file = sys.argv[1]
    extract_text_from_html(html_file)

if __name__ == '__main__':
    main()

