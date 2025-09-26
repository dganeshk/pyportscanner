import sys
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

def main():
    """Main function to run the port scanner."""
    print("-" * 50)
    print("Simple Threaded Port Scanner")
    print("-" * 50)

    target_ip = get_target()
    start_port, end_port = get_port_range()

    print(f"\nScanning ports on {target_ip} from {start_port} to {end_port}...")

    start_threaded_scan(target_ip, start_port, end_port)
    print("\nScan completed.")

if __name__ == "__main__":
    main()
