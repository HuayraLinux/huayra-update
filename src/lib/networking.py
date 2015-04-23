# -*- coding: utf-8 -*-

import dbus


class NetworkStatus(object):
    DBUS_IFACE = DBUS_NAME = 'org.freedesktop.NetworkManager'
    DBUS_PATH = '/org/freedesktop/NetworkManager'

    NM_STATE_REF = {
        0: 'NM_STATE_UNKNOWN',
        10: 'NM_STATE_ASLEEP',
        20: 'NM_STATE_DISCONNECTED',
        30: 'NM_STATE_DISCONNECTING',
        40: 'NM_STATE_CONNECTING',
        50: 'NM_STATE_CONNECTED_LOCAL',
        60: 'NM_STATE_CONNECTED_SITE',
        70: 'NM_STATE_CONNECTED_GLOBAL',
    }

    def __init__(self, *args, **kwargs):
        self._bus = dbus.SystemBus()
        self._current_status = 40

        self.proxy = kwargs['proxy']

        self._initial_status()
        self._bind_status()

    def _initial_status(self):
        nm = self._bus.get_object(self.DBUS_IFACE, self.DBUS_PATH)
        new_status = nm.Get(
            self.DBUS_NAME,
            'State',
            dbus_interface=dbus.PROPERTIES_IFACE)

        self._change_status(new_status)

    def _change_status(self, nm_state):
        new_status = nm_state

        if new_status in (30, 40):
            print 'Conectando/Desconectando, no hago nada.'

        elif new_status < self._current_status:
            self.proxy.on_disconnect()

        elif new_status > self._current_status:
            self.proxy.on_connect()

        self._current_status = new_status

        print self.NM_STATE_REF[self._current_status]

    def _bind_status(self):
        self._bus.add_signal_receiver(self._change_status, dbus_interface=self.DBUS_IFACE, signal_name='StateChanged')
