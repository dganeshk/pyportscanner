import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import socket

# This adds the project's root directory to the system path,
# allowing us to import our modules for testing.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import get_target, get_port_range
from scanner import scan_port
from threaded_scanner import start_threaded_scan

class TestPortScanner(unittest.TestCase):
    
    # Test cases for main.py (input validation)
    @patch('builtins.input', side_effect=['example.com'])
    def test_get_target_valid_input(self, mock_input):
        target = get_target()
        self.assertEqual(target, 'example.com')

    @patch('builtins.input', side_effect=['', '127.0.0.1'])
    def test_get_target_invalid_then_valid(self, mock_input):
        target = get_target()
        self.assertEqual(target, '127.0.0.1')

    @patch('builtins.input', side_effect=['1-1024'])
    def test_get_port_range_valid(self, mock_input):
        start, end = get_port_range()
        self.assertEqual(start, 1)
        self.assertEqual(end, 1024)

    @patch('builtins.input', side_effect=['not-a-range', '1-1024'])
    def test_get_port_range_invalid_format(self, mock_input):
        start, end = get_port_range()
        self.assertEqual(start, 1)
        self.assertEqual(end, 1024)

    @patch('builtins.input', side_effect=['65536-65537', '100-99', '1-10'])
    def test_get_port_range_invalid_values(self, mock_input):
        start, end = get_port_range()
        self.assertEqual(start, 1)
        self.assertEqual(end, 10)
        
    # Test cases for scanner.py
    
    # TCP Tests
    @patch('socket.socket')
    def test_scan_port_tcp_open(self, mock_socket):
        """Test that scan_port correctly identifies an open TCP port."""
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.return_value = 0
        
        with patch('builtins.print') as mock_print:
            scan_port('127.0.0.1', 80, protocol='tcp')
            mock_print.assert_called_with('TCP Port 80 is open')
            mock_instance.close.assert_called_once()
            
    @patch('socket.socket')
    def test_scan_port_tcp_closed(self, mock_socket):
        """Test that scan_port correctly handles a closed TCP port."""
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.return_value = 111
        
        with patch('builtins.print') as mock_print:
            scan_port('127.0.0.1', 81, protocol='tcp')
            mock_print.assert_not_called()
            mock_instance.close.assert_called_once()

    # UDP Tests
    @patch('socket.socket')
    def test_scan_port_udp_open_or_filtered(self, mock_socket):
        """Test that scan_port correctly identifies an open or filtered UDP port."""
        mock_instance = mock_socket.return_value
        # For UDP, a timeout means the port is likely open or filtered.
        mock_instance.recvfrom.side_effect = socket.timeout
        
        with patch('builtins.print') as mock_print:
            scan_port('127.0.0.1', 53, protocol='udp')
            mock_print.assert_called_with('UDP Port 53 is open or filtered')
            mock_instance.close.assert_called_once()
            
    @patch('socket.socket')
    def test_scan_port_udp_closed(self, mock_socket):
        """Test that scan_port correctly identifies a closed UDP port."""
        mock_instance = mock_socket.return_value
        # A closed UDP port will typically return an ICMP error, which
        # appears as a ConnectionResetError in Python.
        mock_instance.recvfrom.side_effect = ConnectionResetError
        
        with patch('builtins.print') as mock_print:
            scan_port('127.0.0.1', 54, protocol='udp')
            mock_print.assert_not_called()
            mock_instance.close.assert_called_once()
    
    # Test cases for threaded_scanner.py
    @patch('threaded_scanner.scan_port')
    def test_start_threaded_scan_tcp(self, mock_scan_port):
        """Test that the threaded scanner processes all TCP ports."""
        target_ip = '127.0.0.1'
        start_port = 1
        end_port = 50
        
        start_threaded_scan(target_ip, start_port, end_port, protocol='tcp')
        
        self.assertEqual(mock_scan_port.call_count, (end_port - start_port + 1))
        
        calls = mock_scan_port.call_args_list
        ports_scanned = {call[0][1] for call in calls}
        
        expected_ports = set(range(start_port, end_port + 1))
        self.assertEqual(ports_scanned, expected_ports)

    @patch('threaded_scanner.scan_port')
    def test_start_threaded_scan_udp(self, mock_scan_port):
        """Test that the threaded scanner processes all UDP ports."""
        target_ip = '127.0.0.1'
        start_port = 1
        end_port = 50
        
        start_threaded_scan(target_ip, start_port, end_port, protocol='udp')
        
        self.assertEqual(mock_scan_port.call_count, (end_port - start_port + 1))
        
        calls = mock_scan_port.call_args_list
        ports_scanned = {call[0][1] for call in calls}
        
        expected_ports = set(range(start_port, end_port + 1))
        self.assertEqual(ports_scanned, expected_ports)

    @patch('finder.scan_port')
    def test_find_first_open_port(self, mock_scan_port):
        """
        Tests that find_first_open_port correctly finds the first open port
        and stops scanning.
        """
        # Scenario 1: Open port is found
        # The mock will return False for the first 4 ports, and True for the 5th.
        mock_scan_port.side_effect = [False, False, False, False, True]
        
        target = '127.0.0.1'
        start_port = 1
        end_port = 10
        
        # We expect the function to return the 5th port in the range (which is port 5)
        # and to stop after finding it.
        result = find_first_open_port(target, start_port, end_port, 'tcp')
        
        self.assertEqual(result, 5)
        # Assert that scan_port was called exactly 5 times (for ports 1 through 5)
        self.assertEqual(mock_scan_port.call_count, 5)

        # Reset the mock for the next scenario
        mock_scan_port.reset_mock()

        # Scenario 2: No open port is found
        # The mock will always return False.
        mock_scan_port.side_effect = [False] * 10
        
        result = find_first_open_port(target, start_port, end_port, 'tcp')
        
        self.assertIsNone(result)
        # Assert that scan_port was called for all 10 ports in the range
        self.assertEqual(mock_scan_port.call_count, 10)


if __name__ == '__main__':
    unittest.main()
