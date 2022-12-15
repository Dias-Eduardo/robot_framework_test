***Settings***
Documentation    Arquivo para testar o envio de pacotes HTTP com o T-Rex
Library    packet_creator.py

*** Variables ***
${duracao_local}    

*** Keywords ***
the ARP packets are created
    # Pacote da porta 0 
    ${ether}=    Create Ether    ${mac_porta_0}    ff:ff:ff:ff:ff:ff
    ${arp}=    Create ARP    192.168.50.2     192.168.50.3   
    ${protocols}=     Create List    ${ether}    ${arp}    
    ${packet_0}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_0}

    # Pacote da porta 1
    ${ether}=    Create Ether    ${mac_porta_1}     ff:ff:ff:ff:ff:ff
    ${arp}=    Create ARP   192.168.50.3    192.168.50.2   
    ${protocols}=    Create List    ${ether}    ${arp}   
    ${packet_1}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_1}

    ${duracao}    Set Variable    ${duracao_local}
    Set Global Variable    ${nome_do_protocolo}
    ${nome_do_protocolo}     Set Variable    ARP
    Set Global Variable    ${nome_do_protocolo}