***Settings***
Documentation    Arquivo para testar o envio de pacotes ARP com o T-Rex
Library    packet_creator.py

*** Variables ***
${duracao_local}    

*** Keywords ***
the ARP packets are created
    # Pacote da porta 0 
    ${ether}=    Create Ether    ${mac_porta_0}    ff:ff:ff:ff:ff:ff
    ${arp}=    Create ARP    ${ip_porta_0}     ${ip_porta_1}  
    ${protocols}=     Create List    ${ether}    ${arp}    
    ${packet_0}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_0}

    # Pacote da porta 1
    ${ether}=    Create Ether    ${mac_porta_1}     ff:ff:ff:ff:ff:ff
    ${arp}=    Create ARP   ${ip_porta_1}    ${ip_porta_0}  
    ${protocols}=    Create List    ${ether}    ${arp}   
    ${packet_1}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_1}

    ${duracao}    Set Variable    ${duracao_local}
    Set Global Variable    ${nome_do_protocolo}
    ${nome_do_protocolo}     Set Variable    ARP
    Set Global Variable    ${nome_do_protocolo}