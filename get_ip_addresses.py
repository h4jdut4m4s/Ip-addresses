#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

"""
    Script to get all IP addresses.
    --with-prefix prints all the addresses with the appropriate subnets
    --overlapping prints the overlapping subnets from the IP addresses
"""

IPS_WITH_PREFIX = "ip -o -f inet addr show | awk '/scope global/ {print $4}'"
IPS_ALL = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*'"

class IpAddresses:

    def get_ip_addresses(self):
        '''
        The main function to execute. If one of the shell commands fails to execute, the programs throws
        a RuntimeError exception.
        '''
        args = self.parse_arguments(sys.argv[1:])
        try:
            if args.overlapping:
                return self.ip_addresses_overlapping()
            elif args.with_prefix:
                return self.ip_addresses_with_prefix()
            else:
                return self.ip_addresses_all()
        except subprocess.CalledProcessError as ex:
            raise RuntimeError(f"Failed to execute bash command: {ex}")

    def ip_addresses_all(self):
        '''
        Getting all the IPs.
        '''
        ip_addresses_all = os.system(IPS_ALL)
        return ip_addresses_all

    def ip_addresses_with_prefix(self):
        '''
        Getting the list of IP addresses, with subnets.
        '''
        ip_addresses_with_subnet = os.system(IPS_WITH_PREFIX)
        return ip_addresses_with_subnet

    def ip_addresses_overlapping(self):
        '''
        Getting the list of IP addresses, then printing the overlapping addresses
        '''
        ip_addresses = subprocess.check_output(IPS_WITH_PREFIX, shell=True)
        addresses_string_parameter = ' '.join(ip_addresses.decode("utf-8").split('\n'))
        overlapping_ips = os.system("ipconflict -o " + addresses_string_parameter)
        return overlapping_ips

    def parse_arguments(self,
                        args):
        parser = argparse.ArgumentParser(
            prog="get_ip_addresses",
            usage=None,
            description="""
                Script to get all IP addresses.
                --with-prefix prints all the addresses with the appropriate subnets
                --overlapping prints the overlapping subnets from the IP addresses
            """,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        parser.add_argument(
            "--with-prefix",
            action='store_true'
        )
        parser.add_argument(
            "--overlapping",
            action='store_true'
        )
        args = parser.parse_args(args)
        return args


if __name__ == "__main__":
    ip_adresses = IpAddresses()
    ip_adresses.get_ip_addresses()
