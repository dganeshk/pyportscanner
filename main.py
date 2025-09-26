import sys
import time
from threaded_scanner import start_threaded_scan

def get_target():
    """Prompts the user for the target IP address."""
    while True:
        target = input("Enter the target IP address or hostname: ")
        if target:
            return target
        print("Invalid input. Please enter a valid IP or hostname.")

def get_port_range():
    """Prompts the user for a port range (e.g., 1-1024)."""
    while True:
        port_range_str = input("Enter the port range to scan (e.g., 1-1024): ")
        try:
            start_port_str, end_port_str = port_range_str.split('-')
            start_port = int(start_port_str)
            end_port = int(end_port_str)
            
            if 0 < start_port <= end_port <= 65535:
                return start_port, end_port
            else:
                print("Invalid port range. Ports must be between 1 and 65535, and the start port must be less than or equal to the end port.")
        except ValueError:
            print("Invalid format. Please enter the range like '1-1024'.")

def get_protocol():
    """Prompts the user to choose a protocol for scanning."""
    while True:
        protocol = input("Enter the protocol to scan (tcp or udp): ").lower()
        if protocol in ['tcp', 'udp']:
            return protocol
        print("Invalid protocol. Please enter 'tcp' or 'udp'.")

def main():
    """Main function to run the port scanner."""
    print("-" * 50)
    print("Simple Threaded Port Scanner")
    print("-" * 50)

    target_ip = get_target()
    start_port, end_port = get_port_range()
    protocol = get_protocol()

    print(f"\nScanning {protocol.upper()} ports on {target_ip} from {start_port} to {end_port}...")
    start_time = time.time()
    start_threaded_scan(target_ip, start_port, end_port, protocol)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nScan completed in {total_time:.2f} seconds.")

if __name__ == "__main__":
    main()