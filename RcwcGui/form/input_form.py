import wx
import wx.xrc
import wx.grid
from RawCoalWashabilityCurve import Row
from ..validator.validators import FloatingPointValidator


class NumberEntry(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        """
        初始化数值录入框
        :param args:
        :param kwargs:
        """
        """
        录入限制在FloatingPointValidator里实现.
        """
        super(NumberEntry, self).__init__(validator=FloatingPointValidator(), *args, **kwargs)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFucus)
        pass

    # todo 切换至此录入框时默认选中.现在不起作用.
    def OnSetFucus(self, evt):
        self.SelectAll()
        evt.Skip()
        pass

    pass


class InputForm(wx.Dialog):

    def __init__(self, parent):
        super(InputForm, self).__init__(parent, id=wx.ID_ANY, title="请录入相关信息:", pos=wx.DefaultPosition,
                                        style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr)
        self.parent= parent
        gSizer2 = wx.GridSizer(0, 2, 0, 0)

        self.m_lable_min = wx.StaticText(self, wx.ID_ANY, u"密度下限", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_lable_min.Wrap(-1)
        gSizer2.Add(self.m_lable_min, 0, wx.ALL, 5)

        self.m_txtDensityLow = NumberEntry(self, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_txtDensityLow, 0, wx.ALL, 5)

        self.m_lable_max = wx.StaticText(self, wx.ID_ANY, u"密度上限", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_lable_max.Wrap(-1)
        gSizer2.Add(self.m_lable_max, 0, wx.ALL, 5)

        self.m_txtDensityHigh = NumberEntry(self, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_txtDensityHigh, 0, wx.ALL, 5)

        self.m_lable_r = wx.StaticText(self, wx.ID_ANY, u"产率（%）", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_lable_r.Wrap(-1)
        gSizer2.Add(self.m_lable_r, 0, wx.ALL, 5)

        self.m_txtProductivity = NumberEntry(self, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_txtProductivity, 0, wx.ALL, 5)

        self.m_lable_a = wx.StaticText(self, wx.ID_ANY, u"灰分（%）", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_lable_a.Wrap(-1)
        gSizer2.Add(self.m_lable_a, 0, wx.ALL, 5)

        self.m_txtAsh = NumberEntry(self, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_txtAsh, 0, wx.ALL, 5)

        self.m_btnOK = wx.Button(self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_btnOK.Bind(wx.EVT_BUTTON, self.OnOkClick)
        gSizer2.Add(self.m_btnOK, 0, wx.ALL, 5)

        self.m_btnCancel = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_btnCancel.Bind(wx.EVT_BUTTON, self.OnCancelClick)
        gSizer2.Add(self.m_btnCancel, 0, wx.ALL, 5)

        self.SetSizer(gSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def OnOkClick(self, evt):
        self.row = Row(float(self.m_txtDensityLow.Value),
                       float(self.m_txtDensityHigh.Value),
                       float(self.m_txtAsh.Value),
                       float(self.m_txtProductivity.Value)
                       )
        self.EndModal(wx.ID_OK)
        pass

    def OnCancelClick(self, evt):
        self.EndModal(wx.ID_CANCEL)
        pass
