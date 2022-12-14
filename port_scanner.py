import sys
import socket
from concurrent.futures import ThreadPoolExecutor

if len(sys.argv) < 2:
    print("Usage: port_scanner.py [IP]")

ip = sys.argv[1]
open_ports =[] 

ports = range(1, 65535)


def probe_port(ip, port, result = 1): 
  try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.settimeout(0.5) 
    r = sock.connect_ex((ip, port))   
    if r == 0: 
      result = r 
    sock.close() 
  except Exception as e: 
    pass 
  return result

with ThreadPoolExecutor(len(ports)) as executor:
    results = executor.map(probe_port, [ip]*len(ports), ports)

    for port,response in zip(ports,results):
        if response == 0:
            print(f'Port {port} is open')
    