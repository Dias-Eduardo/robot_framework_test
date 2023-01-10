***Settings***
Documentation    Arquivo para testar o envio de pacotes IPv6 com o T-Rex
Library    packet_creator.py

*** Keywords ***
the IPv6 packets are created
    # Pacote da porta 0 
    ${ether}=    Create Ether    ${mac_porta_0}    ${mac_porta_1}
    ${ip}=    Create IPv6    ${ipv6_porta_0}    ${ipv6_porta_1}
    ${dummy_bytes}=    Create Dummy Bytes    ${50}
    ${protocols}=    Create List    ${ether}    ${ip}    ${dummy_bytes}
    ${packet_0}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_0}

    # Pacote da porta 1
    ${ether}=    Create Ether    ${mac_porta_1}    ${mac_porta_0}
    ${ip}=    Create IPv6    ${ipv6_porta_1}    ${ipv6_porta_0}
    ${dummy_bytes}=    Create Dummy Bytes    ${50}
    ${protocols}=    Create List    ${ether}    ${ip}    ${dummy_bytes}
    ${packet_1}=    Assemble Protocols    ${protocols}
    Set Global Variable     ${packet_1}
