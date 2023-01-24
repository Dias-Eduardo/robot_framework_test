import sys
# Utilizamos a biblioteca Scapy que é incluída junto ao T-rex. 
sys.path.append('/opt/trex-core/scripts/external_libs/scapy-2.3.1/python3/scapy')
sys.path.append('/opt/trex-core/scripts/external_libs/scapy-2.3.1/python3/scapy/contrib')
sys.path.append('/opt/trex-core/scripts/external_libs/scapy-2.3.1/python3/scapy/layers')

from robot.api import logger # Imprimir para o console com o Robot Framework

import stl_path
from trex.stl.api import *
import igmp
import dhcp
import dhcp6

# Aqui criamos e definimos os pacotes a serem enviados com Scapy

def create_ether(mac_src, mac_dst):
    return Ether(src=mac_src, dst=mac_dst)


def create_ipv4(ip_src, ip_dst):
    return IP(src=ip_src, dst=ip_dst)


def create_ipv6(ip_src, ip_dst):
    return IPv6(src=ip_src, dst=ip_dst)


def create_bootp(client_hw_addr):
    return dhcp.BOOTP(chaddr=client_hw_addr, ciaddr='0.0.0.0', xid = 0x01020304, flags = 1)


def create_dhcp():
    return dhcp.DHCP(options=[("message-type","discover"),'end'])


def create_udp(port_src, port_dst):
    return UDP(dport=port_dst, sport=port_src)


def create_tcp(port_src, port_dst):
    return TCP(dport=port_dst, sport=port_src)


def create_icmp(type, code=0):
    return ICMP(type=type, code=code)


def create_arp(psrc, pdst, op=1):
    return ARP(pdst=pdst ,psrc= psrc, op=op)


def create_dns():
    return  DNS(rd=1, qd=DNSQR(qname='www.eduardodias.com'))


def create_dummy_bytes(size):
    return Raw(RandString(size=size))


def create_IGMP(type, gaddr):
    return igmp.IGMP(type=type, gaddr=gaddr)


def assemble_protocols(protocols):
    result_package = protocols[0]
    for i in range(1, len(protocols)):
        result_package /= protocols[i]
    return result_package



def robot_print(msg):
    logger.console(msg)        
