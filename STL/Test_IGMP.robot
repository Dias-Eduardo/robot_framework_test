***Settings***
Documentation    Arquivo para testar o envio de pacotes IGMP com o T-Rex
Library    packet_creator.py

*** Keywords ***
the IGMP packets are created
    # Pacote da porta 0 
    ${ether}=    Create Ether    ${mac_porta_0}    ${mac_porta_1}
    ${ip}=    Create IPv4    ${ip_porta_0}    ${ip_porta_1}
    ${igmp}=    Create IGMP    ${0x12}    ${ip_porta_1}
    ${protocols}=     Create List    ${ether}    ${ip}    ${igmp}
    ${packet_0}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_0}

    # Pacote da porta 1
    ${ether}=    Create Ether    ${mac_porta_1}    ${mac_porta_0}
    ${ip}=    Create IPv4    ${ip_porta_1}    ${ip_porta_0}
    ${igmp}=    Create IGMP    ${0x12}    ${ip_porta_1}
    ${protocols}=    Create List    ${ether}    ${ip}    ${igmp}
    ${packet_1}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_1}
