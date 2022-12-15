***Settings***
Documentation    Arquivo para testar o T-Rex
Library    profile_configurator.py


*** Keywords ***
the HTTP comunication is configured
    http_config_file    ${ip_porta_0}    ${ip_porta_1}
    ${profile_name}    Set Variable   http_simple.py
    Set Global Variable     ${profile_name}

