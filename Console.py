import os
import platform
import socket
import subprocess
from typing import Dict, Callable
import re

import Messages
import PeerDiscovery
from Connection import Connection


class Console:

    def __init__(self) -> None:
        self.target_node_adress=""
        self.connection=None  #init in connect_to_peer method
        self.commands_map: Dict[str, Callable[[], None]] = {"ping": self.ping, "help": self.print_commands,
                                                       "ustaw adres": self.set_target_node_adress,
                                                       "polacz": self.connect_to_peer,
                                                        "dns":self.print_nodes_addres_form_dns,
                                                            "getaddr":self.get_addr}#dostepne w konsoli polecenia

    def set_target_node_adress(self):
        while True:
            adress=input("Podaj adres ip docelowego węzła>")
            if self.is_address_valid(adress):
                self.target_node_adress=adress
                if self.connection!=None:
                    self.connection.is_connected=False
                print("Pomyslnie zmieniono adres docelowego wezla\n")
                break
            else:
                print("Podano nieprawidlowy adres ip")

    def is_address_valid(self, adress):
        return re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", adress)

    def ping(self):


        param = '-n' if platform.system().lower() == 'windows' else '-c'

        if self.target_node_adress=="":
            self.set_target_node_adress()
        print("Wysyłanie pinga....\n")

        #wysyłanie pinga
        command = ['ping', param, '1', self.target_node_adress]

        if subprocess.call(command, stdout=open(os.devnull, 'wb')) == 0:
            print("Sukces!")
        else:
            print("Host nie został osiągnięty")

    def print_commands(self):
        print("ping:wysyłanie pinga\n"
              "help:pomoc\n"
              "polacz:ustanawia połączenie z wybranym węzłem(wysyła version i verack)\n"
              "ustaw adres:ustawia adres docelowego węzła\n"
              "dns: wyszukiwanie adresów węzłów za pomocą dns\n"
              "getaddr: uzyskanie adresów innych węzłow z danego węzła")
    def print_nodes_addres_form_dns(self):
        PeerDiscovery.print_nodes_form_DNS()

    def connect_to_peer(self):
        if(self.target_node_adress==""):
            self.set_target_node_adress()
        self.connection=Connection()
        self.connection.connect_to_node(self.target_node_adress)

    def get_addr(self):
        if(self.connection==None or not(self.connection.is_connected)):
            print("Operacja niedostępna. Najepierw musisz nawiązać połaczenie z węzłem.")
            return


        self.connection.get_addr()

    def run_console(self):
        self.to_close: bool = False
        while not(self.to_close):


            activity = self.get_activity()
            try:
                activity()
            except Exception:
                print("Zby dlugi czas oczekiwania")



    def get_activity(self):
       while True:
            command = input("Podaj polecenie>")


            activity = self.commands_map.get(command)
            if activity==None:
                print("Podana nazwa polecenia jest błędna")
                continue
            return activity





if __name__ == '__main__':
    console=Console()
    console.run_console()









