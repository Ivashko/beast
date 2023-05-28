from scapy.all import *


def tcp_sniff(packet):
    global flag
    if packet.haslayer(IP):
        if packet[IP].dport == 1111 and str(packet[IP])[52:]:
            if flag:
                with open("/home/beast/beast/tmp.txt", "w") as file:
                    file.write(str(packet[IP])[52:])
                flag = False
            else:
                flag = True


def listen():
    sniff(iface="lo", prn=tcp_sniff, store=0)

    
if __name__ == "__main__":
    flag = True
    listen()
    
