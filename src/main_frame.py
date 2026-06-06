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
#  Class main
#---------------------------------------------------------------------------

class main ( wx.Frame ):

	def __init__(self, parent):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 911,561 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		self.SetBackgroundColour(wx.Colour("#6495ED"))

		root = wx.BoxSizer(wx.VERTICAL)

		head = wx.BoxSizer(wx.HORIZONTAL)

		self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, u"输入或点击\"...\"选择文件", _(u"选择文件"), _(u"*.enbx*"), wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL)
		self.m_filePicker1.SetForegroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
		self.m_filePicker1.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ))
		self.m_filePicker1.SetMinSize(wx.Size( 200,-1 ))

		head.Add(self.m_filePicker1, 0, 0, 5)

		self.preview = wx.Button(self, wx.ID_ANY, _(u"预览"), wx.DefaultPosition, wx.DefaultSize, 0)
		head.Add(self.preview, 0, 0, 5)

		self.output = wx.Button(self, wx.ID_ANY, _(u"导出docx"), wx.DefaultPosition, wx.DefaultSize, 0)
		head.Add(self.output, 0, 0, 5)


		root.Add(head, 0, wx.EXPAND, 5)

		preview = wx.BoxSizer(wx.HORIZONTAL)

		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_LEFT )
		self.m_notebook1.SetForegroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ))
		self.m_notebook1.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ))


		preview.Add(self.m_notebook1, 1, wx.EXPAND, 5)


		root.Add(preview, 1, wx.EXPAND, 5)


		self.SetSizer( root )
		self.Layout()

		self.Centre(wx.BOTH)

	def __del__( self ):
		pass


if __name__ == '__main__':
	app = wx.App()
	main(None).Show()
	app.MainLoop()
	