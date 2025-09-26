import socket
import sys

def scan_port(target_ip, port):
    """
    Attempts to connect to a specific port on the target IP.

    Args:
        target_ip (str): The IP address or hostname to scan.
        port (int): The port number to check.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            print(f"Port {port} is open")
        
        s.close()
        
    except socket.gaierror:
        print(f"Hostname could not be resolved.")
        sys.exit() 
    except socket.error:
        print(f"Could not connect to the server.")
        sys.exit()
