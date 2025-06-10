from TransportLayer.transport import TransportLayer
from ApplicationLayer.echo_app import echo_server, echo_client
from ApplicationLayer.ftp_app import ftp_server, ftp_client
import threading
import time

def main():
    channel = []  # Simulated channel (shared list)
    transport = TransportLayer()

    print("\n========== TRANSPORT & APPLICATION LAYER DEMO ==========")

    # Echo test
    echo_port = transport.assign_port("echo_server", 7000)
    print("\n--- Echo Service Test ---")
    print(f"[Setup] Echo server assigned to port {echo_port}")

    # Start Echo Server in a thread
    server_thread = threading.Thread(target=echo_server, args=(transport, echo_port, channel))
    server_thread.start()
    time.sleep(0.2)  # Give server time to start

    print("[Action] Starting Echo Client...")
    echo_client(transport, echo_port, "Hello, World!", channel)
    server_thread.join()
    print("[Result] Echo service test completed.\n")

    # FTP test
    ftp_port = transport.assign_port("ftp_server", 21)
    files = {"readme.txt": "This is a test file."}
    print("\n--- FTP Service Test ---")
    print(f"[Setup] FTP server assigned to port {ftp_port}")
    print("[Setup] FTP server has files:", list(files.keys()))

    # Start FTP Server in a thread
    ftp_server_thread = threading.Thread(target=ftp_server, args=(transport, ftp_port, channel, files))
    ftp_server_thread.start()
    time.sleep(0.2)  # Give server time to start

    print("[Action] Starting FTP Client...")
    ftp_client(transport, ftp_port, "readme.txt", channel)
    ftp_server_thread.join()
    print("[Result] FTP service test completed.\n")

    print("========== DEMO COMPLETE ==========")

if __name__ == "__main__":
    main()