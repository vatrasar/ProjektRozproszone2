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
		self.connection_type=socket.SOCK_STREAM#tcp default

		self.connection=None  #init in connect_to_peer method
		self.commands_map: Dict[str, Callable[[], None]] = {"ping": self.ping, "help": self.print_commands,
													   "ustaw adres": self.set_target_node_adress,
													   "polacz": self.connect_to_peer,
														"dns":self.print_nodes_addres_form_dns,
															"getaddr":self.get_addr,
															"addr":self.addr,
															"udp":self.set_udp,
															"tcp":self.set_tcp,
															"getheaders":self.get_headers,
															"getblocks":self.get_blocks,
															"getdata":self.get_data,
															"inv":self.inv}#dostepne w konsoli polecenia

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
			  "getaddr: uzyskanie adresów innych węzłow z danego węzła\n"
			  "getheaders: wyswietla nagłówki\n"
			  "getblocks: wyświetla bloki\n"
			  "getdata: wyświetla dane\n"
			  "inv:\n")
	def print_nodes_addres_form_dns(self):
		PeerDiscovery.print_nodes_form_DNS()

	def connect_to_peer(self):
		if(self.target_node_adress==""):
			self.set_target_node_adress()
		self.connection=Connection(self.connection_type)
		self.connection.connect_to_node(self.target_node_adress)

	def get_addr(self):
		if(self.connection==None or not(self.connection.is_connected)):
			print("Operacja niedostępna. Najpierw musisz nawiązać połaczenie z węzłem.")
			return


		self.connection.get_addr()

	def run_console(self):
		self.to_close: bool = False
		while not(self.to_close):


			activity = self.get_activity()
			try:
				activity()
			except TimeoutError:
				print("Zby dlugi czas oczekiwania")
			except socket.error as err:
				print(err)
				print("Czas na odpowiedź minął")


	def set_udp(self):

		self.connection_type=socket.SOCK_DGRAM
		if self.connection!=None:
			self.connection.is_connected=False
		print("Połaczenie bedzie teraz realizowane przy pomocy UDP")
	def set_tcp(self):

		self.connection_type=socket.SOCK_STREAM
		if self.connection!=None:
			self.connection.is_connected=False

		print("Połaczenie bedzie teraz realizowane przy pomocy TCP")
	def get_activity(self):
		while True:
			command = input("Podaj polecenie>")


			activity = self.commands_map.get(command)
			if activity==None:
				print("Podana nazwa polecenia jest błędna")
				continue
			return activity
	def addr(self):
		if (self.connection == None or not (self.connection.is_connected)):
			print("Operacja niedostępna. Najepierw musisz nawiązać połaczenie z węzłem.")
			return
		ip=None
		port=None
		while True:
			adress = input("Podaj adres ip do wysłania>")
			if self.is_address_valid(adress):
				ip = adress
				break
			else:
				print("Podano nieprawidlowy adres ip")

		while True:
			port_: str = input("Podaj numer portu>")
			if port_.isnumeric():
				port = port_
				break
			else:
				print("Podano zły numer portu")
		self.connection.addr(ip,port)

	def inv(self):
		if (self.connection == None or not (self.connection.is_connected)):
			print("Operacja niedostępna. Najpierw musisz nawiązać połaczenie z węzłem.")
			return
		self.connection.inv()

	def get_blocks(self):
		if (self.connection == None or not (self.connection.is_connected)):
			print("Operacja niedostępna. Najpierw musisz nawiązać połaczenie z węzłem.")
			return
		self.connection.get_blocks()

	def get_headers(self):
		if (self.connection == None or not (self.connection.is_connected)):
			print("Operacja niedostępna. Najpierw musisz nawiązać połaczenie z węzłem.")
			return
		self.connection.get_headers()

	def is_hash_valid(self, valid_hash):
		if len(valid_hash) == 64:
			return True
		else:
			return False
			
	def get_data(self):
		if (self.connection == None or not (self.connection.is_connected)):
			print("Operacja niedostępna. Najpierw musisz nawiązać połaczenie z węzłem.")
			return
		tx_id=None
		while True:
			t_id = input("Podaj hash transakcji do pobrania>")
			if self.is_hash_valid(t_id):
				tx_id = t_id
				break
			else:
				print("Podano nieprawidlowy hash\nPodaj hash SHA-256>")
		self.connection.get_data(tx_id)





if __name__ == '__main__':
	console=Console()
	console.run_console()









