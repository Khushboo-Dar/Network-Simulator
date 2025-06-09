# File: utils/ip_allocator.py

import ipaddress

class IPAllocator:
    def __init__(self, cidr_block):
        self.network = ipaddress.IPv4Network(cidr_block, strict=False)
        self.hosts = self.network.hosts()
        self.allocated = []

    def next_ip(self):
        try:
            ip = next(self.hosts)
            self.allocated.append(str(ip))
            return str(ip)
        except StopIteration:
            raise Exception("No more available IPs in the subnet")

    def show_allocated(self):
        print("\n[ALLOCATED IP ADDRESSES]")
        for ip in self.allocated:
            print(ip)
