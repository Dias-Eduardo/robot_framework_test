***Settings***
Documentation    Arquivo para testar o T-Rex
Library    T-Rex_test.py
#Library    /opt/trex/v2.87/external_libs/scapy-2.4.3/scapy/layers/l2.py
Resource   Test_UDP.robot
Resource   Test_ICMP.robot
Resource   Test_DNS.robot
Resource   Test_ARP.robot
Resource   Test_IPv6.robot
Resource   Test_IGMP.robot
Resource   Test_DHCP.robot

*** Variables ***
# Os endereços MAC e IP das interfaces de rede que serão utilizadas nos testes. Neste teste possuimos apenas duas interfaces.
${mac_porta_0}    08:00:27:cf:c0:b4
${ip_porta_0}    192.168.50.2
${ipv6_porta_0}    fe80::53f8:e38a:c8b3:d5bc


${mac_porta_1}    08:00:27:64:1d:5c 
${ip_porta_1}    192.168.50.3
${ipv6_porta_1}    fe80::375d:8152:eece:a0c3


# Definir a velocidade e duracao de todos os testes
${velocidade}    ${100}     # Em pacotes por segundo
${duracao}    ${10}    # Em segundos

*** Test Cases ***

T-Rex DHCP Test
    Given the DHCP packets are created
        And the t-rex basic configuration is done
    When traffic is started through t-rex api
    Then all traffic sent is received without dropped packets
        And we then disconnect
        

T-Rex UDP Test
    Given the UDP packets are created
        And the t-rex basic configuration is done
    When traffic is started through t-rex api
    Then all traffic sent is received without dropped packets
        And we then disconnect


T-Rex IPv6 Test
    Given the IPv6 packets are created
        And the t-rex basic configuration is done
    When traffic is started through t-rex api
    Then all traffic sent is received without dropped packets
        And we then disconnect


T-Rex IGMP Test
    Given the IGMP packets are created
        And the t-rex basic configuration is done
    When traffic is started through t-rex api
    Then all traffic sent is received without dropped packets
        And we then disconnect


T-Rex ARP Test    
    Given the ARP packets are created
        And the t-rex basic configuration is done
    When traffic is started through t-rex api
    Then all traffic sent is received without dropped packets
        And we then disconnect


T-Rex ICMP Test
    Given the ICMP packets are created
        And the t-rex basic configuration is done
    When traffic is started through t-rex api
    Then all traffic sent is received without dropped packets
        And we then disconnect


T-Rex DNS Test    
    Given the DNS packets are created
        And the t-rex basic configuration is done
    When traffic is started through t-rex api
    Then all traffic sent is received without dropped packets
        And we then disconnect







*** Keywords ***
the t-rex basic configuration is done
    Init    ${packet_0}    ${packet_1}    ${velocidade}


traffic is started through t-rex api
    Start Traffic    ${duracao}


all traffic sent is received without dropped packets
    ${lost_packets}=    get_lost_packets
    ${no_error}=    Set Variable    ${True}
    IF  ${lost_packets} > ${0}
        ${no_error}=    ${False}
    END
    Should be True     ${no_error}


we then disconnect
    Disconnect

