
# Aqui nós configuramos o profile que será depois carregado

def http_config_file(ip_client, ip_server):
    configuration_string = '''
from trex.astf.api import *


class Prof1():
    def __init__(self):
        pass

    def get_profile(self, **kwargs):
        # ip generator
        ip_gen_c = ASTFIPGenDist(ip_range=["''' + ip_client + '", "' + ip_client + '''"], distribution="seq")
        ip_gen_s = ASTFIPGenDist(ip_range=["'''+ ip_server + '", "' + ip_server + '''"], distribution="seq")
        ip_gen = ASTFIPGen(glob=ASTFIPGenGlobal(ip_offset="1.0.0.0"),
                           dist_client=ip_gen_c,
                           dist_server=ip_gen_s)

        return ASTFProfile(default_ip_gen=ip_gen,
                            cap_list=[ASTFCapInfo(file="../avl/delay_10_http_browsing_0.pcap",
                            cps=2.776)])


def register():
    return Prof1()
'''


    file = open('/opt/trex-datacom/trex-core/scripts/astf/http_simple.py', 'w+') # Trocar aqui caso path ao T-Rex seja diferente
    file.seek(0, os.SEEK_SET)   
    file.write(configuration_string)
