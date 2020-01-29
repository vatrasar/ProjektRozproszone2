import socket
import time
from typing import List, Tuple
import binascii
import Encode
import Messages
from exceptions import UnexpectedInV


class Connection:
	def __init__(self,connection_type) -> None:
		self.is_connected=False  #when send and received version and verack to node
		self.socket=None
		self.connection_type=connection_type


	def connect_to_node(self, ip_addr: str):
		self.socket=socket.socket(socket.AF_INET, self.connection_type)
		try:
			self.socket.settimeout(5)
			#Tcp Connection
			self.socket.connect((ip_addr, 8333))
			if socket.SOCK_STREAM==self.connection_type:
				print("Nawiązano połączenie TCP")
			# else:
			#     print("Nawiązano połączenie UDP")
			self.socket.settimeout(None)

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
		except TimeoutError:
			print("Czas na zwrocenie wiadomosci minął")
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

	def inv(self):
		print("Wiadomść inv wysłana")

	def get_blocks(self):
		message_getblocks=Messages.getblocks_message()
		self.socket.send(bytes(message_getblocks))
		print("Wysłano wiadomość getblocks")
		time.sleep(3)
		while True:
			try:
				for i in range(0,2):
					if Messages.receive_header(self.socket, "inv"):
						break
				Encode.encode_inv(self.socket)
				break #everything ok
			except UnexpectedInV:
				continue

		#hash of gensis block: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f

	def get_headers(self):
		print("Wiadomść getHeaders wysłana")

	def get_data(self, tx_id):
		magic_value = 0xd9b4bef9
		#tx_id = "fc67704eff327aecfadb2cf3774edc919ba69aba624b836461ce2be9c00a0c20"
		buffer_size = 1024
		message_getdata = Messages.getdata_message(tx_id)
		self.socket.send(bytes(message_getdata))
		print("Wysłano wiadomość getdata")
		time.sleep(3)
		while True:
			if Messages.receive_header(self.socket, "tx"):
				Encode.encode_transaction(self.socket)
				break
			self.socket.send(bytes(message_getdata))
			print("Wysłano wiadomość getdata")
