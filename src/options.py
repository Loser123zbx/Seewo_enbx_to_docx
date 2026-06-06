import wx
import wx.xrc

import gettext
_ = gettext.gettext

#--------------------------------------------------------------------------
#  Class options
#---------------------------------------------------------------------------

class options ( wx.Frame ):

	def __init__(self, parent):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,264 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		self.SetBackgroundColour(wx.Colour( 239, 235, 235 ))

		root = wx.BoxSizer(wx.VERTICAL)

		color = wx.BoxSizer(wx.HORIZONTAL)

		self.background_color = wx.StaticText(self, wx.ID_ANY, _(u"背景色"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.background_color.Wrap(-1)

		self.background_color.SetFont(wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ))

		color.Add(self.background_color, 0, wx.ALL, 5)

		self.m_colourPicker1 = wx.ColourPickerCtrl(self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE)
		color.Add(self.m_colourPicker1, 0, wx.ALL, 5)

		self.enable_color = wx.Button(self, wx.ID_ANY, _(u"确认更改"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.enable_color.SetFont(wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ))

		color.Add(self.enable_color, 0, 0, 5)


		root.Add(color, 0, wx.EXPAND, 5)

		toumingdu = wx.BoxSizer(wx.HORIZONTAL)

		self.toumingdu_text = wx.StaticText(self, wx.ID_ANY, _(u"透明度"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.toumingdu_text.Wrap(-1)

		self.toumingdu_text.SetFont(wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ))

		toumingdu.Add(self.toumingdu_text, 0, wx.ALL, 5)

		self.m_slider1 = wx.Slider(self, wx.ID_ANY, 50, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_AUTOTICKS|wx.SL_BOTTOM|wx.SL_HORIZONTAL|wx.SL_LABELS)
		toumingdu.Add(self.m_slider1, 1, wx.ALL, 5)

		self.enable_toumingdu = wx.Button(self, wx.ID_ANY, _(u"确认更改"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.enable_toumingdu.SetFont(wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ))

		toumingdu.Add(self.enable_toumingdu, 0, 0, 5)


		root.Add(toumingdu, 0, wx.EXPAND, 5)

		others = wx.BoxSizer(wx.VERTICAL)

		booloptionsChoices = [_(u"是否调试"), _(u"是否默认在任务完成后删除任务过程中产生的垃圾"), _(u"是否默认只导出文字")]
		self.booloptions = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, booloptionsChoices, wx.LB_ALWAYS_SB|wx.LB_EXTENDED|wx.LB_MULTIPLE|wx.LB_NEEDED_SB)
		others.Add(self.booloptions, 1, wx.ALL|wx.EXPAND, 5)

		self.apply_all = wx.Button(self, wx.ID_ANY, _(u"确认更改"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.apply_all.SetFont(wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ))

		others.Add(self.apply_all, 0, wx.EXPAND, 5)

		self.options_reset = wx.Button(self, wx.ID_ANY, _(u"重置设置"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.options_reset.SetFont(wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ))

		others.Add(self.options_reset, 0, wx.EXPAND, 5)


		root.Add(others, 1, wx.EXPAND, 5)


		self.SetSizer( root )
		self.Layout()

		self.Centre(wx.BOTH)

	def __del__( self ):
		pass


