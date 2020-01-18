import hashlib
import random
import struct
import time
import socket
from os import linesep as endl




def version_message()->str:
    version = struct.pack("i", 60002)
    services = struct.pack("Q", 0) #	unsigned long long
    timestamp = struct.pack("q", int(time.time()))
    addr_recv = struct.pack("Q", 0)
    addr_recv += struct.pack(">16s", str.encode("127.0.0.1"))
    addr_recv += struct.pack(">H", 8333)
    addr_from = struct.pack("Q", 0)
    addr_from += struct.pack(">16s", str.encode("127.0.0.1"))
    addr_from += struct.pack(">H", 8333)
    nonce = struct.pack("Q", random.getrandbits(64))
    user_agent_bytes = struct.pack("B", 0)
    height = struct.pack("i", 0)
    payload = version + services + timestamp + addr_recv + addr_from + nonce +user_agent_bytes + height
    message=make_header_message("version",payload)
    return message


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
    while True:
        magic_letters = socket.recv(4)
        if magic_letters.hex() == "f9beb4d9":
            command = socket.recv(12).decode("utf-8")
            if messsage_name == command[0:len(messsage_name)]:
                print("Odebrano zwrotną wiadomość "+messsage_name+endl)
                payload_lenght=socket.recv(4)
                payload_lenght=struct.unpack("I",payload_lenght)[0]
                socket.recv(4)  # drop checksum
                return payload_lenght

def verack_message():
   message= make_header_message("verack",b"")
   return message


def receive_verack(socket: socket.socket):
    receive_header(socket,"verack")

