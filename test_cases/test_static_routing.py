# # File: test_cases/test_static_routing.py

# from models.router import Router
# from models.switch import Switch
# from models.host import Host
# from network.interface import Interface

# print("\n=== [STATIC ROUTING DEMO: Host A → Host D] ===")

# # Setup Devices
# host_a = Host("A")
# host_a.configure_interface("11.11.11.10", "aaaa")

# host_d = Host("D")
# host_d.configure_interface("22.22.22.40", "dddd")

# router = Router("R")
# iface1 = router.add_interface("11.11.11.1", "ee01")
# iface2 = router.add_interface("22.22.22.1", "ee02")
# router.add_static_route("11.11.11.0/24", None, iface1)
# router.add_static_route("22.22.22.0/24", None, iface2)

# # Setup Switches
# sw_x = Switch("X")
# sw_y = Switch("Y")
# sw_x.add_interface(host_a.interfaces[0])
# sw_x.add_interface(iface1)
# sw_y.add_interface(host_d.interfaces[0])
# sw_y.add_interface(iface2)

# # Run ARP
# print("\n[Step 1] Host A ARPs for Router (11.11.11.1)")
# host_a.send_arp_request("11.11.11.1", sw_x)

# print("\n[Step 2] Host A sends data to Host D")
# host_a.send_packet("22.22.22.40", "Hello, D!", sw_x, "11.11.11.1")

# # Print Tables
# host_a.show_arp_table()
# router.show_arp_table()
# router.show_routing_table()


# File: test_cases/test_static_routing.py

# from models.host import Host
# from models.router import Router
# from models.switch import Switch
# from network.interface import Interface

# print("\n=== [STATIC ROUTING DEMO: Host A → Host D] ===")

# # Step 1: Initialize Hosts
# host_a = Host("A")
# iface_a = host_a.configure_interface("11.11.11.10", "aaaa")

# host_d = Host("D")
# iface_d = host_d.configure_interface("22.22.22.40", "dddd")

# # Step 2: Initialize Router
# router = Router("R")
# iface_r1 = router.add_interface("11.11.11.1", "ee01")  # to Subnet 1
# iface_r2 = router.add_interface("22.22.22.1", "ee02")  # to Subnet 2

# # Add Static Routes
# router.add_static_route("11.11.11.0/24", None, iface_r1)
# router.add_static_route("22.22.22.0/24", None, iface_r2)

# # Step 3: Initialize Switches
# sw_x = Switch("X")
# sw_y = Switch("Y")

# # Step 4: Connect Interfaces to Switches
# sw_x.add_interface(iface_a); iface_a.port = 2
# sw_x.add_interface(iface_r1); iface_r1.port = 3

# sw_y.add_interface(iface_d); iface_d.port = 5
# sw_y.add_interface(iface_r2); iface_r2.port = 4

# # Step 5: ARP Resolution for Host A → Router
# print("\n[Step 1] Host A ARPs for Router (11.11.11.1)")
# host_a.send_arp_request("11.11.11.1", sw_x)

# # Step 6: Host A Sends Data to Host D
# print("\n[Step 2] Host A sends data to Host D")
# host_a.send_packet("22.22.22.40", "Hello, D!", sw_x, "11.11.11.1")

# # Step 7: Router Processes and Forwards
# # This occurs in Router.receive_packet(), already handled in routing logic

# # Final Tables
# print("\n✅ Final Tables")
# host_a.show_arp_table()
# host_d.show_arp_table()
# router.show_arp_table()
# sw_x.show_mac_table()
# sw_y.show_mac_table()
# router.show_routing_table()


# File: test_cases/test_static_routing.py

from models.router import Router
from models.switch import Switch
from models.host import Host
from utils.longest_prefix_match import longest_prefix_match

print("\n=== [STATIC ROUTING DEMO: Host A → Host D] ===")

# Setup Hosts
host_a = Host("A"); host_a.configure_interface("11.11.11.10", "aaaa")
host_d = Host("D"); host_d.configure_interface("22.22.22.40", "dddd")

# Setup Router
router = Router("R")
eth0 = router.add_interface("11.11.11.1", "ee01")  # To Host A
eth1 = router.add_interface("22.22.22.1", "ee02")  # To Host D

# Static Routing Table Entries
router.add_static_route("11.11.11.0/24", None, eth0)
router.add_static_route("22.22.22.0/24", None, eth1)

# Setup Switches
sw_x = Switch("X")
sw_y = Switch("Y")

sw_x.add_interface(host_a.interfaces[0])
sw_x.add_interface(eth0)

sw_y.add_interface(host_d.interfaces[0])
sw_y.add_interface(eth1)

# STEP 1: A ARPs for router
print("\n[Step 1] Host A ARPs for Router (11.11.11.1)\n")
host_a.send_arp_request("11.11.11.1", sw_x)

# STEP 2: A sends data to D
print("\n[Step 2] Host A sends data to Host D\n")
host_a.send_packet("22.22.22.40", "Hello, D!", sw_x, gateway_ip="11.11.11.1")

# STEP 3: Router routes to D (via eth1)
print("\n[Step 3] Router forwards packet to Host D\n")
router.receive_packet("22.22.22.40", "Hello, D!", eth0)

# STEP 4: Host D ARPs for Router
print("\n[Step 4] Host D ARPs for Router (22.22.22.1)\n")
host_d.send_arp_request("22.22.22.1", sw_y)

# STEP 5: D replies back to A
print("\n[Step 5] Host D sends reply to Host A\n")
host_d.send_packet("11.11.11.10", "Reply to A!", sw_y, gateway_ip="22.22.22.1")

# STEP 6: Router delivers to A
print("\n[Step 6] Router forwards reply to Host A\n")
router.receive_packet("11.11.11.10", "Reply to A!", eth1)
print("\n======================")
print("  ✅ FINAL TABLE DUMPS")
print("======================")

host_a.show_arp_table()
host_d.show_arp_table()
router.show_arp_table()
sw_x.show_mac_table()
sw_y.show_mac_table()
router.show_routing_table()
router.show_interfaces()

