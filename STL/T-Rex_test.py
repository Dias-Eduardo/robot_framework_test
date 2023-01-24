
import sys
sys.path.append('/opt/trex-core/scripts/automation/trex_control_plane/interactive/trex/examples/stl') # stl_path.py

import stl_path
from trex.stl.api import *

from robot.api import logger # Imprimir para o console com o Robot Framework

from datetime import datetime

import time
import json

# Esse programa envia x pacotes da porta 0 para a porta 1 e x pacotes da porta 1 para a porta 0.

c = 0
passed = 0
duracao_teste_real = 0

def init(packet_0, packet_1, velocidade):
    global c
    global passed
  
    c = STLClient() # Criamos uma instancia da classe STLClient que irá administrar todo o fluxo de pacotes
    passed = True

    stl_pkt_0 = STLPktBuilder(pkt = packet_0) # Criamos as duas instancias da classe STLPktBuilder que definirá
    stl_pkt_1 = STLPktBuilder(pkt = packet_1) # os pacotes a serem enviados pelo fluxo. A classe recebe como construtor 
                                              # apenas o pacote que criamos anteriormente em Scapy.

    # Definimos o primeiro objeto STLStream, que modela um fluxo de pacotes, o qual o formato é definido no parametro "packet",
    # com a velocidade sendo definida no parâmetro "mode". O parametro "flow_stats" indica que queremos registrar as estatisticas
    # de latencia, pois por default isso não é registrado.
    # Esse primeiro objeto irá definir um fluxo de pacotes da porta 0 para a porta 1
    s1 = STLStream(packet = stl_pkt_0,
                    mode = STLTXCont(pps = velocidade),
                    flow_stats = STLFlowLatencyStats(pg_id = 7))


    # Definimos o segundo objeto STLStream para modelar o nosso segundo fluxo, que irá da porta 1 para a porta 0.
    # A única diferença aqui é que usamos o parametro "isg" (Inter-Stream Gap) para definir um atraso entre os fluxos
    s2 = STLStream(packet = stl_pkt_1,
                    isg = 1000,
                    mode = STLTXCont(pps = velocidade),
                    flow_stats = STLFlowLatencyStats(pg_id = 8))
    
    # Conectamos com o servidor que deve ter sido iniciado
    c.connect()                                                                

    # Resetamos as configurações passadas das portas que serão utilizadas, neste exemplo serão apenas as portas 0 e 1
    c.reset(ports = [0, 1])     

    #  Associamos os objetos STLStream, que definem o fluxo, que criamos anteriormente para as suas devidas portas.
    c.add_streams(s1, ports = [0])
    c.add_streams(s2, ports = [1])

    # Limpamos todas as estatíscas que tinham sido usadas anteriormente. Caso queira-se medir as estatisticas de todas os
    # protocolos de uma só vez basta comentar essa linha.
    c.clear_stats()
    
    robot_print("\n#\tPortas configuradas!")


def start_traffic (duracao):
    global c
    global duracao_teste_real

    robot_print("\n#\tComecando trafego...")
    horario_inicio = datetime.now() # Pegamos o horario de inicio do trafego
    robot_print("#\tTeste comecado as " + str(horario_inicio))
    c.start(ports = [0, 1], duration = duracao)  # Iniciamos o trafego

    c.wait_on_traffic(ports = [0, 1]) # Esperamos ate que o trafego seja concluido

    horario_termino = datetime.now() # Pegamos o horario de termino do teste
    robot_print("#\tTeste terminado as " + str(horario_termino))

    duracao_teste_real = horario_termino - horario_inicio # Calculamos o tempo do teste


def get_lost_packets():
    # Função para imprimir as estatisticas referentes ao fluxo 
    global c
    stats = c.get_stats()
    # robot_print(stats) # Para imprimir todo o dict com todas as estatisticas disponiveis                                                 

    # Pegamos as estatiscas de latencia de cada uma das portas
    lat_stats_0 = stats['latency'].get(7)
    lat_0 = lat_stats_0['latency']

    lat_stats_1 = stats['latency'].get(8)
    lat_1 = lat_stats_1['latency']
     
    robot_print("\n#\tDuracao do teste: " + str(duracao_teste_real))

    robot_print("\n#\tEstatisticas da porta 0:")
    robot_print("#\t\tPacotes enviados: " + str(stats[0]["opackets"]))
    robot_print("#\t\tPacotes recebidos: " + str(stats[0]["ipackets"]))
    robot_print("#\t\tVelocidade de envio: " + str(stats[0]["tx_pps"]) + " pps")
    robot_print("#\t\tVelocidade de recebimento: " + str(stats[0]["rx_pps"]) + " pps")
    robot_print("#\t\tJitter: " + str(lat_0['jitter']) + " microssegundos")
    robot_print("#\t\tAverage Latency: " + str(lat_0['average']) + " microssegundos")
    robot_print("#\t\tMax Latency: " + str(lat_0['total_max']) + " microssegundos")
    robot_print("#\t\tMin Lantency: " +  str(lat_0['total_min']) + " microssegundos")

    robot_print("\n#\tEstatisticas da porta 1:")
    robot_print("#\t\tPacotes enviados: " + str(stats[1]["opackets"]))
    robot_print("#\t\tPacotes recebidos: " + str(stats[1]["ipackets"]))
    robot_print("#\t\tVelocidade de envio: " + str(stats[1]["tx_pps"]) + " pps")
    robot_print("#\t\tVelocidade de recebimento: " + str(stats[1]["rx_pps"]) + " pps")
    robot_print("#\t\tJitter: " + str(lat_1['jitter']) + " microssegundos") 
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
