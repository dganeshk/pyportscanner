import threading
from queue import Queue
from scanner import scan_port

NUMBER_OF_THREADS = 100

port_queue = Queue()

def worker(target_ip):
    """
    This is the function that each thread will run.
    It continuously pulls a port from the queue and scans it.
    """
    while True:
        port = port_queue.get()
        scan_port(target_ip, port)
        port_queue.task_done()

def start_threaded_scan(target_ip, start_port, end_port):
    """
    Sets up the threads and starts the scanning process.

    Args:
        target_ip (str): The IP address to scan.
        start_port (int): The first port in the range.
        end_port (int): The last port in the range.
    """
    for port in range(start_port, end_port + 1):
        port_queue.put(port)
        
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker, args=(target_ip,), daemon=True)
        thread.start()
    
    port_queue.join()
