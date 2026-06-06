# -*- coding: utf-8 -*-
from typing import List, Optional
import sys
import io
if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
def extract_enbx(path):
        """解压 enbx 文件"""
        import zipfile
        
        # 传入压缩文件zfile.zip获取相关信息
        try:
                with zipfile.ZipFile(path, 'r') as zip_file:
                        zip_info = zip_file.infolist()
                        for info in zip_info:
                                try:
                                        # 注意：直接解压到当前目录可能会覆盖文件，建议指定提取路径
                                        zip_file.extract(info.filename, path='tmp/')                        
                                        print(f"Filename: {info.filename}")
                                        print(f"File size: {info.file_size} bytes")
                                        print(f"File date: {info.date_time}")

                                except zipfile.BadZipFile:
                                        print("BadZipFile")
                                        continue

                                except zipfile.ReadError:
                                        print("ReadError")
                                        continue

                                except PermissionError:
                                        print("PermissionError")
                                        continue
        except Exception as e:
                print(f"Error opening zip file: {e}")

# 定义数据类用于存储最小文本单元
try:
        from dataclasses import dataclass

        @dataclass
        class TextRunData:
                """存储单个 TextRun 的最小单元数据"""
                text: str
                font_size: float = 0.0
                font_family: str = ""
                is_bold: bool = False
                is_italic: bool = False
                foreground_color: str = "#FF000000"  # 默认黑色
                background_color: str = "#00FFFFFF"  # 默认透明

                def __repr__(self):
                        return f"TextRun('{self.text}', bold={self.is_bold}, color={self.foreground_color})"
except ImportError:
        # 如果 Python 版本过低不支持 dataclasses，可以回退到普通类或使用字典
        class TextRunData:
                def __init__(self, text, font_size=0.0, font_family="", is_bold=False, is_italic=False, foreground_color="#FF000000", background_color="#00FFFFFF"):
                        self.text = text
                        self.font_size = font_size
                        self.font_family = font_family
                        self.is_bold = is_bold
                        self.is_italic = is_italic
                        self.foreground_color = foreground_color
                        self.background_color = background_color

                def __repr__(self):
                        return f"TextRun('{self.text}', bold={self.is_bold}, color={self.foreground_color})"

def _parse_hex_color(element) -> str:
        """辅助函数：从 ColorBrush 标签中提取颜色值"""
        if element is None:
                return "#FF000000"
        color_brush = element.find('ColorBrush')
        if color_brush is not None and color_brush.text:
                return color_brush.text.strip()
        return "#FF000000"

def _parse_text_run(run_element) -> TextRunData:
        """解析单个 <TextRun> 节点"""
        import xml.etree.ElementTree as ET
        
        # 获取文本内容，处理可能的换行符实体 &#xD;
        text_elem = run_element.find('Text')
        text_content = text_elem.text.split('&#xD;')[0]
        text_content = text_elem.text.split('\r\n')[0]

        
        # 获取字体大小
        font_size_elem = run_element.find('FontSize')
        font_size = float(font_size_elem.text) if font_size_elem is not None and font_size_elem.text else 0.0

        # 获取字体家族
        font_family_elem = run_element.find('FontFamily/Source')
        font_family = font_family_elem.text if font_family_elem is not None and font_family_elem.text else ""

        # 获取样式
        weight_elem = run_element.find('FontWeight')
        is_bold = weight_elem.text == 'Bold' if weight_elem is not None else False
        
        style_elem = run_element.find('FontStyle')
        is_italic = style_elem.text == 'Italic' if style_elem is not None else False

        # 获取前景色 (文字颜色)
        fg_color = _parse_hex_color(run_element.find('Foreground'))
        
        # 获取背景色
        bg_color = _parse_hex_color(run_element.find('Background'))

        return TextRunData(
                text=text_content,
                font_size=font_size,
                font_family=font_family,
                is_bold=is_bold,
                is_italic=is_italic,
                foreground_color=fg_color,
                background_color=bg_color
        )

def read_xml_to_sentence(path):
        """
        解析 Slide XML 文件
        返回结构: [ TextBox1 [ Line1 [ Run1, Run2 ], Line2 [ Run3 ] ], TextBox2 [ ... ] ]
        """
        import xml.etree.ElementTree as ET
        
        try:
                tree = ET.parse(path)
                root = tree.getroot()
                
                slide_content = []
                
                # 查找所有的 <Text> 元素 (即文本框)
                # .//Text 表示递归查找所有层级的 Text 标签
                text_boxes = root.findall('.//Text')
                
                for tb in text_boxes:
                        rich_text = tb.find('RichText')
                        if rich_text is None:
                                continue
                                
                        text_lines = rich_text.find('TextLines')
                        if text_lines is None:
                                continue
                                
                        current_textbox_lines = []
                        
                        # 遍历每一行 <TextLine>
                        for line in text_lines.findall('TextLine'):
                                current_line_runs = []
                                
                                # 遍历行内的每一个 <TextRun>
                                runs = line.findall('TextRuns/TextRun')
                                for run in runs:
                                        run_data = _parse_text_run(run)
                                        # 只有当文本不为空或者我们想保留格式占位时才添加
                                        # 这里我们保留所有 Run，包括纯换行或空格，以保持结构完整
                                        current_line_runs.append(run_data)
                                
                                current_textbox_lines.append(current_line_runs)
                                
                        slide_content.append(current_textbox_lines)
                        
                return slide_content

        except Exception as e:
                print(f"Error parsing XML: {e}")
                return []

if __name__ == '__main__':
        #测试解压
        print(extract_enbx('D:\\123_softs\\enbx_to_docx\\英才班知识点落实.enbx'))
        
        #测试 XML 解析
        xml_path = 'D:\\123_softs\\enbx_to_docx\\src\\core\\tmp\\Slides\\Slide_47.xml'
        structured_data = read_xml_to_sentence(xml_path)
        
        if structured_data:
                print(f"共找到 {len(structured_data)} 个文本框")
                for i, textbox in enumerate(structured_data):
                        print(f"\n--- 文本框 {i+1} ---")
                        for j, line in enumerate(textbox):
                                # 将一行中的所有 Run 拼接起来查看纯文本效果
                                line_text = "".join([run.text for run in line])
                                print(f"  行 {j+1}: {repr(line_text)}")
        else:
                print("未解析到数据或文件路径错误")