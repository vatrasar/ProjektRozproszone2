import os
import platform
import subprocess
from typing import Dict, Callable
import re



class Console:

    def __init__(self) -> None:
        self.target_node_adress=""
    def set_target_node_adress(self):
        while True:
            adress=input("Podaj adres ip docelowego węzła>")
            if self.is_address_valid(adress):
                self.target_node_adress=adress
                print("Pomyslnie zmieniono adres docelowego wezla\n")
                break
            else:
                print("Podano nieprawidlowy adres ip")

    def is_address_valid(self, adress):
        return re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", adress)

    def ping(self):


        param = '-n' if platform.system().lower() == 'windows' else '-c'
        print("Wysyłanie pinga....\n")
        if self.target_node_adress=="":
            self.set_target_node_adress()

        command = ['ping', param, '5', self.target_node_adress]

        if subprocess.call(command, stdout=open(os.devnull, 'wb')) == 0:
            print("Host został osiągnięty")
        else:
            print("Host nie został osiągnięty")

    def print_commands(self):
        print("ping:wysyłanie pinga\n"
              "help:pomoc\n"
              "version:wyslanie wiadomosci version\n"
              "ustaw adres:ustawia adres docelowego węzła\n")
    def run_console(self):
        to_close: bool = False
        while not(to_close):


            activity = self.get_activity()

            activity()



    def get_activity(self):
       while True:
            command = input("Podaj polecenie>")
            commands_map: Dict[str, Callable[[], None]] = {"ping": self.ping,"help":self.print_commands,"ustaw adres":self.set_target_node_adress}

            activity = commands_map.get(command)
            if activity==None:
                print("Podana nazwa polecenia jest błędna")
                continue
            return activity





if __name__ == '__main__':
    console=Console()
    console.run_console()









