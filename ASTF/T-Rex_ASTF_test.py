
import sys
sys.path.append('/opt/trex-datacom/trex-core/scripts/automation/trex_control_plane/interactive/trex/examples/astf') # astf_path.py


import astf_path
from trex.astf.api import *

import os

from robot.api import logger # Imprimir para o console com o Robot Framework
from datetime import datetime

c = 0
passed = 0
duracao_teste_real = 0


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
    global duracao_teste_real

    robot_print("\n#\tComecando trafego...")
    horario_inicio = datetime.now() # Pegamos o horario de inicio do trafego
    robot_print("#\tTeste comecado as " + str(horario_inicio))

    c.start(mult = multiplicador, duration = duracao, latency_pps = 1) # Iniciamos o trafego

    c.wait_on_traffic() # Esperamos ate que o trafego seja concluido

    horario_termino = datetime.now() # Pegamos o horario de termino do teste
    robot_print("#\tTeste terminado as " + str(horario_termino))

    duracao_teste_real = horario_termino - horario_inicio # Calculamos o tempo do teste


def print_stats_and_check_error():
    global c
    stats = c.get_stats()
    # robot_print(stats) # Para imprimir todo o dict com todas as estatisticas de disponiveis
    
    client_stats = stats['traffic']['client']
    server_stats = stats['traffic']['server']
    robot_print(client_stats) # Para imprimir o dict com todas as estatisticas do cliente disponiveis
    robot_print(server_stats) # Para imprimir o dict com todas as estatisticas do servidor disponiveis
       
    robot_print("\n#\tDuracao do teste: " + str(duracao_teste_real))
    
    robot_print("\n#\tEstatisticas do cliente:")
    robot_print("#\t\tTentativas de conexão feitas: " + str(client_stats['tcps_connattempt']))
    robot_print("#\t\tConexões feitas: " + str(client_stats['tcps_connects']))
    robot_print("#\t\tConexões encerradas: " + str(client_stats['tcps_closed']))
    robot_print("#\t\tBytes enviados: " + str(client_stats['tcps_sndbyte']))
    robot_print("#\t\tBytes enviados confirmados: " + str(client_stats['tcps_sndbyte_ok']))
    robot_print("#\t\tACKs enviados: " + str(client_stats['tcps_sndacks']))
    robot_print("#\t\tACKs recebidos: " + str(client_stats['tcps_rcvackpack']))
    robot_print("#\t\tPacotes enviados por segundo: " + str(client_stats['m_tx_pps_r']))
    robot_print("#\t\tPacotes recebidos por segundo: " + str(client_stats['m_rx_pps_r']))
    
    robot_print("\n\n");
    
    robot_print("\n#\tEstatisticas do servidor:")
    robot_print("#\t\tConexões aceitas: " + str(server_stats['tcps_accepts']))
    robot_print("#\t\tConexões feitas: " + str(server_stats['tcps_connects']))
    robot_print("#\t\tConexões encerradas: " + str(server_stats['tcps_closed']))
    robot_print("#\t\tBytes enviados: " + str(server_stats['tcps_sndbyte']))
    robot_print("#\t\tBytes enviados confirmados: " + str(server_stats['tcps_sndbyte_ok']))
    robot_print("#\t\tACKs enviados: " + str(server_stats['tcps_sndacks']))
    robot_print("#\t\tACKs recebidos: " + str(server_stats['tcps_rcvackpack']))
    robot_print("#\t\tPacotes enviados por segundo: " + str(server_stats['m_tx_pps_r']))
    robot_print("#\t\tPacotes recebidos por segundo: " + str(server_stats['m_rx_pps_r']))
    
    robot_print("\n\n");
    
    lat_stats = c.get_latency_stats()

    # robot_print(lat_stats) # Para imprimir todo o dict com todas as estatisticas de latencia disponiveis   
   
    
    if client_stats['tcps_connattempt'] == client_stats['tcps_connects'] and client_stats['tcps_connects'] == client_stats['tcps_closed']:
    	return True
    else:
    	return False
    



def disconnect():
    global c
    c.disconnect()


def robot_print(msg):
    logger.console(msg) 
