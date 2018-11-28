import wx
import wx.xrc
import wx.grid


class GridPopupMenu(wx.Menu):
    def __init__(self, parent):
        if not isinstance(parent, wx.grid.Grid):
            raise ValueError("父类必须为wx.grid.Grid类型!")
        super(GridPopupMenu, self).__init__()
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), '添加一行')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAddRow, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), '删除该行')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnDeleteRow, cmi)

    def OnAddRow(self, e):
        pass

    def OnDeleteRow(self, e):
        pass


class DataGrid(wx.grid.Grid):
    _HeaderAttr = None

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.WANTS_CHARS,
                 name=wx.grid.GridNameStr):
        super(DataGrid, self).__init__(parent, id=id, pos=pos, size=size, style=style, name=name)
        self.moveTo = None

        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.CreateGrid(7, 9)
        self.EnableEditing(True)
        # 设置列表标签左右以及上下对齐方式：左对齐，下沉
        self.SetColLabelAlignment(wx.ALIGN_CENTER_VERTICAL, wx.ALIGN_CENTER_HORIZONTAL)
        self._DrawHeader()
        self._DrawFooter()
        self._BindEvents()

        self.AddDataLine(4, 1.2, 1.3, 32.3, 3.6)
        pass

    def _SetCellStringLength(self, x, y, len):
        editor = wx.grid.GridCellTextEditor()
        editor.SetParameters(str.format("{0}", len))
        self.SetCellEditor(x, y, editor)
        pass

    def _SetFloatCell(self, x, y, value):
        editor = wx.grid.GridCellFloatEditor()
        self.SetCellEditor(x, y, editor)
        renderer = wx.grid.GridCellNumberRenderer()
        self.SetCellRenderer(x, y, renderer)
        self.SetCellValue(x, y, str.format("{0}", value))
        pass

    def _GetHeaderAttr(self):
        if self._HeaderAttr == None:
            attr = wx.grid.GridCellAttr()
            # 字体颜色：黑色
            attr.SetTextColour(wx.BLACK)
            # 设置背景颜色：红色
            # attr.SetBackgroundColour(wx.GREEN)
            # 设置字体格式
            attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            # 居中
            attr.SetAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            return attr
        else:
            return self._HeaderAttr
        pass

    def _DrawHeader(self):
        # 第一行:
        self.SetCellSize(0, 1, 1, 2)
        self.SetCellValue(0, 1, "浮沉组成")
        self.SetCellSize(0, 3, 1, 2)
        self.SetCellValue(0, 3, "浮煤累计")
        self.SetCellSize(0, 5, 1, 2)
        self.SetCellValue(0, 5, "沉煤累计")
        self.SetCellSize(0, 7, 1, 2)
        self.SetCellValue(0, 7, "邻近密度物含量")

        self.SetRowAttr(0, self._GetHeaderAttr())

        # 第二行
        self.SetCellValue(1, 0, "密度")
        self.SetCellSize(1, 1, 1, 2)
        self.SetCellValue(1, 1, "校正后")
        self.SetCellValue(1, 3, "数量")
        self.SetCellValue(1, 4, "灰分")
        self.SetCellValue(1, 5, "数量")
        self.SetCellValue(1, 6, "灰分")
        self.SetCellValue(1, 7, "分选密度")
        self.SetCellValue(1, 8, "数量")

        self.SetRowAttr(1, self._GetHeaderAttr())

        # 第三行
        self.SetCellValue(2, 0, "δ Kg/L")
        self.SetCellValue(2, 1, "占本级%")
        self.SetCellValue(2, 2, "灰分%")
        self.SetCellValue(2, 3, "r %")
        self.SetCellValue(2, 4, "A %")
        self.SetCellValue(2, 5, "r %")
        self.SetCellValue(2, 6, "A %")
        self.SetCellValue(2, 7, "δp Kg/L")
        self.SetCellValue(2, 8, "±0.1含量")
        self.SetRowAttr(2, self._GetHeaderAttr())
        # 第四行
        for x in range(9):
            self.SetCellValue(3, x, str.format("{0}", x + 1))
            pass
        self.SetRowAttr(3, self._GetHeaderAttr())
        pass

    def _DrawFooter(self):
        if self.NumberRows > 6:
            x = self.NumberRows - 3
            self.SetCellValue(x, 0, "合计")
            self.SetCellValue(x + 1, 0, "煤泥")
            self.SetCellValue(x + 2, 0, "总计")
            pass
        else:
            raise Exception("没有足够的行.")
        pass

    def _BindEvents(self):
        # test all the events
        # 左单击
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        # 右单击
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        # 左双击
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        # 右双击
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)

        # label 左单击
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        # label 右单击
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        # label 左双击
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        # label 右双击
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)

        self.Bind(wx.grid.EVT_GRID_COL_SORT, self.OnGridColSort)

        # 拖动Row大小
        self.Bind(wx.grid.EVT_GRID_ROW_SIZE, self.OnRowSize)
        # 拖动Col大小
        self.Bind(wx.grid.EVT_GRID_COL_SIZE, self.OnColSize)

        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnSelectCell)

        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        self.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        self.Bind(wx.grid.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)
        pass

    def AddDataLine(self, index, low, high, r, a):
        self.InsertRows(index, 1)
        density = str.format("{0}~{1}", low, high)
        self.SetCellValue(index, 0, density)
        self._SetFloatCell(index, 1, r)
        self._SetFloatCell(index, 2, a)
        pass

    def OnCellLeftClick(self, evt):
        evt.skip()

    def OnCellRightClick(self, evt):
        row = evt.GetRow()
        rowCount = self.NumberRows
        # 只在数据区域显示菜单.
        if rowCount <= 7 or (row >= 4 and row <= rowCount - 1 - 3):
            self.PopupMenu(GridPopupMenu(self), evt.GetPosition())

    def OnCellLeftDClick(self, evt):
        evt.skip()

    def OnCellRightDClick(self, evt):
        evt.skip()

    def OnLabelLeftClick(self, evt):
        evt.skip()

    def OnLabelRightClick(self, evt):
        evt.skip()

    def OnLabelLeftDClick(self, evt):
        evt.skip()

    def OnLabelRightDClick(self, evt):
        evt.skip()

    def OnGridColSort(self, evt):
        evt.skip()

    def OnRowSize(self, evt):
        evt.skip()

    def OnColSize(self, evt):
        evt.skip()

    def OnRangeSelect(self, evt):
        evt.skip()

    def OnCellChange(self, evt):
        evt.skip()

    def OnIdle(self, evt):
        # evt.skip()
        pass

    def OnSelectCell(self, evt):
        evt.skip()

    def OnEditorShown(self, evt):
        evt.skip()

    def OnEditorHidden(self, evt):
        evt.skip()

    def OnEditorCreated(self, evt):
        evt.skip()


pass


class MainForm(wx.Frame):
    """We simply derive a new class of Frame."""

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE | wx.TAB_TRAVERSAL)

        self._grid = DataGrid(self)

    def __del__(self):
        pass
