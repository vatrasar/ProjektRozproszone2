import hashlib
import random
import struct
import time
import socket
from os import linesep as endl
import binascii
import utils
import math

def encode_inv(socket):
	num_of_inputs = int.from_bytes(socket.recv(1),byteorder='little')
	print("Liczba danych wejściowych: "+str(num_of_inputs))
	#hash wyjscia
	i = 0
	while i < num_of_inputs:
		msg_type = int.from_bytes(socket.recv(4),byteorder='little')
		if msg_type == 1:
			print("Hash transakcji "+str(i)+":")
		elif msg_type == 2:
			print("Hash bloku "+str(i)+":")
		else:
			print("Rodzaj wiadomosci: "+str(msg_type)+"\nHash: ")
		msg_hash = socket.recv(32)
		print(str(binascii.hexlify(msg_hash)))
		i = i + 1

def encode_transaction(socket):
	print("Version: ")
	ver = int.from_bytes(socket.recv(2),byteorder='little')
	ver2 = int.from_bytes(socket.recv(2),byteorder='little')
	print(ver)
	tx_type = ['Payment', 'Coinstake', 'Deposit', 'Vote', 'Logout', 'Slash', 'Withdraw', 'Admin']
	print("Typ transakcji: "+str(tx_type[ver2]))
	num_of_inputs = int.from_bytes(socket.recv(1),byteorder='little')
	print("Liczba danych wejściowych: "+str(num_of_inputs))
	#hash wyjscia
	tx_hash = socket.recv(32)
	print("Hash transakcji wyjściowej: "+str(binascii.hexlify(tx_hash)))
	index = int.from_bytes(socket.recv(4),byteorder='little')
	print("Index: "+str(index))
	if int.from_bytes(tx_hash,byteorder='little' )==0:
		print("Ta transakcja jest pierwszą w bloku")
	#...
	else:
		length_str = int.from_bytes(socket.recv(3),byteorder='little')
		off = math.floor(length_str/1024)
		for i in range(0, off):
			a=socket.recv(1024)
		socket.recv(length_str-(1024*off))
		i = 1
		while i < num_of_inputs:
			tx_hash = socket.recv(32)
			print(str(i)+". Hash transakcji wyjściowej: "+str(binascii.hexlify(tx_hash)))
			index = int.from_bytes(socket.recv(4),byteorder='little')
			print(" Index: "+str(index))
			length_str = int.from_bytes(socket.recv(3),byteorder='little')
			off = math.floor(length_str/1024)
			for i in range(0, off):
				a=socket.recv(1024)
			socket.recv(length_str-(1024*off))
			
			print("Wersja wiadomości wysyłającego: "+str(int.from_bytes(socket.recv(4),byteorder='little')))
			i = i + 1
	
