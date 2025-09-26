import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import get_target, get_port_range
from scanner import scan_port
from threaded_scanner import start_threaded_scan

class TestPortScanner(unittest.TestCase):
    
    # Test cases for main.py
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
    @patch('socket.socket')
    def test_scan_port_open(self, mock_socket):
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.return_value = 0
        
        with patch('builtins.print') as mock_print:
            scan_port('127.0.0.1', 80)
            mock_print.assert_called_with('Port 80 is open')
            mock_instance.close.assert_called_once()
            
    @patch('socket.socket')
    def test_scan_port_closed(self, mock_socket):
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.return_value = 111
        
        with patch('builtins.print') as mock_print:
            scan_port('127.0.0.1', 81)
            mock_print.assert_not_called()
            mock_instance.close.assert_called_once()
    
    # Test cases for threaded_scanner.py
    @patch('threaded_scanner.scan_port')
    def test_start_threaded_scan(self, mock_scan_port):
        target_ip = '127.0.0.1'
        start_port = 1
        end_port = 50
        
        start_threaded_scan(target_ip, start_port, end_port)
        
        self.assertEqual(mock_scan_port.call_count, (end_port - start_port + 1))
        
        calls = mock_scan_port.call_args_list
        ports_scanned = {call[0][1] for call in calls}
        
        expected_ports = set(range(start_port, end_port + 1))
        self.assertEqual(ports_scanned, expected_ports)

if __name__ == '__main__':
    unittest.main()
