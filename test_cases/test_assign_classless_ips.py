# File: test_cases/test_assign_classless_ips.py

from models.router import Router
from models.host import Host
from utils.ip_allocator import IPAllocator

print("=== [Test] Classless IPv4 Assignment to Routers + Hosts ===")

num_routers = int(input("Enter number of routers: "))
num_hosts = int(input("Enter number of end devices (hosts): "))
cidr_block = input("Enter classless subnet (e.g., 192.168.1.0/28): ")

allocator = IPAllocator(cidr_block)

routers = []
hosts = []

print("\n▶ Configuring Routers")
for i in range(num_routers):
    name = f"R{i+1}"
    ip = allocator.next_ip()
    mac = f"AA:00:00:00:{i:02X}:{i:02X}"
    r = Router(name)
    r.add_interface(ip, mac)
    routers.append(r)

print("\n▶ Configuring Hosts")
for i in range(num_hosts):
    name = f"H{i+1}"
    ip = allocator.next_ip()
    mac = f"BB:00:00:00:{i:02X}:{i:02X}"
    h = Host(name)
    h.configure_interface(ip, mac)
    hosts.append(h)

print("\n📋 Final Assigned IPs with Device Roles")

print("\n🔹 Routers:")
for r in routers:
    iface = r.interfaces[0]
    print(f"{r.name} → IP: {iface.ip}, MAC: {iface.mac}")

print("\n🔹 Hosts:")
for h in hosts:
    iface = h.interfaces[0]
    print(f"{h.name} → IP: {iface.ip}, MAC: {iface.mac}")

