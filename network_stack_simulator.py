from NetworkLayer.host import Host
from NetworkLayer.router import Router
from NetworkLayer.switch import Switch
from NetworkLayer.serialLink import SerialLink
from TransportLayer.transport import TransportLayer
from ApplicationLayer.ftp_app import ftp_server, ftp_client
from ApplicationLayer.telnet_app import telnet_server, telnet_client
from NetworkLayer.network_interface import NetworkInterface
import threading
import time

def main():
    print("\n=== FULL NETWORK STACK SIMULATION ===")

    # Physical & Network Layer Setup
    s1, s2 = Switch("Switch1"), Switch("Switch2")
    r1 = Router("Router1", {
        "eth1": ("10.0.0.1", "AA:BB:CC:DD:EE:01", 24),
        "eth2": ("20.0.0.1", "AA:BB:CC:DD:EE:02", 24)
    })

    r1.connect_interface("eth1", s1)
    r1.connect_interface("eth2", s2)

    h1 = Host("PC-A", "10.0.0.10", "AA:AA:AA:AA:AA:01", "10.0.0.1")
    h2 = Host("PC-B", "20.0.0.10", "AA:AA:AA:AA:AA:02", "20.0.0.1")

    h1.connect(s1, 1)
    h2.connect(s2, 2)
    s1.connect_device(r1, 3)
    s2.connect_device(r1, 4)

    # RIP setup
    r1.rip.routing_table.clear()
    r1.add_directly_connected_to_rip()

    # Layers
    transport = TransportLayer()
    net = NetworkInterface()
    channel = []

    while True:
        print("\nSelect Service:")
        print("1. FTP")
        print("2. Telnet")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            print("\n[FTP Selected]")
            ftp_port = transport.assign_port("ftp_server", 21)
            files = {"readme.txt": "Welcome to the network simulator!"}
            server_thread = threading.Thread(target=ftp_server, args=(transport, ftp_port, channel, files))
            server_thread.start()
            time.sleep(0.3)

            print("[Client] Sending FTP request from PC-A to PC-B")
            ftp_client(transport, ftp_port, "readme.txt", channel)

            server_thread.join()

        elif choice == "2":
            print("\n[Telnet Selected]")
            telnet_port = transport.assign_port("telnet_server", 23)
            server_thread = threading.Thread(target=telnet_server, args=(transport, telnet_port, channel))
            server_thread.start()
            time.sleep(0.3)

            username = input("Enter Telnet username: ")
            password = input("Enter password: ")
            command = input("Enter command (date, whoami, etc): ")

            telnet_client(transport, telnet_port, username, password, command, channel)
            server_thread.join()

        elif choice == "3":
            print("Exiting full stack simulation.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
