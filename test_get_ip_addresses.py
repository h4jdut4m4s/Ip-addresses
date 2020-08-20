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
        self.class_instance = IpAddresses()

    @unittest.mock.patch('os.system')
    @patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_get_ip_addresses(self,
                              mock_parse,
                              mock_bash_command):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=False)
        command_output = "100.109.0.2" \
                         "127.0.0.1" \
                         "192.168.0.6"

        mock_bash_command.return_value = command_output
        expected_result = self.ip_addresses_all
        self.assertEqual(expected_result, command_output)

    @unittest.mock.patch('os.system')
    @patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_ip_addresses_with_prefix(self,
                                      mock_parse,
                                      mock_bash_command):

        mock_parse.return_value = Namespace(overlapping=False, with_prefix=True)
        command_output = "100.109.0.2" \
                         "127.0.0.1" \
                         "192.168.0.6"

        mock_bash_command.return_value = command_output
        expected_result = self.ip_addresses_with_prefix
        self.assertEqual(expected_result, command_output)

    @unittest.mock.patch('os.system')
    @patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_ip_addresses_overlapping(self,
                                      mock_parse,
                                      mock_bash_command):

        mock_parse.return_value = Namespace(overlapping=True, with_prefix=False)
        command_output = "100.109.0.2" \
                         "127.0.0.1" \
                         "192.168.0.6"

        mock_bash_command.return_value = command_output
        expected_result = self.ip_addresses_overlapping
        self.assertEqual(expected_result, command_output)


if __name__ == '__main__':
    unittest.main()
