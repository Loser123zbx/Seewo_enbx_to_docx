#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import wx
import os
import sys
from main_frame import main as MainFrameClass
from read_xml import extract_enbx


class AppController:
        def __init__(self):
                self.app = wx.App(False)
                self.frame = MainFrameClass(None)
                self.frame.SetTitle("enbx_to_docx 转换器")
                self.frame.SetSize((1200, 750))

                # 统一主题设置（颜色与字体）
                try:
                        self.frame.SetTransparent(225)
                except Exception:
                        pass
                # 主题色与背景
                primary_bg = wx.Colour("#464646")
                accent = wx.Colour("#FFC935")
                self.frame.SetBackgroundColour(primary_bg)
                default_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
                self.frame.SetFont(default_font)
                # 按钮风格
                try:
                        self.frame.preview.SetBackgroundColour(accent)
                        self.frame.preview.SetForegroundColour(wx.Colour(0,0,0))
                        self.frame.output.SetBackgroundColour(accent)
                        self.frame.output.SetForegroundColour(wx.Colour(0,0,0))
                except Exception:
                        pass
                self.frame.preview.SetToolTip("预览已选文件的版面")
                self.frame.output.SetToolTip("打开导出设置并导出选中版面")

                # 事件绑定
                self.frame.m_filePicker1.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_selected)
                self.frame.preview.Bind(wx.EVT_BUTTON, self.on_preview)
                self.frame.output.Bind(wx.EVT_BUTTON, self.on_open_output)

                self.output_window = None

                # 初始化显示欢迎页面
                self._show_welcome_page()

        def _show_welcome_page(self):
                """在 Notebook 中显示欢迎页面"""
                notebook = self.frame.m_notebook1
                notebook.SetBackgroundColour(wx.Colour("#2C2C2C"))
                # 确保清空现有页面（如果有）
                while notebook.GetPageCount() > 0:
                        notebook.DeletePage(0)

                # 创建欢迎面板
                welcome_panel = wx.Panel(notebook)
                welcome_panel.SetBackgroundColour("#FFC863")

                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.AddStretchSpacer(1)  # 顶部弹簧

                # 加粗标题 "欢迎使用enbx_to_docx"
                title_text = wx.StaticText(welcome_panel, label="| 欢迎使用.enbx to .docx |")
                try:
                        title_font = wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "微软雅黑")
                except:
                        # 如果指定面名失败，回退到默认字体
                        title_font = wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
                title_text.SetFont(title_font)
                title_text.SetForegroundColour("#000000")  # 使用强调色
                sizer.Add(title_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

                # 加载图片 "welcome.png"
                img_path = None
                # 尝试多个可能的路径
                possible_paths = [
                        os.path.join(os.path.dirname(__file__), 'welcome.png'),
                        os.path.join(os.path.dirname(__file__), 'src', 'welcome.png'),
                        'src/welcome.png',
                        'welcome.png'
                ]

                for p in possible_paths:
                        if os.path.exists(p):
                                img_path = p
                                break

                if img_path:
                        try:
                                img = wx.Image(img_path, wx.BITMAP_TYPE_ANY)
                                # 限制图片最大宽度，防止过大
                                max_width = 1200
                                if img.GetWidth() > max_width:
                                        scale = max_width / float(img.GetWidth())
                                        new_height = int(img.GetHeight() * scale)
                                        img = img.Scale(max_width, new_height, wx.IMAGE_QUALITY_HIGH)

                                bitmap = wx.Bitmap(img)
                                img_ctrl = wx.StaticBitmap(welcome_panel, bitmap=bitmap)
                                sizer.Add(img_ctrl, 0, wx.ALIGN_CENTER | wx.ALL, 10)
                        except Exception as e:
                                print(f"加载图片失败: {e}")
                                error_text = wx.StaticText(welcome_panel, label="(图片加载失败)")
                                error_text.SetForegroundColour(wx.Colour(200, 40, 40))
                                sizer.Add(error_text, 0, wx.ALIGN_CENTER)
                else:
                        # 如果找不到图片，显示提示文本
                        no_img_text = wx.StaticText(welcome_panel, label="(未找到 welcome.png 图片)")
                        no_img_text.SetForegroundColour(wx.Colour(100, 100, 100))
                        sizer.Add(no_img_text, 0, wx.ALIGN_CENTER)

                # 添加底部说明文本
                hint_label = wx.StaticText(welcome_panel, label="请选择 .enbx 文件开始转换")
                hint_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
                hint_label.SetFont(hint_font)
                hint_label.SetForegroundColour(wx.Colour(100, 100, 100))
                sizer.Add(hint_label, 0, wx.ALIGN_CENTER | wx.TOP, 20)

                sizer.AddStretchSpacer(1)  # 底部弹簧

                welcome_panel.SetSizer(sizer)

                # 将欢迎面板添加到 Notebook，标签设为“欢迎”
                notebook.AddPage(welcome_panel, "欢迎")

        def run(self):
                self.frame.Show()
                self.app.MainLoop()

        def on_file_selected(self, event):
                path = event.GetPath()
                if not path:
                        return
                # 解压到 src/tmp 目录下 (保持原有逻辑，解压位置由 read_xml 决定)
                try:
                        extract_enbx(path)
                        wx.MessageBox("已解压文件到 ./tmp/ (如有)", "完成", wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                        wx.MessageBox(f"解压失败: {e}", "错误", wx.OK | wx.ICON_ERROR)

        def on_preview(self, event):
                # 读取 tmp/Slides, 将每个 xml 名称加入 notebook 作为标签，显示基本文本预览
                # 修改为相对路径 ../tmp/Slides
                slides_dir = "tmp/Slides"
                
                if not os.path.isdir(slides_dir):
                        wx.MessageBox("未找到 tmp/Slides 目录，请先选择 enbx 并解压。", "提示", wx.OK | wx.ICON_INFORMATION)
                        return

                # 清空当前 notebook
                notebook = self.frame.m_notebook1
                # 删除所有页
                while notebook.GetPageCount() > 0:
                        notebook.DeletePage(0)

                files = sorted([f for f in os.listdir(slides_dir) if f.lower().endswith('.xml')])

                if not files:
                        self._show_welcome_page()
                        wx.MessageBox("未在解压目录中找到幻灯片 XML 文件。", "提示", wx.OK | wx.ICON_INFORMATION)
                        return

                # 缩略图目录 - 同样修改为相对路径
                thumbs_dir = os.path.join(os.path.dirname(__file__), '..', 'tmp', 'SlideThumbnails')
                thumbs_dir = os.path.normpath(thumbs_dir)
                
                img_exts = ['.png', '.jpg', '.jpeg', '.bmp']

                for f in files:
                        panel = wx.Panel(notebook)
                        panel.SetBackgroundColour(wx.Colour(245, 248, 250))
                        sizer = wx.BoxSizer(wx.VERTICAL)
                        lbl = wx.StaticText(panel, label=f)
                        lbl.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                        sizer.Add(lbl, 0, wx.ALL, 6)

                        # 查找对应缩略图
                        base = os.path.splitext(f)[0]
                        thumb_path = None
                        if os.path.isdir(thumbs_dir):
                                for ext in img_exts:
                                        candidate = os.path.join(thumbs_dir, base + ext)
                                        if os.path.exists(candidate):
                                                thumb_path = candidate
                                                break

                        if thumb_path:
                                # 加载并按比例缩放以适配区域
                                img = wx.Image(thumb_path)
                                max_w, max_h = 780, 420
                                w, h = img.GetWidth(), img.GetHeight()
                                scale = min(max_w / max(1, w), max_h / max(1, h), 1.0)
                                new_w = int(w * scale)
                                new_h = int(h * scale)
                                if scale < 1.0:
                                        img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
                                bmp = wx.Bitmap(img)
                                bitmap = wx.StaticBitmap(panel, bitmap=bmp)
                                # 添加边距与光影效果（简单模拟）
                                sizer.Add(bitmap, 1, wx.ALL | wx.CENTER, 8)
                        else:
                                # 尝试按原解析渲染文本布局
                                xml_path = os.path.join(slides_dir, f)
                                try:
                                        from read_xml import read_xml_to_sentence
                                        structured = read_xml_to_sentence(xml_path)
                                except Exception:
                                        structured = None

                                if structured:
                                        txt = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
                                        parts = []
                                        for ti, textbox in enumerate(structured):
                                                parts.append(f"--- 文本框 {ti+1} ---")
                                                for lj, line in enumerate(textbox):
                                                        line_text = ''.join([run.text for run in line if run.text])
                                                        parts.append(line_text)
                                                parts.append('')
                                        txt.SetValue('\n'.join(parts))
                                        sizer.Add(txt, 1, wx.EXPAND | wx.ALL, 6)
                                else:
                                        note = wx.StaticText(panel, label=u"(未找到缩略图，且无法解析 XML)")
                                        note.SetForegroundColour(wx.Colour(200, 40, 40))
                                        sizer.Add(note, 0, wx.ALL, 6)

                        panel.SetSizer(sizer)
                        notebook.AddPage(panel, f)

        def on_open_output(self, event):
                import output

                if self.output_window and self.output_window.IsShown():
                        self.output_window.Raise()
                        return
                self.output_window = output.output(self.frame)
                self.output_window.SetTitle("enbx_to_docx - 导出设置")
                




                # 填充 slides 列表 - 修改为相对路径
                slides_dir = "../tmp/Slides/"
                
                try:
                        self.output_window.populate_slides(slides_dir)
                        
                        # 更加优雅的外观：半透明
                        try:
                                self.output_window.SetTransparent(240)
                        except Exception:
                                pass
                        
                        self.output_window.Show()
                        self.output_window.Raise()  # 将窗口置于前端
                        self.output_window.Bind(wx.EVT_CLOSE, self.on_output_close)

                except RuntimeError:
                        # 如果在操作过程中窗口被销毁，重置引用并提示
                        self.output_window = None
                        wx.MessageBox("导出窗口意外关闭，请重试。", "错误", wx.OK | wx.ICON_ERROR)
        def on_output_close(self, event):
                """处理导出窗口关闭事件，防止主程序退出"""
                if self.output_window:
                        self.output_window.Destroy()
                        self.output_window = None
                # 必须调用 Skip，否则窗口可能无法正常关闭或行为异常
                event.Skip()


if __name__ == '__main__':
        # 将当前路径加入 sys.path，确保模块能被导入
        basedir = os.path.dirname(__file__)
        if basedir not in sys.path:
                sys.path.insert(0, basedir)

        controller = AppController()
        controller.run()