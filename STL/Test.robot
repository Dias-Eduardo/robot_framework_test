***Settings***
Documentation    Arquivo para testar o T-Rex
Library    T-Rex_test.py
Resource   Test_UDP.robot
Resource   Test_ICMP.robot
Resource   Test_DNS.robot
Resource   Test_ARP.robot

*** Variables ***
${mac_porta_0}    d0:00:6a:10:3b:cc
${ip_porta_0}    192.168.50.2


${mac_porta_1}    d0:00:6a:10:36:3b
${ip_porta_1}    192.168.50.3

# Definir a velocidade e duracao de todos os testes | Trocar no futuro para testes terem velocidades e duracoes diferentes?
${velocidade}    ${10000}     # Em pacotes por segundo
${duracao}    ${1000}    # Em segundos


${nome_do_protocolo}     undefined
*** Test Cases ***
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


T-Rex UDP Test
    Given the UDP packets are created
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
    ${lost_packets}=    get_lost_packets    ${nome_do_protocolo}
    ${no_error}=    Set Variable    ${True}
    IF  ${lost_packets} > ${0}
        ${no_error}=    ${False}
    END
    Should be True     ${no_error}


we then disconnect
    Disconnect

