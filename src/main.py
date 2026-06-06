#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import wx
import os
import sys
from main_frame import main as MainFrameClass
from output import output as OutputFrameClass
from read_xml import extract_enbx


class AppController:
    def __init__(self):
        self.app = wx.App(False)
        self.frame = MainFrameClass(None)

        # 统一主题设置（颜色与字体）
        try:
            self.frame.SetTransparent(230)
        except Exception:
            pass
        # 主题色与背景
        primary_bg = wx.Colour(250, 252, 254)
        accent = wx.Colour(52, 120, 246)
        self.frame.SetBackgroundColour(primary_bg)
        default_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.frame.SetFont(default_font)
        # 按钮风格
        try:
            self.frame.preview.SetBackgroundColour(accent)
            self.frame.preview.SetForegroundColour(wx.Colour(255,255,255))
            self.frame.output.SetBackgroundColour(accent)
            self.frame.output.SetForegroundColour(wx.Colour(255,255,255))
        except Exception:
            pass
        self.frame.preview.SetToolTip("预览已选文件的版面")
        self.frame.output.SetToolTip("打开导出设置并导出选中版面")

        # 事件绑定
        self.frame.m_filePicker1.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_selected)
        self.frame.preview.Bind(wx.EVT_BUTTON, self.on_preview)
        self.frame.output.Bind(wx.EVT_BUTTON, self.on_open_output)

        self.output_window = None

    def run(self):
        self.frame.Show()
        self.app.MainLoop()

    def on_file_selected(self, event):
        path = event.GetPath()
        if not path:
            return
        # 解压到 src/tmp 目录下
        try:
            extract_enbx(path)
            wx.MessageBox("已解压文件到 ./tmp/ (如有)", "完成", wx.OK|wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"解压失败: {e}", "错误", wx.OK|wx.ICON_ERROR)

    def on_preview(self, event):
        # 读取 tmp/Slides, 将每个 xml 名称加入 notebook 作为标签，显示基本文本预览
        slides_dir = os.path.join(os.path.dirname(__file__), 'tmp', 'Slides')
        if not os.path.isdir(slides_dir):
            wx.MessageBox("未找到 tmp/Slides 目录，请先选择 enbx 并解压。", "提示", wx.OK|wx.ICON_INFORMATION)
            return

        # 清空当前 notebook
        notebook = self.frame.m_notebook1
        # 删除所有页
        while notebook.GetPageCount() > 0:
            notebook.DeletePage(0)

        files = sorted([f for f in os.listdir(slides_dir) if f.lower().endswith('.xml')])
        # 缩略图目录
        thumbs_dir = os.path.join(os.path.dirname(__file__), 'tmp', 'SlideThumbnails')
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
                sizer.Add(bitmap, 1, wx.ALL|wx.CENTER, 8)
            else:
                # 尝试按原解析渲染文本布局
                xml_path = os.path.join(slides_dir, f)
                try:
                    from read_xml import read_xml_to_sentence
                    structured = read_xml_to_sentence(xml_path)
                except Exception:
                    structured = None

                if structured:
                    txt = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
                    parts = []
                    for ti, textbox in enumerate(structured):
                        parts.append(f"--- 文本框 {ti+1} ---")
                        for lj, line in enumerate(textbox):
                            line_text = ''.join([run.text for run in line if run.text])
                            parts.append(line_text)
                        parts.append('')
                    txt.SetValue('\n'.join(parts))
                    sizer.Add(txt, 1, wx.EXPAND|wx.ALL, 6)
                else:
                    note = wx.StaticText(panel, label=u"(未找到缩略图，且无法解析 XML)")
                    note.SetForegroundColour(wx.Colour(200,40,40))
                    sizer.Add(note, 0, wx.ALL, 6)

            panel.SetSizer(sizer)
            notebook.AddPage(panel, f)

    def on_open_output(self, event):
        if self.output_window is None:
            self.output_window = OutputFrameClass(self.frame)
        # 填充 slides 列表
        slides_dir = os.path.join(os.path.dirname(__file__), 'tmp', 'Slides')
        self.output_window.populate_slides(slides_dir)
        # 更加优雅的外观：半透明
        try:
            self.output_window.SetTransparent(240)
        except Exception:
            pass
        self.output_window.Show()


if __name__ == '__main__':
    # 将当前路径加入 sys.path，确保模块能被导入
    basedir = os.path.dirname(__file__)
    if basedir not in sys.path:
        sys.path.insert(0, basedir)

    controller = AppController()
    controller.run()
