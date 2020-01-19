import socket
import time
from typing import List, Tuple

import Messages


class Connection:
    def __init__(self,connection_type) -> None:
        self.is_connected=False #when send and received version and verack to node
        self.socket=None
        self.connection_type=connection_type


    def connect_to_node(self, ip_addr: str):
        self.socket=socket.socket(socket.AF_INET, self.connection_type)
        try:
            # self.socket.settimeout(2000)
            #Tcp Connection
            self.socket.settimeout(5)
            self.socket.connect((ip_addr, 8333))
            if socket.SOCK_STREAM==self.connection_type:
                print("Nawiązano połączenie TCP")
            else:
                print("Nawiązano połączenie UDP")

            #version message
            message_version=Messages.version_message()
            self.socket.send(bytes(message_version))
            print("Wiadomość version wysłana\nOczekuje na odpowiedź...\n")
            Messages.receive_version(self.socket)

            #verack message
            message_verack=Messages.verack_message()
            self.socket.send(bytes(message_verack))
            print("Wiadomość verack wysłana\nOczekuje na odpowiedź...\n")
            Messages.receive_verack(self.socket)

            self.is_connected=True
            print("Ustanowiono połaczenie, można wysyłać wiadomości do węzła\n")




        except socket.error as err:
            print(err)
            if socket.SOCK_STREAM==self.connection_type:
                print("Nie udało się nawiązać połączenia TCP")
            else:
                print("Nie udało się nawiązać połączenia UDP")


    def get_addr(self):
        message=Messages.get_addr()
        self.socket.send(message)
        print("Wiadomość getaddr wysłana\nOczekuje na odpowiedź...\n")

        addr_list: List[Tuple[str, int]]=Messages.receive_addr(self.socket)
        for addr in addr_list:
            print("Adres: "+str(addr[0])+" port:"+str(addr[1]))
    def addr(self,ip,port):
        self.socket.send(Messages.addr(ip,port))
        print("Wiadomość addr pomyślnie wysłana")

