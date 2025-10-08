from queue import Queue
from scanner import scan_port

NUMBER_OF_THREADS = 100

port_queue = Queue()

ERROR_CODES = {
    111: "Connection Refused",  # Linux error
    61: "Connection Refused",   # macOS error
    10061: "Connection Refused",# Windows error
    10060: "Timeout",           # Windows error
    113: "No Route to Host"     # General error
}

def worker(target_ip, protocol):
    """
    This is the function that each thread will run.
    It continuously pulls a port from the queue and scans it.
    """
    while True:
        port = port_queue.get()
        result = scan_port(target_ip, port, protocol)

        if protocol.lower() == 'tcp':
            if result == 0:
                print(f"TCP Port {port} is open")
            else:
                error_description = ERROR_CODES.get(result, "Unknown Error")
                print(f"TCP Port {port} is closed ({error_description})")
        
        elif protocol.lower() == 'udp':
            if result:
                print(f"UDP Port {port} is open or filtered")

        port_queue.task_done()

def start_threaded_scan(target_ip, start_port, end_port, protocol):
    """
    Sets up the threads and starts the scanning process.
    """
    for port in range(start_port, end_port + 1):
        port_queue.put(port)
        
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker, args=(target_ip, protocol,), daemon=True)
        thread.start()
    
    port_queue.join()
