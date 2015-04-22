#! /usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os.path
from dbus.mainloop.glib import DBusGMainLoop

from lib.about import AboutDialog
from lib.networking import NetworkStatus


class HuayraUpdateIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        super(HuayraUpdateIcon, self).__init__()
        self.frame = frame

        self.icon = wx.IconFromBitmap(wx.Bitmap(os.path.join(
            wx.GetApp().app_path,
            'media',
            'huayra-update.png'
        )))
        self.change_tooltip(u'Hay actualizaciones de Huayra disponibles.')

        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnUpdate)

    def change_tooltip(self, text):
        self.SetIcon(self.icon, text)

    def CreatePopupMenu(self, evt=None):
        menu = wx.Menu()
        btn_update = menu.Append(id=-1, text=u'Actualizar Huayra')
        btn_about = menu.Append(id=-1, text='Acerca de')
        menu.AppendSeparator()
        btn_exit = menu.Append(id=wx.ID_EXIT, text=u'Cerrar')

        menu.Bind(wx.EVT_MENU, self.OnUpdate, btn_update)
        menu.Bind(wx.EVT_MENU, self.OnAbout, btn_about)
        menu.Bind(wx.EVT_MENU, self.OnExit, btn_exit)

        return menu

    def OnUpdate(self, evt):
        print 'actualizar'

    def OnAbout(self, evt):
        about_screen = AboutDialog(self.frame)
        about_screen.Show()

    def OnExit(self, evt):
        self.frame.Close()


class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(
            parent=None,
            id=-1,
            title=u'Huayra Update',
        )

        self.tray_icon = HuayraUpdateIcon(self)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, evt):
        self.tray_icon.RemoveIcon()
        self.tray_icon.Destroy()
        self.Destroy()


class HuayraUpdate(wx.App):
    def __init__(self):
        self.app_path = os.path.dirname(os.path.realpath(__file__))
        super(HuayraUpdate, self).__init__(redirect=False)

    def OnInit(self):
        DBusGMainLoop(set_as_default=True)
        a = NetworkStatus()

        return True


if __name__ == '__main__':
    app = HuayraUpdate()
    frame = MainFrame()
    app.MainLoop()
