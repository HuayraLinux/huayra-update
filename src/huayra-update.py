#! /usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from wx.lib.pubsub import pub
import os.path
from dbus.mainloop.glib import DBusGMainLoop
import subprocess
import threading

from lib.about import AboutDialog
from lib.networking import NetworkStatus


def popenAndCall(onExit, popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that
    would give to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs):
        proc = subprocess.Popen(*popenArgs)
        proc.wait()
        onExit()
        return
    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    # returns immediately after the thread starts
    return thread


class test(object):
    def on_connect(self):
        wx.CallAfter(
            pub.sendMessage,
            'network-connected',
            val=True
        )

    def on_disconnect(self):
        wx.CallAfter(
            pub.sendMessage,
            'network-connected',
            val=False
        )


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

        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnUpdate)

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
        if self.frame._is_updating == False:
            self.frame._is_updating = True

            popenAndCall(self.frame._proc_done, ['gpk-update-viewer'])

        else:
            'ah ah ah, no digiste la palabra mágica'

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

        self._is_updating = False
        self._proc = None

        self.tray_icon = HuayraUpdateIcon(self)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        pub.subscribe(self.LaunchPK, 'network-connected')

    def _proc_done(self):
        self._is_updating = False

    def LaunchPK(self, val):
        print 'A LA FLAUTA:', type(val), val

    def OnClose(self, evt):
        if self._is_updating:
            return None

        self.tray_icon.RemoveIcon()
        self.tray_icon.Destroy()
        self.Destroy()


class HuayraUpdate(wx.App):
    def __init__(self):
        self.app_path = os.path.dirname(os.path.realpath(__file__))
        super(HuayraUpdate, self).__init__(redirect=False)

    def OnInit(self):
        proxy_test = test()

        DBusGMainLoop(set_as_default=True)
        a = NetworkStatus(proxy=proxy_test)

        return True


if __name__ == '__main__':
    app = HuayraUpdate()
    frame = MainFrame()
    app.MainLoop()
