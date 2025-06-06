# # File: utils.py

# import ipaddress

# def longest_prefix_match(dst_ip, routing_table):
#     """
#     Finds the longest prefix match for a destination IP
#     in the routing table.

#     Parameters:
#         dst_ip (str): Destination IP (e.g., "22.22.22.40")
#         routing_table (dict): { subnet (str): (next_hop, interface) }

#     Returns:
#         tuple: (matched_subnet, (next_hop, interface)) or None
#     """
#     ip = ipaddress.IPv4Address(dst_ip)
#     best_match = None
#     max_prefix_len = -1

#     for subnet_str, route in routing_table.items():
#         network = ipaddress.IPv4Network(subnet_str, strict=False)
#         if ip in network:
#             if network.prefixlen > max_prefix_len:
#                 best_match = (subnet_str, route)
#                 max_prefix_len = network.prefixlen

#     return best_match


import ipaddress

def longest_prefix_match(ip_str, routing_table):
    dst_ip = ipaddress.IPv4Address(ip_str)
    best_match = None
    max_prefix = -1

    for network_str in routing_table:
        network = ipaddress.IPv4Network(network_str)
        if dst_ip in network and network.prefixlen > max_prefix:
            best_match = (network_str, routing_table[network_str])
            max_prefix = network.prefixlen
    return best_match
