import hashlib
import random
import struct
import time
import socket
from socket import timeout
from os import linesep as endl
import binascii
import utils
import uuid


def version_message()->str:
	version = struct.pack("i", 60002)
	services = struct.pack("Q", 0) #	unsigned long long
	timestamp = struct.pack("q", int(time.time()))
	addr_recv = struct.pack("Q", 0)
	addr_recv += struct.pack(">16s", str.encode("127.0.0.2"))
	addr_recv += struct.pack(">H", 8330)
	addr_from = struct.pack("Q", 0)
	addr_from += struct.pack(">16s", str.encode("127.0.0.1"))
	addr_from += struct.pack(">H", 8333)
	nonce = struct.pack("Q", random.getrandbits(64))
	user_agent_bytes = struct.pack("B", 0)
	height = struct.pack("i", 0)
	payload = version + services + timestamp + addr_recv + addr_from + nonce +user_agent_bytes + height
	message=make_header_message("version",payload)
	return message
def pack_addr(ip,port_number):
	stime = struct.pack("I", int(time.time()))
	addr_recv = struct.pack("Q", 0)
	addr_recv += struct.pack(">16s", str.encode(ip))
	addr_recv += struct.pack(">H", int(port_number))
	return stime+addr_recv

def make_header_message(command, payload: bytes):
	magic = bytes.fromhex("F9BEB4D9") # Main network
	command = command + (12 - len(command)) * "\00"
	command=str.encode(command)
	length = struct.pack("I", len(payload))
	check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
	return magic + command + length + check + payload

def receive_version(socket: socket.socket):
	payload_lenght=receive_header(socket,"version")
	socket.recv(payload_lenght)#drop payload(rest of version message)
	return

def receive_header(socket: socket.socket,messsage_name:str)->int:
	"""

	:param socket:
	:param messsage_name:
	:return payload_lenght: length of rest of message
	"""
	start=time.time()
	while True:

		if time.time()-start>10:
			return
			raise IndexError()
		magic_letters = socket.recv(4)
		if magic_letters.hex() == "f9beb4d9":
			command = socket.recv(12).decode("utf-8")
			print("Jest wiadomość…"+str(command))
			com=str(command)
			# if com=='ping':
			# 	socket.send(bytes(pong_message(socket.recv(8))))
			# 	print("Wysłano wiadomość pong")
			if messsage_name == command[0:len(messsage_name)]:
				print("Odebrano zwrotną wiadomość "+messsage_name+endl)
				payload_lenght = get_payload_lenght(socket)
				socket.recv(4)  # drop checksum
				return payload_lenght
			else:
				drop_message(socket)
				#return 0


def get_payload_lenght(socket):
	payload_lenght = socket.recv(4)
	payload_lenght = struct.unpack("I", payload_lenght)[0]
	return payload_lenght


def drop_message(socket: socket.socket):
	payload_lenght = get_payload_lenght(socket)
	# clear_buffer(socket)
	socket.recv(4)  # drop checksum
	socket.recv(payload_lenght)#drop message

def clear_buffer(sock):
	try:
		while sock.recv(1024): pass
	except:
		pass

def verack_message():
   message= make_header_message("verack",b"")
   return message


def receive_verack(socket: socket.socket):
	receive_header(socket,"verack")


def get_addr():


	message=make_header_message("getaddr",b"")
	return message


def addr(ip_addres,port):
	var_int_adress_number=utils.varint(1)
	# timestamp=struct.pack("q", int(time.time()))
	payload=var_int_adress_number+pack_addr(ip_addres,port)
	return make_header_message("addr",payload)
def receive_addr(socket: socket.socket):


	payload=receive_header(socket,"addr")

	addr_number = get_addr_number(socket)

	# socket.recv(4)#drop timestamp
	addr_list=[]
	for i in range(0,addr_number):
		socket.recv(4)#drop time
		socket.recv(8)#drop service
		socket.recv(12)#drop ipv6
		ipv4=socket.recv(4)


		ipv4=utils.convert_hexip_to_str_ip(ipv4)
		port_hex=socket.recv(2).hex()
		port=int(port_hex,16)
		addr_list.append((ipv4,port))
	return addr_list

def get_addr_number(socket):
	var_int_prefix = socket.recv(1)
	var_int_prefix_hex = int(var_int_prefix.hex(),16)
	addr_number = 0
	if var_int_prefix_hex < 0xfd:
		addr_number = var_int_prefix_hex
	elif var_int_prefix_hex == 0xfd:
		addr_number = struct.unpack('<H', socket.recv(2))[0]
	elif var_int_prefix_hex == 0xfe:
		addr_number = struct.unpack('<L', socket.recv(4))[0]
		# return [struct.unpack('<L', payload[1:5])[0], 5]
	else:
		addr_number = struct.unpack('<Q', socket.recv(8))[0]
	return addr_number
	
	
	

def create_message(magic, command, payload):
	checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[0:4]
	return(struct.pack('L12sL4s', magic, command.encode(), len(payload), checksum) + payload)

def create_payload_getdata(tx_id):
	count = 1
	type = 1
	hash = bytearray.fromhex(tx_id)
	payload = struct.pack('<bb32s', count, type, hash)
	return(payload)
	
def getblocks_message()->str:
	version = struct.pack("i", 60002)
	hash_count = struct.pack("<B", 1)
	block_header_hashes = binascii.unhexlify('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')
	stop_hash = struct.pack("<32s",str.encode('00000000000000000000000000000000'))
	payload = version + hash_count + block_header_hashes + stop_hash
	message=make_header_message("getblocks",payload)
	return message

def getdata_message(tx_hash)->str:
	hash_count = struct.pack("<B", 1)
	type_msg = struct.pack("<I", 1)
	block_header_hashes = binascii.unhexlify(tx_hash)
	payload = hash_count + type_msg + block_header_hashes
	message=make_header_message("getdata",payload)
	return message

def pong_message(nonce)->str:
	message=make_header_message("pong",nonce)
	return message
