#! /usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os.path
from dbus.mainloop.glib import DBusGMainLoop

from lib.networking import NetworkStatus
from lib.about import AboutDialog


class HuayraUpdate(wx.App):
    def OnInit(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__))

        DBusGMainLoop(set_as_default=True)
        a = NetworkStatus()

        return True


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.icon = wx.IconFromBitmap(wx.Bitmap(os.path.join(
            wx.GetApp().current_path,
            'media',
            'huayra-update.png'
        )))
        self.change_tooltip(u'Hay actualizaciones de Huayra disponibles.')

        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnUpdate)

    def change_tooltip(self, text):
        self.SetIcon(self.icon, text)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        btn_update = menu.Append(id=-1, text=u'Actualizar Huayra')
        btn_about = menu.Append(id=-1, text='Acerca de')
        menu.AppendSeparator()
        btn_exit = menu.Append(id=wx.ID_EXIT, text=u'Cerrar')

        menu.Bind(wx.EVT_MENU, self.OnUpdate, btn_update)
        menu.Bind(wx.EVT_MENU, self.OnAbout, btn_about)
        menu.Bind(wx.EVT_MENU, self.OnExit, btn_exit)

        return menu

    def OnUpdate(self, event):
        print 'actualizar'

    def OnAbout(self, event):
        about_screen = AboutDialog()
        about_screen.Show()

    def OnExit(self, event):
        wx.CallAfter(self.Destroy)



if __name__ == '__main__':
    app = HuayraUpdate()
    TaskBarIcon()
    app.MainLoop()
