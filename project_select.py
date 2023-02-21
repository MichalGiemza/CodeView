import wx

last_projects = ["C:\\Projekty\\LushLandsGithub\\LushLands\\"]


class MyDialog(wx.Dialog):
    def __init__(self, parent, title, choices):
        super().__init__(parent, title=title)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.selected_choice = ""
        self.choices = wx.ListBox(self, choices=choices, style=wx.LB_SINGLE)
        vbox.Add(self.choices, 1, wx.EXPAND | wx.ALL, 20)

        confirm_button = wx.Button(self, label='Confirm')
        confirm_button.Bind(wx.EVT_BUTTON, self.OnConfirm)
        vbox.Add(confirm_button, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        self.SetSizer(vbox)
        self.Fit()

    def OnConfirm(self, event):
        self.selected_choice = self.choices.GetStringSelection()
        if self.selected_choice:
            self.EndModal(wx.ID_OK)
        else:
            raise NotImplementedError("TODO: Select new project (os directory selector and then add to list, automatically start this choice)")


def setup_selector():
    app = wx.App()
    dialog = MyDialog(None, title='Select a choice', choices=last_projects)
    dialog.Destroy()
    app.MainLoop()
    return dialog.selected_choice


if __name__ == '__main__':
    print(setup_selector())
