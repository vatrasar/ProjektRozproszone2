import socket

import Messages


class Connection:
    def __init__(self) -> None:
        self.is_connected=False #when send and received version and verack to node
        self.socket=None

    def connect_to_node(self, ip_addr: str):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # self.socket.settimeout(2000)
            #Tcp Connection
            self.socket.connect((ip_addr, 8333))
            print("Nawiązano połączenie TCP")

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




        except socket.error:
            print("Nie udało się nawiązać połączenia TCP")


