import subprocess
import unittest
import unittest.mock
from argparse import Namespace
from unittest.mock import patch
from get_ip_addresses import IpAddresses


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.ip_addresses_all = IpAddresses().ip_addresses_all()
        self.ip_addresses_with_prefix = IpAddresses().ip_addresses_with_prefix()
        self.ip_addresses_overlapping = IpAddresses().ip_addresses_overlapping()
        self.get_ip_addresses = IpAddresses().get_ip_addresses()

    @patch('os.system')
    @patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_get_ip_addresses_all(self,
                                  mock_parse,
                                  mock_bash_command):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=False)
        IpAddresses().ip_addresses_all()
        bash_command = "ifconfig | grep" \
                       " -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' |" \
                       " grep -Eo '([0-9]*\.){3}[0-9]*'"
        mock_bash_command.assert_called_once_with(bash_command)

    @unittest.mock.patch('os.system')
    @patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_ip_addresses_with_prefix(self,
                                      mock_parse,
                                      mock_bash_command):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=True)
        IpAddresses().ip_addresses_with_prefix()
        bash_command = "ip -o -f inet addr show | awk '/scope global/ {print $4}'"
        mock_bash_command.assert_called_once_with(bash_command)

    @unittest.mock.patch('os.system')
    @patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_ip_addresses_overlapping(self,
                                      mock_parse,
                                      mock_bash_command):
        mock_parse.return_value = Namespace(overlapping=True, with_prefix=False)
        IpAddresses().ip_addresses_with_prefix()
        bash_command = "ip -o -f inet addr show | awk '/scope global/ {print $4}'"
        mock_bash_command.assert_called_once_with(bash_command)

    @patch('get_ip_addresses.IpAddresses.ip_addresses_all')
    @patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_no_parameters(self,
                              mock_parse,
                              mock_all):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=False)
        mock_all.return_value = "0.0.0.0"
        self.assertEqual("0.0.0.0", IpAddresses().get_ip_addresses())

    @patch('get_ip_addresses.IpAddresses.ip_addresses_all')
    @patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_raise_runtime_error(self,
                                 mock_parse,
                                 mock_all):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=False)
        mock_all.return_value = subprocess.CalledProcessError
        self.assertRaises(RuntimeError, IpAddresses().get_ip_addresses())

    def tearDown(self):
        self.ip_addresses_all = None
        self.ip_addresses_with_prefix = None
        self.ip_addresses_overlapping = None
        self.get_ip_addresses = None

if __name__ == '__main__':
    unittest.main()
