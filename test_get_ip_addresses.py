import argparse
import subprocess
import unittest.mock
from argparse import Namespace
from get_ip_addresses import IpAddresses


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.ip_addresses_all = IpAddresses().ip_addresses_all()
        self.ip_addresses_with_prefix = IpAddresses().ip_addresses_with_prefix()
        self.ip_addresses_overlapping = IpAddresses().ip_addresses_overlapping()
        self.maxDiff = None

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_get_ip_addresses_all(self,
                                  mock_parse,
                                  mock_bash_command):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=False)
        IpAddresses().ip_addresses_all()
        bash_command = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*'"
        mock_bash_command.assert_called_once_with(bash_command)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_ip_addresses_with_prefix(self,
                                      mock_parse,
                                      mock_bash_command):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=True)
        IpAddresses().ip_addresses_with_prefix()
        bash_command = "ip -o -f inet addr show | awk '/scope global/ {print $4}'"
        mock_bash_command.assert_called_once_with(bash_command)
        
    @unittest.mock.patch('os.system')
    @unittest.mock.patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_ip_addresses_overlapping(self,
                                      mock_parse,
                                      mock_bash_command):
        mock_parse.return_value = Namespace(overlapping=True, with_prefix=False)
        ips_with_prefix = subprocess.check_output("ip -o -f inet addr show | awk '/scope global/ {print $4}'",
                                                  shell=True)
        command_arguments = ' '.join(ips_with_prefix.decode("utf-8").split('\n'))
        IpAddresses().ip_addresses_overlapping()
        bash_command = f"ipconflict -o {command_arguments}"
        mock_bash_command.assert_called_once_with(bash_command)

    @unittest.mock.patch('get_ip_addresses.IpAddresses.ip_addresses_all')
    @unittest.mock.patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_no_parameters_called(self,
                                  mock_parse,
                                  mock_all):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=False)
        mock_all.return_value = "0.0.0.0"
        self.assertEqual("0.0.0.0", IpAddresses().get_ip_addresses())

    @unittest.mock.patch('get_ip_addresses.IpAddresses.ip_addresses_with_prefix')
    @unittest.mock.patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_with_prefix_called(self,
                                mock_parse,
                                mock_prefix):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=True)
        mock_prefix.return_value = "0.0.0.0"
        self.assertEqual("0.0.0.0", IpAddresses().get_ip_addresses())

    @unittest.mock.patch('get_ip_addresses.IpAddresses.ip_addresses_overlapping')
    @unittest.mock.patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_overlapping_called(self,
                                mock_parse,
                                mock_prefix):
        mock_parse.return_value = Namespace(overlapping=True, with_prefix=False)
        mock_prefix.return_value = "0.0.0.0"
        self.assertEqual("0.0.0.0", IpAddresses().get_ip_addresses())

    @unittest.mock.patch('get_ip_addresses.IpAddresses.ip_addresses_all')
    @unittest.mock.patch('get_ip_addresses.IpAddresses.parse_arguments')
    def test_raise_runtime_error(self,
                                 mock_parse,
                                 mock_all):
        mock_parse.return_value = Namespace(overlapping=False, with_prefix=False)
        mock_all.side_effect = subprocess.CalledProcessError(returncode=2, cmd=["bad"])
        self.assertRaises(RuntimeError, IpAddresses().get_ip_addresses)

    def test_parser(self):
        parser = IpAddresses().parse_arguments(args=["--with-prefix", "--overlapping"])
        self.assertTrue(parser)

    def tearDown(self):
        self.ip_addresses_all = None
        self.ip_addresses_with_prefix = None
        self.ip_addresses_overlapping = None
        self.get_ip_addresses = None


if __name__ == '__main__':
    unittest.main()
