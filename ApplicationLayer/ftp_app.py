def ftp_server(transport, listen_port, channel=None, files=None):
    channel = channel or transport.channel
    files = files or {}
    print(f"[FTP Server] Listening on port {listen_port}")
    
    try:
        raw_data = transport.receive(listen_port)
        if not raw_data:
            raise ValueError("Empty message received")
        
        if len(raw_data) < 4:
            raise ValueError("Message too short")
            
        filename_len = int(raw_data[:4])
        if len(raw_data) < 4 + filename_len + 1:
            raise ValueError("Invalid message format")
            
        filename = raw_data[4:4+filename_len]
        port_str = raw_data[4+filename_len:].strip()
        
        print(f"[FTP Server] File request: '{filename}'")
        print(f"[FTP Server] Data port: {port_str}")

        content = files.get(filename, "File not found")
        transport.send(listen_port + 1, int(port_str), content)
        print("[FTP Server] Transfer complete")
        
    except Exception as e:
        print(f"[FTP Server] ERROR: {str(e)}")

def ftp_client(transport, server_port, filename, channel=None):
    channel = channel or transport.channel
    try:
        control_port = transport.assign_port("ftp_client")
        data_port = transport.assign_port("ftp_client_data")
        
        message = f"{len(filename):04d}{filename}\n{data_port}"
        print(f"[FTP Client] Sending request for '{filename}'")
        transport.send(control_port, server_port, message)

        response = transport.receive(data_port)
        print(f"[FTP Client] Received: '{response}'")
        
    except Exception as e:
        print(f"[FTP Client] ERROR: {str(e)}")