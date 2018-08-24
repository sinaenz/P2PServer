# P2PServer
A TCP based P2P server


--- register as a gateway ---

send    b'GG,gateway-id'    to   gilsatech.com:8080

--- connect as a mobile (send commands to gateway) ---

send    b'GM,gateway-id,mobile-id,command'    to    gilsatech.com:8080
