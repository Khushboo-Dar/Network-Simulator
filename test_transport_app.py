from TransportLayer.transport import TransportLayer
from ApplicationLayer.echo_app import echo_server, echo_client
from ApplicationLayer.ftp_app import ftp_server, ftp_client
from ApplicationLayer.telnet_app import telnet_server, telnet_client
import threading
import time

def main():
    channel = []  # Simulated channel (shared list)
    transport = TransportLayer()

    print("\n" + "="*60)
    print("========== TRANSPORT & APPLICATION LAYER DEMO ==========")
    print("="*60)

    # Echo test
    print("\n" + "="*60)
    print("--- Echo Service Test ---")
    print("="*60)
    echo_port = transport.assign_port("echo_server", 7000)
    print(f"[Setup] Assigned well-known port 7000 to Echo Server process.")
    print("    > This port is reserved for the echo service, enabling clients to know where to send echo requests.")
    print(f"[Backend] Port table after assignment: {transport.port_table}")

    # Start Echo Server in a thread
    print("[Backend] Starting Echo Server thread to listen for incoming messages on port 7000.")
    server_thread = threading.Thread(target=echo_server, args=(transport, echo_port, channel))
    server_thread.start()
    time.sleep(0.2)  # Give server time to start

    print("[Action] Echo Client will now send a message to the Echo Server using an ephemeral port.")
    echo_client(transport, echo_port, "Hello, World!", channel)
    server_thread.join()
    print("[Result] Echo service test completed. The message was sent, echoed, and received successfully.\n")

    # FTP test
    print("\n" + "="*60)
    print("--- FTP Service Test ---")
    print("="*60)
    ftp_port = transport.assign_port("ftp_server", 21)
    files = {"readme.txt": "This is a test file."}
    print(f"[Setup] Assigned well-known port 21 to FTP Server process.")
    print("    > Port 21 is the standard port for FTP services, allowing clients to request files.")
    print(f"[Setup] FTP server has the following files available: {list(files.keys())}")
    print(f"[Backend] Port table after assignment: {transport.port_table}")

    # Start FTP Server in a thread
    print("[Backend] Starting FTP Server thread to listen for file requests on port 21.")
    ftp_server_thread = threading.Thread(target=ftp_server, args=(transport, ftp_port, channel, files))
    ftp_server_thread.start()
    time.sleep(0.2)  # Give server time to start

    print("[Action] FTP Client will now request 'readme.txt' from the FTP Server using an ephemeral port.")
    ftp_client(transport, ftp_port, "readme.txt", channel)
    ftp_server_thread.join()
    print("[Result] FTP service test completed. The file was requested and the content received by the client.\n")

    # Telnet test
    print("\n" + "="*60)
    print("--- Telnet Service Test ---")
    print("="*60)
    telnet_port = transport.assign_port("telnet_server", 23)
    print(f"[Setup] Assigned well-known port 23 to Telnet Server process.")
    print("    > Port 23 is the standard port for Telnet services, enabling remote command execution.")
    print(f"[Backend] Port table after assignment: {transport.port_table}")

    print("[Backend] Starting Telnet Server thread to listen for commands on port 23.")
    telnet_server_thread = threading.Thread(target=telnet_server, args=(transport, telnet_port, channel))
    telnet_server_thread.start()
    time.sleep(0.2)  # Give server time to start

    print("[Action] Telnet Client will now send the command 'date' to the Telnet Server using an ephemeral port.")
    telnet_client(transport, telnet_port, "date", channel)
    telnet_server_thread.join()
    print("[Result] Telnet service test completed. The command was sent and the response received by the client.\n")

    print("="*60)
    print("========== DEMO COMPLETE ==========")
    print("="*60)

if __name__ == "__main__":
    main()