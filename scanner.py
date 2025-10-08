import socket
import sys

def scan_port(target_ip, port, protocol='tcp'):
    """
    Attempts to connect to a specific port on the target IP.
    Returns the connect_ex error code for TCP, a boolean for UDP.

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
            s.close()
            return result

        elif protocol.lower() == 'udp':
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            try:
                s.sendto(b'ping', (target_ip, port))
                s.recvfrom(1024)
                s.close()
                return False
            except socket.timeout:
                s.close()
                return True
            except ConnectionResetError:
                s.close()
                return False
        else:
            print(f"Invalid protocol: {protocol}. Please choose 'tcp' or 'udp'.")
            return -1

    except socket.gaierror:
        print(f"Hostname could not be resolved.")
        sys.exit()
    except socket.error:
        print(f"Could not connect to the server.")
        sys.exit()
