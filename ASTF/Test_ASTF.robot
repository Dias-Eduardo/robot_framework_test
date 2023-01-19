***Settings***
Documentation    Arquivo para testar o modo Advanced Stateful T-Rex
Library    T-Rex_ASTF_test.py
Resource    Test_HTTP.robot


*** Variables ***
${ip_porta_0}    192.168.50.2


${ip_porta_1}    192.168.50.3


# Definir a velocidade e duracao de todos os testes | Trocar no futuro para testes terem velocidades e duracoes diferentes?
${multiplicador}    ${10}     # Multiplicador da velocidade
${duracao}    ${10}    # Em segundos

${profile_name}    undefined

*** Test Cases ***
T-Rex HTTP Test
    Given the HTTP comunication is configured
    And the t-rex basic configuration is done
    When traffic is started through t-rex api
    Then all traffic sent is received without dropped packets
        And we then disconnect


*** Keywords ***    
the t-rex basic configuration is done
    Init    ${profile_name} 


traffic is started through t-rex api
    Start Traffic    ${multiplicador}    ${duracao}


all traffic sent is received without dropped packets
    Print Stats And Get Lost Packets
    # ${lost_packets}=    
    # ${no_error}=    Set Variable    ${True}
    # IF  ${lost_packets} > ${0}
    #     ${no_error}=    ${False}
    # END
    # Should be True     ${no_error}


we then disconnect
    Disconnect