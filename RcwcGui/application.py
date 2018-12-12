from .form.main_form import MainForm
import wx


class Application(wx.App):

    @property
    def MainForm(self):
        return self._MainForm

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        super(Application, self).__init__(redirect, filename, useBestVisual, clearSigInt)
        self._MainForm = MainForm(title=u"原煤可选性曲线")

    def run(self):
        if self._MainForm != None and isinstance(self._MainForm, MainForm):
            self._MainForm.Show(True)
            self.MainLoop()
        else:
            raise Exception("找不到指定的窗体.")
