***Settings***
Documentation    Arquivo para testar o envio de pacotes ICMP com o T-Rex
Library    packet_creator.py



*** Keywords ***
the ICMP packets are created
    # Pacote da porta 0 
    ${ether}=    Create Ether    ${mac_porta_0}    ${mac_porta_1}
    ${ip}=    Create IPv4    ${ip_porta_0}    ${ip_porta_1}
    ${icmp}=    Create ICMP    ${8}    ${0}
    ${protocols}=     Create List    ${ether}    ${ip}    ${icmp}
    ${packet_0}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_0}

    # Pacote da porta 1
    ${ether}=    Create Ether    ${mac_porta_1}    ${mac_porta_0}
    ${ip}=    Create IPv4    ${ip_porta_1}    ${ip_porta_0}
    ${icmp}=    Create ICMP    ${8}    ${0}
    ${protocols}=    Create List    ${ether}    ${ip}    ${icmp}
    ${packet_1}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_1}

    ${nome_do_protocolo}    Set Variable    ICMP
    Set Global Variable    ${nome_do_protocolo}