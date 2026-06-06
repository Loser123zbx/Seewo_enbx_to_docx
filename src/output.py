# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------
# Python code generated with wxFormBuilder (version 3.9.0 Jun 14 2020)
# http://www.wxformbuilder.org/
#
# PLEASE DO *NOT* EDIT THIS FILE!
#--------------------------------------------------------------------------

import wx
import wx.xrc

import gettext
_ = gettext.gettext

#--------------------------------------------------------------------------
#  Class output
#---------------------------------------------------------------------------

class output ( wx.Frame ):

	def __init__(self, parent):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,460 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		self.SetBackgroundColour(wx.Colour( 239, 235, 235 ))

		root = wx.BoxSizer(wx.HORIZONTAL)

		self.output_bitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap( u"output_setting.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0)
		root.Add(self.output_bitmap, 0, 0, 5)

		settings = wx.BoxSizer(wx.VERTICAL)

		self.output_text = wx.StaticText(self, wx.ID_ANY, _(u"填充导出选项"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.output_text.Wrap(-1)

		self.output_text.SetFont(wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ))

		settings.Add(self.output_text, 0, wx.ALL, 5)

		self.fontsize = wx.StaticText(self, wx.ID_ANY, _(u"导出字符大小比例(从希沃课件到.docx文档的文字大小比例)"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.fontsize.Wrap(-1)

		settings.Add(self.fontsize, 0, wx.ALL, 5)

		self.font_size_bili = wx.TextCtrl(self, wx.ID_ANY, _(u"0.3"), wx.DefaultPosition, wx.DefaultSize, 0)
		settings.Add(self.font_size_bili, 0, wx.ALL, 5)

		output_settingsChoices = [_(u"使用英汉互译模式导出"), _(u"只导出文本而不导出字符格式"), _(u"导出为同一文件")]
		self.output_settings = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, output_settingsChoices, wx.LB_ALWAYS_SB|wx.LB_EXTENDED|wx.LB_MULTIPLE|wx.LB_NEEDED_SB)
		settings.Add(self.output_settings, 0, wx.ALL|wx.EXPAND, 5)

		self.output = wx.Button(self, wx.ID_ANY, _(u"导出"), wx.DefaultPosition, wx.DefaultSize, 0)
		settings.Add(self.output, 0, wx.ALL, 5)


		root.Add(settings, 1, wx.EXPAND, 5)


		self.SetSizer( root )
		self.Layout()

		self.Centre(wx.BOTH)

	def __del__( self ):
		pass


