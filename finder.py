from scanner import scan_port

def find_first_open_port(target_ip, start_port, end_port, protocol='tcp'):
    """
    Finds the first open port in a given range.

    Args:
        target_ip (str): The IP address or hostname to scan.
        start_port (int): The first port in the range.
        end_port (int): The last port in the range.
        protocol (str): The protocol to use ('tcp' or 'udp').

    Returns:
        int or None: The first open port number found, or None if no open ports are found.
    """
    print(f"Finding the first open {protocol.upper()} port on {target_ip} from {start_port} to {end_port}...")
    for port in range(start_port, end_port + 1):
        if scan_port(target_ip, port, protocol):
            print(f"\nFound first open port: {port}")
            return port
    
    print("\nNo open ports found in the specified range.")
    return None
