def ftp_server(transport, listen_port, channel, files):
    print(f"[FTP Server] Listening for control connection on port {listen_port} (default control port 21)")
    
    # Step 1: Receive filename from client (control connection)
    filename = transport.receive(listen_port, channel)
    print(f"[FTP Server] File requested by client: '{filename}'")

    # Step 2: Fetch file content
    content = files.get(filename, "File not found")
    print(f"[FTP Server] Preparing file content: '{content}'")

    # Step 3: Receive the client's data port (from PORT command equivalent)
    client_data_port = transport.receive(listen_port, channel)
    print(f"[FTP Server] Received client's data port: {client_data_port}")

    # Step 4: Send file content to client's data port (simulating data connection)
    server_data_port = listen_port + 1  # mimic FTP using port 20 for data transfer
    print(f"[FTP Server] Opening data connection from port {server_data_port} to client's data port {client_data_port}")
    transport.send(server_data_port, client_data_port, content, channel)
    print("[FTP Server] File content sent over data connection.")
def ftp_client(transport, server_port, filename, channel):
    # Step 1: Assign control port
    control_port = transport.assign_port("ftp_client")
    print(f"[FTP Client] Control connection established on port {control_port} (default client control port)")

    # Step 2: Assign client-side data port
    data_port = transport.assign_port("ftp_client_data")
    print(f"[FTP Client] Reserved data port {data_port} for receiving file")

    # Step 3: Send file request over control connection
    print(f"[FTP Client] Sending filename '{filename}' to server control port {server_port}")
    transport.send(control_port, server_port, filename, channel)

    # Step 4: Send data port info (PORT command equivalent)
    print(f"[FTP Client] Informing server of client data port: {data_port}")
    transport.send(control_port, server_port, str(data_port), channel)

    # Step 5: Receive content over data connection
    print(f"[FTP Client] Waiting to receive file content on data port {data_port}")
    content = transport.receive(data_port, channel)
    print(f"[FTP Client] File content received: '{content}'")