import socket


def print_nodes_form_DNS():
    dns_seed_list=("seed.bitcoin.sipa.be",
    "dnsseed.bluematt.me",
    "dnsseed.bitcoin.dashjr.org",
    "seed.bitcoinstats.com",
    "seed.bitcoin.jonasschnelli.ch",
    "seed.btc.petertodd.org")
    print("Wyszukane hosty to:")
    # print(socket.gethostbyname(dns_seed_list[0]))
    _,_,nodes_addrs=socket.gethostbyname_ex(dns_seed_list[0])
    for i,node in enumerate(nodes_addrs):
        print(node)

