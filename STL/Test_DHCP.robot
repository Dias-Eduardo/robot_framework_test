***Settings***
Documentation    Arquivo para testar o envio de pacotes DHCP com o T-Rex
Library    packet_creator.py  

*** Keywords ***
the DHCP packets are created
    # Pacote da porta 0 
    ${ether}=    Create Ether    ${mac_porta_0}    ${mac_porta_1}
    ${ip}=    Create IPv4    ${ip_porta_0}    ${ip_porta_1}
    ${udp}=    Create UDP    ${67}    ${68}
    ${bootp}=    Create BOOTP   ${mac_porta_0}
    ${dhcp}=    Create DHCP    
    ${protocols}=     Create List    ${ether}    ${ip}    ${udp}  ${bootp}  ${dhcp}
    ${packet_0}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_0}

    # Pacote da porta 1
    ${ether}=    Create Ether    ${mac_porta_1}    ${mac_porta_0}
    ${ip}=    Create IPv4    ${ip_porta_1}    ${ip_porta_0}
    ${udp}=    Create UDP    ${67}    ${68}
    ${bootp}=    Create BOOTP   ${mac_porta_1}
    ${dhcp}=    Create DHCP  
    ${protocols}=    Create List    ${ether}    ${ip}    ${udp}  ${bootp}  ${dhcp}
    ${packet_1}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_1}