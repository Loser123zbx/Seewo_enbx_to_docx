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
#  Class running
#---------------------------------------------------------------------------

class running ( wx.Dialog ):

	def __init__(self, parent):
		import os
		wx.Dialog.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 739,224 ), style = wx.CAPTION|wx.DEFAULT_DIALOG_STYLE)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		root = wx.BoxSizer(wx.HORIZONTAL)
		
		# 加载图片 "progress.png"
		img_path = None
		# 尝试多个可能的路径
		possible_paths = [
			os.path.join(os.path.dirname(__file__), 'progress.png'),
			os.path.join(os.path.dirname(__file__), 'src', 'progress.png'),
			'src/progress.png',
			'progress.png'
		]
		for p in possible_paths:
			if os.path.isfile(p):
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
				self.image_ctrl = wx.StaticBitmap(self, wx.ID_ANY, bitmap, wx.DefaultPosition, wx.DefaultSize, 0)
				root.Add(self.image_ctrl, 0, wx.ALL|wx.EXPAND, 5)
			except Exception as e:
				print(f"加载图片失败: {e}")

		progressbar1 = wx.BoxSizer(wx.VERTICAL)

		self.progressbar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
		self.progressbar.SetValue(50)
		self.progressbar.SetForegroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ))

		progressbar1.Add(self.progressbar, 0, wx.ALL|wx.EXPAND, 5)

		self.running_tip = wx.StaticText(self, wx.ID_ANY, _(u"正在加载："), wx.DefaultPosition, wx.DefaultSize, 0)
		self.running_tip.Wrap(-1)

		progressbar1.Add(self.running_tip, 0, wx.ALL, 5)

		self.running_detail = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY)
		progressbar1.Add(self.running_detail, 1, wx.ALL|wx.EXPAND, 5)


		root.Add(progressbar1, 1, wx.EXPAND, 5)


		self.SetSizer( root )
		self.Layout()

		self.Centre(wx.BOTH)

	def __del__( self ):
		pass


if __name__ == "__main__":
	app = wx.App(False)
	dlg = running(None)
	dlg.ShowModal()
	dlg.Destroy()

