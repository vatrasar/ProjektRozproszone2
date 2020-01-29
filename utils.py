import struct


def varint(n):
    if n < 0xfd:
        return struct.pack('<B', n)
    elif n < 0xffff:
        return struct.pack('<cH', '\xfd', n)
    elif n < 0xffffffff:
        return struct.pack('<cL', '\xfe', n)
    else:
        return struct.pack('<cQ', '\xff', n)

def check_varint_size(prefix):
    n0 = ord(prefix)
    if n0 < 0xfd:
        return 1
    elif n0 == 0xfd:
        return  2
    elif n0 == 0xfe:
        return 4
    else:
        return 6


def convert_hexip_to_str_ip(ipv4: bytes):

    a=convert_to_str(ipv4[0:1])
    b=convert_to_str(ipv4[1:2])
    c=convert_to_str(ipv4[2:3])
    d=convert_to_str(ipv4[3:4])
    dot="."
    return a+dot+b+dot+c+dot+d

def convert_to_str(ip_part: bytes):
    a=ip_part.hex()
    hex_as_decimal=int(a,16)
    decimal_hex_as_str=str(hex_as_decimal)
    # if len(decimal_hex_as_str)<3:
    #     zero_number=3-len(decimal_hex_as_str)
    #     zeros="0"*zero_number
    #     decimal_hex_as_str=zeros+decimal_hex_as_str
    return decimal_hex_as_str


def get_varInt_number(socket):
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