# pyportscanner
repository to support port scanning in python
Python Port Scanner
A simple, fast, and educational port scanner built in Python. This tool uses multithreading to efficiently scan a range of TCP and UDP ports on a given host.

Features
TCP Scanning: Quickly identify open TCP ports on a target.

UDP Scanning: Detect open or filtered UDP ports.

Multithreaded: Utilizes a thread pool to perform scans concurrently, significantly reducing scan time.

Modular Design: The code is split into logical files (main.py, scanner.py, threaded_scanner.py) for clarity and maintainability.

User-friendly Interface: Simple command-line prompts for target IP, port range, and protocol.

How to Use
Prerequisites
Make sure you have Python 3 installed on your system. No external libraries are needed as this project uses Python's built-in socket and threading modules.

Running the Scanner
Clone the Repository (or download the files).

Navigate to the project directory in your terminal.

Run the script using the following command:

Bash

python main.py
Follow the prompts:

Enter the target IP address or hostname (e.g., 127.0.0.1 or scanme.nmap.org).

Enter the port range (e.g., 1-1024).

Choose the protocol (tcp or udp).

The scanner will then report all open ports it finds.
