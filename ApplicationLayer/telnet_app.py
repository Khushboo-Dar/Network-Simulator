import time

def to_nvt(string):
    encoded = string.replace('\n', '\r\n')
    print(f"[NVT Encode] Original: '{string}' -> Encoded: '{encoded}'")
    return encoded

def from_nvt(encoded):
    decoded = encoded.replace('\r\n', '\n')
    print(f"[NVT Decode] Encoded: '{encoded}' -> Decoded: '{decoded}'")
    return decoded

def telnet_server(transport, port, channel):
    print(f"[Telnet Server] Listening on port {port}")
    username = transport.receive(port, channel).strip()
    password = transport.receive(port, channel).strip()
    client_port = transport.last_source_port
    response_port = client_port + 1

    if username == "sibgat" and password == "1234":
        login_msg = "Login successful"
        print(f"[Telnet Server] Login successful for user: {username}")
    else:
        login_msg = "Login failed"
        print(f"[Telnet Server] Login failed for user: {username}")

    encoded_login = to_nvt(login_msg)
    print(f"[Telnet Server] Sending response (Local → NVT): '{login_msg}' -> '{encoded_login}'")
    transport.send(port, response_port, encoded_login, channel)

    if login_msg != "Login successful":
        return

    command_encoded = transport.receive(port, channel)
    print(f"[Telnet Server] Received encoded command: '{command_encoded.strip()}'")
    decoded_command = from_nvt(command_encoded.strip())
    print(f"[Telnet Server] Decoded (NVT → Local): '{command_encoded.strip()}' -> '{decoded_command}'")

    if decoded_command == "date":
        response = time.ctime()
    elif decoded_command == "whoami":
        response = f"You are {username}"
    else:
        response = f"Unknown command: {decoded_command}"

    encoded_response = to_nvt(response)
    print(f"[Telnet Server] Sending response (Local → NVT): '{response}' -> '{encoded_response}'")
    transport.send(port, response_port, encoded_response, channel)

def telnet_client(transport, server_port, username, password, command, channel):
    client_port = transport.assign_port("telnet_client")
    receive_port = transport.assign_port("telnet_client_response", client_port + 1)

    print(f"[Telnet Client] Connecting to port {server_port}")
    print("[Telnet Client] Sending username and password...")

    transport.send(client_port, server_port, username, channel)
    transport.send(client_port, server_port, password, channel)

    encoded_login = transport.receive(receive_port, channel)
    login_status = from_nvt(encoded_login).strip()
    print(f"[Telnet Client] Response received (NVT → Local): '{encoded_login}' -> '{login_status}'")
    print(f"[Telnet Client] Server response: {login_status}")

    if login_status != "Login successful":
        print("[Telnet Client] Aborting command due to failed login.")
        return

    encoded_command = to_nvt(command)
    print(f"[Telnet Client] Sending (Local → NVT): '{command}' -> '{encoded_command}'")
    transport.send(client_port, server_port, encoded_command, channel)

    encoded_reply = transport.receive(receive_port, channel)
    decoded_reply = from_nvt(encoded_reply)
    print(f"[Telnet Client] Response received (NVT → Local): '{encoded_reply}' -> '{decoded_reply.strip()}'")
    print(f"[Telnet Client] Received response: {decoded_reply.strip()}")
