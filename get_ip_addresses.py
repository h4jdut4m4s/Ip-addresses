#!/usr/bin/env python3

import argparse
import os
import subprocess

"""
    Script to get all IP addresses.
    --with-prefix prints all the addresses with the appropriate subnets
    --overlapping prints the overlapping subnets from the IP addresses
"""


class IpAddresses:

    def get_ip_addresses(self):
        args = self.parse_arguments()
        if args.overlapping:
            return self.ip_addresses_overlapping()
        elif args.with_prefix:
            return self.ip_addresses_with_prefix()
        else:
            return self.ip_addresses_all()

    def ip_addresses_all(self):
        '''
        Getting all the IPs.
        '''
        ip_addresses_all = os.system("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' |"
                                     " grep -Eo '([0-9]*\.){3}[0-9]*'")
        return ip_addresses_all

    def ip_addresses_with_prefix(self):
        '''
        Getting the list of IP addresses, with subnets.
        '''
        ip_addresses_with_subnet = os.system("ip -o -f inet addr show | awk '/scope global/ {print $4}'")
        return ip_addresses_with_subnet

    def ip_addresses_overlapping(self):
        '''
        Getting the list of IP addresses, then printing the overlapping addresses
        '''
        ip_addresses = subprocess.check_output("ip -o -f inet addr show | awk '/scope global/ {print $4}'", shell=True)
        addresses_string_parameter = ' '.join(ip_addresses.decode("utf-8").split('\n'))
        overlapping_ips = os.system("ipconflict -o " + addresses_string_parameter)
        return overlapping_ips

    def parse_arguments(self):
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
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    ip_adresses = IpAddresses()
    ip_adresses.get_ip_addresses()
