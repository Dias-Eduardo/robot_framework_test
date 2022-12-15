T_REX_VERSION = "2.87"

import sys
sys.path.append('/opt/trex/v' + T_REX_VERSION + '/automation/trex_control_plane/interactive/trex/examples/stl') # stl_path.py

import stl_path
from trex.stl.api import *

from robot.api import logger # Imprimir para o console com o Robot Framework

from datetime import datetime

import time
import json

# Esse programa envia x pacotes da porta 0 para a porta 1 e x pacotes da porta 1 para a porta 0.

c = 0
passed = 0

def init(packet_0, packet_1, velocidade):
    global c
    global passed
  
    c = STLClient()
    passed = True

    stl_pkt_0 = STLPktBuilder(pkt = packet_0)
    stl_pkt_1 = STLPktBuilder(pkt = packet_1)

    s1 = STLStream(packet = stl_pkt_0,
                    mode = STLTXCont(pps = velocidade),
                    flow_stats = STLFlowLatencyStats(pg_id = 7))

    s2 = STLStream(packet = stl_pkt_1,
                    isg = 1000,
                    mode = STLTXCont(pps = velocidade),
                    flow_stats = STLFlowLatencyStats(pg_id = 8))
    
    c.connect()                                                                

    c.reset(ports = [0, 1])     

    c.add_streams(s1, ports = [0])

    c.add_streams(s2, ports = [1])

    c.clear_stats()
    
    robot_print("\n#\tPortas configuradas!")


def start_traffic (duracao):
    global c
    
    robot_print("\n#\tComecando trafego...")
    robot_print("#\tTeste comecado as " + str(datetime.now()))
    c.start(ports = [0, 1], duration = duracao)                     

    c.wait_on_traffic(ports = [0, 1])

    robot_print("#\tTeste terminado as " + str(datetime.now())) 


def get_lost_packets(nome_protocolo):
    global c
    stats = c.get_stats()
    #robot_print(stats) # Para imprimir todo o dict das estatisticas                                                 

    lat_stats_0 = stats['latency'].get(7)
    lat_0 = lat_stats_0['latency']

    lat_stats_1 = stats['latency'].get(8)
    lat_1 = lat_stats_1['latency']
   
    robot_print("\n#\tTeste do protocolo: " + nome_protocolo)

 

    robot_print("\n#\tEstatisticas da porta 0:")
    robot_print("#\t\tPacotes enviados: " + str(stats[0]["opackets"]))
    robot_print("#\t\tPacotes recebidos: " + str(stats[0]["ipackets"]))
    robot_print("#\t\tVelocidade de envio: " + str(stats[0]["tx_pps"]) + " pps")
    robot_print("#\t\tVelocidade de recebimento: " + str(stats[0]["rx_pps"]) + " pps")
    robot_print("#\t\tJitter: " + str(lat_0['jitter']) + " microssegundos") # Não sei oq esse  número significa ainda, perguntar pra alguem inteligente
    robot_print("#\t\tAverage Latency: " + str(lat_0['average']) + " microssegundos")
    robot_print("#\t\tMax Latency: " + str(lat_0['total_max']) + " microssegundos")
    robot_print("#\t\tMin Lantency: " +  str(lat_0['total_min']) + " microssegundos")
    robot_print("\n#\tEstatisticas da porta 1:")
    robot_print("#\t\tPacotes enviados: " + str(stats[1]["opackets"]))
    robot_print("#\t\tPacotes recebidos: " + str(stats[1]["ipackets"]))
    robot_print("#\t\tVelocidade de envio: " + str(stats[1]["tx_pps"]) + " pps")
    robot_print("#\t\tVelocidade de recebimento: " + str(stats[1]["rx_pps"]) + " pps")
    robot_print("#\t\tJitter: " + str(lat_1['jitter']) + " microssegundos") # Não sei oq esse  número significa ainda, perguntar pra alguem inteligente
    robot_print("#\t\tAverage Latency: " + str(lat_1['average']) + " microssegundos")
    robot_print("#\t\tMax Latency: " + str(lat_1['total_max']) + " microssegundos")
    robot_print("#\t\tMin Lantency: " +  str(lat_1['total_min']) + " microssegundos")
    lost_1 = stats[0]["opackets"] - stats[1]["ipackets"]
    lost_0 = stats[1]["opackets"] - stats[0]["ipackets"]
    robot_print("\n#\tPacotes perdidos de 0 para 1: " + str(lost_1))
    robot_print("#\tPacotes perdidos de 1 para 0: " + str(lost_0))
    return lost_0 + lost_1

def robot_print(msg):
    logger.console(msg)        


def disconnect():
    global c
    c.disconnect()


