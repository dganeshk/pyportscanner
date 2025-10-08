import socket
import sys

def scan_port(target_ip, port, protocol='tcp'):
    """
    Attempts to connect to a specific port on the target IP.

    Args:
        target_ip (str): The IP address or hostname to scan.
        port (int): The port number to check.
        protocol (str): The protocol to use ('tcp' or 'udp').
    """
    try:
        if protocol.lower() == 'tcp':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                print(f"TCP Port {port} is open")
            s.close()
        elif protocol.lower() == 'udp':
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(5)
            try:
                s.sendto(b'ping', (target_ip, port))
                s.recvfrom(1024)
            except socket.timeout:
                print(f"UDP Port {port} is open or filtered")
            s.close()
        else:
            print(f"Invalid protocol: {protocol}. Please choose 'tcp' or 'udp'.")

    except socket.gaierror:
        print(f"Hostname could not be resolved.")
        sys.exit() 
    except socket.error:
        print(f"Could not connect to the server.")
        sys.exit()
