# -*- coding: utf-8 -*-

import wx
import wx.html
import os.path

import webbrowser


class wxHTML(wx.html.HtmlWindow):
    def OnLinkClicked(self, link):
        webbrowser.open(link.GetHref())


class AboutDialog(wx.Frame):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(
            parent=parent,
            title=u'Acerca de',
            style=wx.CLOSE_BOX
        )

        titular = wx.Panel(parent=self)
        txt = wx.StaticText(parent=titular, label=u'Huayra Update')
        txt.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        szr_titular = wx.BoxSizer(wx.HORIZONTAL)
        szr_titular.Add(txt)
        titular.SetSizer(szr_titular)

        panel = wx.Panel(parent=self)

        self.btn_close = wx.Button(parent=panel, label=u'Cerrar')
        self.btn_close.Bind(wx.EVT_BUTTON, self.OnClose)

        szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        szr_buttons.Add(self.btn_close, flag=wx.RIGHT, border=2)

        self.szr_panel = wx.BoxSizer(wx.VERTICAL)
        self.szr_panel.Add(szr_buttons)
        panel.SetSizer(self.szr_panel)

        # --
        self.messages = wxHTML(parent=self)
        self.messages.LoadPage(os.path.join(
            wx.GetApp().current_path,
            'media',
            'about.html'
        ))

        # --

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(titular, flag=wx.LEFT|wx.ALL, border=5)
        sizer.Add(self.messages, 1, flag=wx.EXPAND)
        sizer.Add(panel, flag=wx.ALL|wx.CENTER, border=5)

        self.SetSizer(sizer)

        self.SetMinSize((320, 240))
        self.SetMaxSize((320, 240))
        self.Center()

    def OnClose(self, evt):
        self.Close()
