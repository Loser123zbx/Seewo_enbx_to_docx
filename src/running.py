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
		wx.Dialog.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 739,224 ), style = wx.CAPTION|wx.DEFAULT_DIALOG_STYLE)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		root = wx.BoxSizer(wx.HORIZONTAL)

		self.progress_bitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap( u"progress.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0)
		root.Add(self.progress_bitmap, 0, 0, 5)

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

