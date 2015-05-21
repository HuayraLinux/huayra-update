# -*- coding: utf-8 -*-

import wx
import os.path

TITLE_TXT = """Huayra Update"""
ABOUT_TXT = """Te avisa cuando hay actualizaciones del sistema disponibles."""
VERSION_TXT = """Versión: 0.3"""

class AboutDialog(wx.Frame):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(
            parent=parent,
            title=u'Acerca de',
        )

        img = os.path.join(wx.GetApp().app_path, 'media', 'fondo.png')
        bmp = wx.Image(img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        panel = wx.Panel(self)
        wx.StaticBitmap(panel, -1, bmp, (0, 0))

        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Asap')

        txt = wx.StaticText(panel, id=-1, label=TITLE_TXT, pos=(115, 40))
        txt.SetFont(
            wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Asap')
        )

        txt1 = wx.StaticText(panel, id=-1, label=ABOUT_TXT, pos=(115, 58))
        txt1.Wrap(200)
        txt1.SetFont(font)

        txt2 = wx.StaticText(panel, id=-1, label=VERSION_TXT, pos=(115, 120))
        txt2.Wrap(200)
        txt2.SetFont(font)


        self.SetMinSize((350, 250))
        self.SetMaxSize((350, 250))

        w, h = wx.DisplaySize()
        x = (w / 2) - (350 / 2)
        y = (h / 2) - (250 / 2)

        self.SetPosition((x,y))

    def OnClose(self, evt):
        self.Close()
