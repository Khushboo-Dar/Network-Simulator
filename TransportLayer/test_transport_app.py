from TransportLayer.transport import TransportLayer
from ApplicationLayer.ftp_app import ftp_server, ftp_client
from ApplicationLayer.telnet_app import telnet_server, telnet_client
import threading
import time

def simulate_transport_layer():
    channel = {}  # Simulated channel (can be a dict or list depending on your transport layer)
    transport = TransportLayer()

    print("\n" + "="*60)
    print("========== TRANSPORT & APPLICATION LAYER DEMO ==========")
    print("="*60)

    while True:
        print("\nSelect a service to simulate:")
        print("1. FTP")
        print("2. Telnet")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        # ------------------ FTP Service ------------------
        if choice == '1':
            print("\n" + "="*60)
            print("--- FTP Service Test ---")
            print("="*60)

            ftp_port = transport.assign_port("ftp_server", 21)
            files = {"readme.txt": "This is a test file."}
            print(f"[Setup] Assigned port 21 to FTP Server.")
            print(f"[Setup] Files available: {list(files.keys())}")
            print(f"[Backend] Port table after assignment: {transport.port_table}")

            ftp_server_thread = threading.Thread(target=ftp_server, args=(transport, ftp_port, channel, files))
            ftp_server_thread.start()

            time.sleep(0.2)  # Let server start

            print("[Action] FTP Client will now request 'readme.txt'")
            ftp_client(transport, ftp_port, "readme.txt", channel)

            ftp_server_thread.join()
            print("[Result] FTP test completed.\n")

        # ------------------ Telnet Service ------------------
        elif choice == '2':
            print("\n" + "="*60)
            print("--- Telnet Service Test ---")
            print("="*60)

            telnet_port = transport.assign_port("telnet_server", 23)
            print(f"[Setup] Assigned port 23 to Telnet Server.")
            print(f"[Backend] Port table after assignment: {transport.port_table}")

            username = input("Enter Telnet username: ")
            password = input("Enter password: ")
            command = input("Enter Telnet command (e.g., date, whoami): ")

            telnet_server_thread = threading.Thread(target=telnet_server, args=(transport, telnet_port, channel))
            telnet_server_thread.start()

            time.sleep(0.2)  # Let server start

            telnet_client(transport, telnet_port, username, password, command, channel)

            telnet_server_thread.join()
            print("[Result] Telnet test completed.\n")

        # ------------------ Exit ------------------
        elif choice == '3':
            print("\nExiting Transport Layer simulation. Goodbye!\n")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")
