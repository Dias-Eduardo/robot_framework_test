***Settings***
Documentation    Arquivo para testar o envio de pacotes DNS com o T-Rex
Library    packet_creator.py

*** Keywords ***
the DNS packets are created
    # Pacote da porta 0 
    ${ether}=    Create Ether    ${mac_porta_0}    ${mac_porta_1}
    ${ip}=    Create IPv4    ${ip_porta_0}    ${ip_porta_1}
    ${udp}=    Create UDP    ${1234}    ${53}
    ${dns}=    Create DNS    
    ${protocols}=     Create List    ${ether}    ${ip}    ${udp}    ${dns}
    ${packet_0}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_0}

    # Pacote da porta 1
    ${ether}=    Create Ether    ${mac_porta_1}    ${mac_porta_0}
    ${ip}=    Create IPv4    ${ip_porta_1}    ${ip_porta_0}
    ${udp}=    Create UDP    ${4321}    ${53}
    ${dns}=    Create DNS   
    ${protocols}=    Create List    ${ether}    ${ip}    ${udp}    ${dns}
    ${packet_1}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_1}

    ${nome_do_protocolo}    Set Variable    DNS
    Set Global Variable    ${nome_do_protocolo}
