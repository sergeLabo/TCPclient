#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

####################################################################
# This file is part of TCPclient.

# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#####################################################################

    
"""
projet TCPclient
Send data to ip, port for test
"""

from os import _exit

import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock

from labtcpclient import LabTcpClient


class MainScreen(Screen):
    """Ecran principal"""

    info = StringProperty()
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        print("Initialisation de MainScreen ok")
        
        self.config = TCPclientApp.get_running_app().config
        self.create_client()

        # Boucle
        freq = int(self.config.get('network', 'freq'))
        tempo = 1 / freq
        self.event = Clock.schedule_interval(self.update, tempo)
        self.num = 0
        
    def update(self, dt):
        self.info = str(self.num)
        data = str(self.num).encode("utf-8")
        self.clt.send(data)
        self.num += 1
        
    def create_client(self):
        self.ip = self.config.get('network', 'tcp_ip')
        self.port = int(self.config.get('network', 'tcp_port'))
        print("ip =", self.ip)
        print("port =", self.port)
        self.clt = LabTcpClient(self.ip, self.port)
        print("Création d'un client TCP", self.clt)

    def reset_client(self):
        self.clt = None
        self.create_client()
        print("Client réinitialisé")
        
    def reset_clock(self):
        self.event.cancel()
        freq = int(self.config.get('network', 'freq'))
        tempo = 1 / freq
        self.event = Clock.schedule_interval(self.update, tempo)

    def do_reset(self):
        self.num = 0

     
SCREENS = { 0: (MainScreen, "Main")}


class TCPclientApp(App):
    
    def build(self):
        """Execute en premier apres run()"""

        # Creation des ecrans
        self.screen_manager = ScreenManager()
        for i in range(len(SCREENS)):
            self.screen_manager.add_widget(SCREENS[i][0](name=SCREENS[i][1]))

        return self.screen_manager

    def on_start(self):
        """Execute apres build()"""
        pass

    def build_config(self, config):
        """Si le fichier *.ini n'existe pas,
        il est cree avec ces valeurs par defaut.
        Si il manque seulement des lignes, il ne fait rien !
        """

        config.setdefaults('network',
                            { 'tcp_ip': '127.0.0.1',
                              'tcp_port': '8000',
                              'freq': '1'})

        config.setdefaults('kivy',
                            { 'log_level': 'debug',
                              'log_name': 'tcpclient_%y-%m-%d_%_.txt',
                              'log_dir': '/log',
                              'log_enable': '1'})

        config.setdefaults('postproc',
                            { 'double_tap_time': 250,
                              'double_tap_distance': 20})

    def build_settings(self, settings):
        """Construit l'interface de l'ecran Options,
        pour  le serveur seul, Kivy est par defaut,
        appele par app.open_settings() dans .kv
        """

        data =  """[{"type": "title", "title":"Reseau"},
                            {  "type":    "numeric",
                                "title":   "Frequence",
                                "desc":    "Frequence entre 1 et 60 Hz",
                                "section": "network", 
                                "key":     "freq"},

                    {"type": "title", "title":"Reseau"},
                            {   "type":    "string",
                                "title":   "TCP IP",
                                "desc":    "TCP IP",
                                "section": "network", 
                                "key":     "tcp_ip"},
                                
                    {"type": "title", "title":"Reseau"},
                            {   "type":    "numeric",
                                "title":   "TCP Port",
                                "desc":    "TCP Port",
                                "section": "network", 
                                "key":     "tcp_port"}
                    ]
                """

        # self.config est le config de build_config
        settings.add_json_panel('TCPclient', self.config, data=data)

    def on_config_change(self, config, section, key, value):
        """Si modification des options, fonction appelee automatiquement
        """

        freq = int(self.config.get('network', 'freq'))
        ip = self.config.get('network', 'tcp_ip')
        port = int(self.config.get('network', 'tcp_port'))
        menu = self.screen_manager.get_screen("Main")

        if config is self.config:
            token = (section, key)

            # If frequency change
            if token == ('network', 'freq'):
                print("Nouvelle frequence", freq)
                menu.reset_clock()

            # If ip change
            if token == ('network', 'tcp_ip'):
                print("Nouvelle ip", ip)
                menu.reset_client()

            # If port change
            if token == ('network', 'tcp_port'):
                print("Nouveau port", port )
                menu.reset_client()
                
    def go_mainscreen(self):
        """Retour au menu principal depuis les autres ecrans."""

        #if touch.is_double_tap:
        self.screen_manager.current = ("Main")

    def do_reset(self):
        """reset de self.num"""

        menu = self.screen_manager.get_screen("Main")
        menu.do_reset()
        
    def do_quit(self):
        print("Je quitte proprement")

        # Kivy
        TCPclientApp.get_running_app().stop()

        # Extinction de tout
        _exit(0)


if __name__ == "__main__":
    TCPclientApp().run()
