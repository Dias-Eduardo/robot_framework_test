
import sys
sys.path.append('/opt/trex/trex-core/scripts/automation/trex_control_plane/interactive/trex/examples/astf') # astf_path.py


import astf_path
from trex.astf.api import *

import os

from robot.api import logger # Imprimir para o console com o Robot Framework


c = 0
passed = 0


def init(profile_name):
    # Recebemos como argumento o nome do profile que deve ser carregado para fazer a comunicação
    global c
    global passed

    # Criamos um objeto do tipo "ASTFClient" que modelará a comunicação  
    c = ASTFClient()
    
    # Conectamos ao servidor do T-Rex que deve ser iniciado anteriormente
    c.connect()

    # Resetamos a comunicação
    c.reset()

    # Carregamos o profile que foi passado no argumento
    profile_path = os.path.join(astf_path.get_profiles_path(), profile_name)
    c.load_profile(profile_path)

    # Limpamos as estatisticas 
    c.clear_stats()

    passed = True

    robot_print("\n#\tPortas configuradas!")
    

def start_traffic(multiplicador, duracao):
    global c

    robot_print("\n#\tComecando trafego...")
    horario_inicio = datetime.now() # Pegamos o horario de inicio do trafego
    robot_print("#\tTeste comecado as " + str(horario_inicio))

    c.start(mult = multiplicador, duration = duracao, latency_pps = 1) # Iniciamos o trafego

    c.wait_on_traffic() # Esperamos ate que o trafego seja concluido

    horario_termino = datetime.now() # Pegamos o horario de termino do teste
    robot_print("#\tTeste terminado as " + str(horario_termino)) 
    duracao_teste_real = horario_termino - horario_inicio
    robot_print("\n#\tDuracao do teste: " + duracao_teste_real)


def print_stats_and_get_lost_packets():
    global c
    stats = c.get_stats()
    # robot_print(stats) # Para imprimir todo o dict com todas as estatisticas de disponiveis

    lat_stats = c.get_latency_stats()

    # robot_print(lat_stats) # Para imprimir todo o dict com todas as estatisticas de latencia disponiveis

    client_stats = stats['traffic']['client']
    server_stats = stats['traffic']['server']

    tcp_client_sent, tcp_server_recv = client_stats.get('tcps_sndbyte', 0), server_stats.get('tcps_rcvbyte', 0)
    tcp_server_sent, tcp_client_recv = server_stats.get('tcps_sndbyte', 0), client_stats.get('tcps_rcvbyte', 0)

    udp_client_sent, udp_server_recv = client_stats.get('udps_sndbyte', 0), server_stats.get('udps_rcvbyte', 0)
    udp_server_sent, udp_client_recv = server_stats.get('udps_sndbyte', 0), client_stats.get('udps_rcvbyte', 0)

    
    # Caso o número de pacotes enviados pelo cliente e recebidos pelo servidor, ou vice-versa, sejam diferentes, o teste irá falhar
    if (tcp_client_sent != tcp_server_recv):
        robot_print("\n#\tMuitos pacotes TCP perdidos: cliente mandou %s bytes e o servidor recebeu %s bytes" % (tcp_client_sent, tcp_server_recv))
        return False;
    elif (tcp_server_sent != tcp_client_recv):
        robot_print("\n#\tMuitos pacotes TCP perdidos: servidor mandou %s bytes e o cliente recebeu %s bytes" % (tcp_server_recv, tcp_client_sent))
        return False;
    elif (udp_client_sent != udp_server_sent):
        robot_print("\n#\tMuitos pacotes UDP perdidos: cliente mandou %s bytes e o servidor recebeu %s bytes" % (udp_client_sent, udp_server_recv))
        return False;
    elif (udp_server_sent != udp_client_recv):
        robot_print("\n#\tMuitos pacotes UDP perdidos: servidor mandou %s bytes e o cliente recebeu %s bytes" % (udp_server_sent, udp_client_recv))
        return False;


    robot_print(client_stats)

    robot_print("\n\n\n");

    robot_print(server_stats)




def disconnect():
    global c
    c.disconnect()


def robot_print(msg):
    logger.console(msg) 