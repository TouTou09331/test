# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class Fibersim_dialog
###########################################################################

class Fibersim_dialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"导入几何信息", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.Size( 1000,-1 ), wx.DefaultSize )

		bSizerFibersim = wx.BoxSizer( wx.VERTICAL )

		self.m_panelTop = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizerTopButtons = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText_FileName = wx.StaticText( self.m_panelTop, wx.ID_ANY, u"文件名称：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_FileName.Wrap( -1 )

		bSizerTopButtons.Add( self.m_staticText_FileName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_textCtrl_FileName = wx.TextCtrl( self.m_panelTop, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		bSizerTopButtons.Add( self.m_textCtrl_FileName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizerTopButtons.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText_ImportGrid = wx.StaticText( self.m_panelTop, wx.ID_ANY, u"导入尺寸定义表：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_ImportGrid.Wrap( -1 )

		bSizerTopButtons.Add( self.m_staticText_ImportGrid, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_textCtrl_ImportGrid = wx.TextCtrl( self.m_panelTop, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 250,-1 ), 0 )
		bSizerTopButtons.Add( self.m_textCtrl_ImportGrid, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_bpButton_ShowGrid = wx.BitmapButton( self.m_panelTop, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 60,26 ), wx.BU_AUTODRAW|0 )
		bSizerTopButtons.Add( self.m_bpButton_ShowGrid, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizerTopButtons.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizerTopButtons.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		self.m_panelTop.SetSizer( bSizerTopButtons )
		self.m_panelTop.Layout()
		bSizerTopButtons.Fit( self.m_panelTop )
		bSizerFibersim.Add( self.m_panelTop, 0, wx.EXPAND, 5 )

		self.m_scrolledGridPanel = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledGridPanel.SetScrollRate( 5, 5 )
		self.m_scrolledGridPanel.Hide()

		bSizerGridsContent = wx.BoxSizer( wx.VERTICAL )

		bSizerStructuralUnitID = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledGridPanel, wx.ID_ANY, u"结构单元ID" ), wx.VERTICAL )

		self.m_gridStructuralUnitID = wx.grid.Grid( bSizerStructuralUnitID.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_gridStructuralUnitID.CreateGrid( 10, 10 )
		self.m_gridStructuralUnitID.EnableEditing( True )
		self.m_gridStructuralUnitID.EnableGridLines( True )
		self.m_gridStructuralUnitID.EnableDragGridSize( False )
		self.m_gridStructuralUnitID.SetMargins( 0, 0 )

		# Columns
		self.m_gridStructuralUnitID.EnableDragColMove( False )
		self.m_gridStructuralUnitID.EnableDragColSize( True )
		self.m_gridStructuralUnitID.SetColLabelSize( 0 )
		self.m_gridStructuralUnitID.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_gridStructuralUnitID.EnableDragRowSize( True )
		self.m_gridStructuralUnitID.SetRowLabelSize( 0 )
		self.m_gridStructuralUnitID.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_gridStructuralUnitID.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.m_gridStructuralUnitID.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizerStructuralUnitID.Add( self.m_gridStructuralUnitID, 1, wx.ALL|wx.EXPAND, 2 )


		bSizerGridsContent.Add( bSizerStructuralUnitID, 0, wx.ALL|wx.EXPAND, 3 )

		bSizerPlyNumbers = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledGridPanel, wx.ID_ANY, u"铺层数" ), wx.VERTICAL )

		self.m_gridPlyNumbers = wx.grid.Grid( bSizerPlyNumbers.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_gridPlyNumbers.CreateGrid( 10, 10 )
		self.m_gridPlyNumbers.EnableEditing( True )
		self.m_gridPlyNumbers.EnableGridLines( True )
		self.m_gridPlyNumbers.EnableDragGridSize( False )
		self.m_gridPlyNumbers.SetMargins( 0, 0 )

		# Columns
		self.m_gridPlyNumbers.EnableDragColMove( False )
		self.m_gridPlyNumbers.EnableDragColSize( True )
		self.m_gridPlyNumbers.SetColLabelSize( 0 )
		self.m_gridPlyNumbers.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_gridPlyNumbers.EnableDragRowSize( True )
		self.m_gridPlyNumbers.SetRowLabelSize( 0 )
		self.m_gridPlyNumbers.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_gridPlyNumbers.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizerPlyNumbers.Add( self.m_gridPlyNumbers, 1, wx.ALL|wx.EXPAND, 2 )


		bSizerGridsContent.Add( bSizerPlyNumbers, 0, wx.ALL|wx.EXPAND, 3 )

		bSizerPlyRatio = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledGridPanel, wx.ID_ANY, u"铺层比" ), wx.VERTICAL )

		self.m_gridPlyRatio = wx.grid.Grid( bSizerPlyRatio.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_gridPlyRatio.CreateGrid( 10, 10 )
		self.m_gridPlyRatio.EnableEditing( True )
		self.m_gridPlyRatio.EnableGridLines( True )
		self.m_gridPlyRatio.EnableDragGridSize( False )
		self.m_gridPlyRatio.SetMargins( 0, 0 )

		# Columns
		self.m_gridPlyRatio.EnableDragColMove( False )
		self.m_gridPlyRatio.EnableDragColSize( True )
		self.m_gridPlyRatio.SetColLabelSize( 0 )
		self.m_gridPlyRatio.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_gridPlyRatio.EnableDragRowSize( True )
		self.m_gridPlyRatio.SetRowLabelSize( 0 )
		self.m_gridPlyRatio.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_gridPlyRatio.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizerPlyRatio.Add( self.m_gridPlyRatio, 1, wx.ALL|wx.EXPAND, 2 )


		bSizerGridsContent.Add( bSizerPlyRatio, 0, wx.ALL|wx.EXPAND, 3 )

		bSizerPlyBase = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledGridPanel, wx.ID_ANY, u"铺层库" ), wx.VERTICAL )

		self.m_gridPlyBase = wx.grid.Grid( bSizerPlyBase.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_gridPlyBase.CreateGrid( 10, 10 )
		self.m_gridPlyBase.EnableEditing( True )
		self.m_gridPlyBase.EnableGridLines( True )
		self.m_gridPlyBase.EnableDragGridSize( False )
		self.m_gridPlyBase.SetMargins( 0, 0 )

		# Columns
		self.m_gridPlyBase.EnableDragColMove( False )
		self.m_gridPlyBase.EnableDragColSize( True )
		self.m_gridPlyBase.SetColLabelSize( 0 )
		self.m_gridPlyBase.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_gridPlyBase.EnableDragRowSize( True )
		self.m_gridPlyBase.SetRowLabelSize( 0 )
		self.m_gridPlyBase.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_gridPlyBase.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizerPlyBase.Add( self.m_gridPlyBase, 1, wx.ALL|wx.EXPAND, 2 )


		bSizerGridsContent.Add( bSizerPlyBase, 0, wx.ALL|wx.EXPAND, 3 )


		self.m_scrolledGridPanel.SetSizer( bSizerGridsContent )
		self.m_scrolledGridPanel.Layout()
		bSizerGridsContent.Fit( self.m_scrolledGridPanel )
		bSizerFibersim.Add( self.m_scrolledGridPanel, 0, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.LI_HORIZONTAL )
		bSizerFibersim.Add( self.m_staticline1, 0, wx.EXPAND, 5 )

		self.m_panelButtom = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizerButtom = wx.BoxSizer( wx.HORIZONTAL )


		bSizerButtom.Add( ( 0, 0), 1, wx.EXPAND, 0 )

		self.m_buttonStartImport = wx.Button( self.m_panelButtom, wx.ID_ANY, u"开始导入", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		bSizerButtom.Add( self.m_buttonStartImport, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_buttonApply = wx.Button( self.m_panelButtom, wx.ID_ANY, u"应用", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		bSizerButtom.Add( self.m_buttonApply, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_buttonCancel = wx.Button( self.m_panelButtom, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		bSizerButtom.Add( self.m_buttonCancel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizerButtom.Add( ( 0, 0), 1, wx.EXPAND, 0 )


		self.m_panelButtom.SetSizer( bSizerButtom )
		self.m_panelButtom.Layout()
		bSizerButtom.Fit( self.m_panelButtom )
		bSizerFibersim.Add( self.m_panelButtom, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizerFibersim )
		self.Layout()
		bSizerFibersim.Fit( self )

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


