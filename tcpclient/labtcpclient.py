#!/usr/bin/python3
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



import socket
from time import sleep


class LabTcpClient:
    """Envoi et réception sur le même socket en TCP.
    Toutes les méthodes sont sans try.
    """

    def __init__(self, ip, port):

        self.ip = ip
        self.port = port
        self.server_address = (ip, port)
        self.data = None
        self.sock = None
        self.create_socket()

    def create_socket(self):
        """Création du socket sans try, et avec connexion."""

        while not self.sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect_sock()
            print("Création du socket client {}".format(self.server_address))
            sleep(0.01)

    def connect_sock(self):
        """Connexion de la socket, si ok retoune 1 sinon None"""

        try:
            self.sock.connect(self.server_address)
            return 1
        except:
            print("Connexion impossible du client sur {}".
                  format(self.server_address))
            return None

    def send(self, msg):
        """Envoi d'un message, avec send, msg doit être encodé avant."""

        # Création d'un socket si besoin
        if not self.sock:
            self.create_socket()

        # Envoi
        try:
            self.sock.send(msg)
        except:
            print("Envoi raté: {}".format(msg))
            # Nouvelle création d'une socket
            self.sock.close()
            self.sock = None

    def reconnect(self):
        """Reconnexion."""

        self.sock = None
        self.create_socket()

    def close_sock(self):
        """Fermeture de la socket."""

        try:
            self.sock.close()
        except:
            print("La socket client est déjà close")

        self.sock = None

    def listen(self):
        """Retourne les data brutes reçues."""

        raw_data = None

        raw_data = self.sock.recv()

        return raw_data


if __name__ == "__main__":

    ip = "192.168.1.12"
    port = 8000

    clt = LabTcpClient(ip, port)

    int_list = [x for x in range(20)]
    for num in int_list:
        num = str(num).encode("utf-8")
        print(num)
        clt.send(num)
        sleep(1)
        if num == 10:
            clt = None

    clt.close_sock()
