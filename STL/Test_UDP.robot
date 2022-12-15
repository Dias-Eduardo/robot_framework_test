***Settings***
Documentation    Arquivo para testar o envio de pacotes UDP com o T-Rex
Library    packet_creator.py

*** Keywords ***
the UDP packets are created
    # Pacote da porta 0 
    ${ether}=    Create Ether    ${mac_porta_0}    ${mac_porta_1}
    ${ip}=    Create IPv4    ${ip_porta_0}    ${ip_porta_1}
    ${udp}=    Create UDP    ${1234}    ${4321}
    ${protocols}=     Create List    ${ether}    ${ip}    ${udp}
    ${packet_0}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_0}

    # Pacote da porta 1
    ${ether}=    Create Ether    ${mac_porta_1}    ${mac_porta_0}
    ${ip}=    Create IPv4    ${ip_porta_1}    ${ip_porta_0}
    ${udp}=    Create UDP    ${4321}    ${1234}
    ${protocols}=    Create List    ${ether}    ${ip}    ${udp}
    ${packet_1}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_1}

    ${nome_do_protocolo}    Set Variable    UDP
    Set Global Variable    ${nome_do_protocolo}
