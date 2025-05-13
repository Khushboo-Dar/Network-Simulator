# File: test_cases/test_static_routing.py

from models.router import Router
from models.switch import Switch
from models.host import Host
from network.interface import Interface

print("\n=== [STATIC ROUTING DEMO: Host A → Host D] ===")

# Setup Devices
host_a = Host("A")
host_a.configure_interface("11.11.11.10", "aaaa")

host_d = Host("D")
host_d.configure_interface("22.22.22.40", "dddd")

router = Router("R")
iface1 = router.add_interface("11.11.11.1", "ee01")
iface2 = router.add_interface("22.22.22.1", "ee02")
router.add_static_route("11.11.11.0/24", None, iface1)
router.add_static_route("22.22.22.0/24", None, iface2)

# Setup Switches
sw_x = Switch("X")
sw_y = Switch("Y")
sw_x.add_interface(host_a.interfaces[0])
sw_x.add_interface(iface1)
sw_y.add_interface(host_d.interfaces[0])
sw_y.add_interface(iface2)

# Run ARP
print("\n[Step 1] Host A ARPs for Router (11.11.11.1)")
host_a.send_arp_request("11.11.11.1", sw_x)

print("\n[Step 2] Host A sends data to Host D")
host_a.send_packet("22.22.22.40", "Hello, D!", sw_x, "11.11.11.1")

# Print Tables
host_a.show_arp_table()
router.show_arp_table()
router.show_routing_table()
