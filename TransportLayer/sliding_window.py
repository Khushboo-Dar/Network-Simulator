import time
import random

def go_back_n_send(data, channel, src_port, dst_port, window_size=4):
    # Simulate sending data in segments with Go-Back-N
    segments = [data[i:i+4] for i in range(0, len(data), 4)]
    base = 0
    next_seq = 0
    acked = [False] * len(segments)
    print(f"[Go-Back-N] Sending {len(segments)} segments from port {src_port} to {dst_port}")
    while base < len(segments):
        # Send window
        while next_seq < base + window_size and next_seq < len(segments):
            print(f"[Go-Back-N] Sent segment {next_seq}: {segments[next_seq]}")
            channel.append((src_port, dst_port, next_seq, segments[next_seq]))
            next_seq += 1
        # Simulate ACKs
        time.sleep(0.1)
        for i in range(base, next_seq):
            if random.random() > 0.1:  # 90% chance of ACK
                acked[i] = True
                print(f"[Go-Back-N] ACK received for segment {i}")
        while base < len(segments) and acked[base]:
            base += 1

def go_back_n_receive(channel, dst_port):
    received = []
    expected_seq = 0
    sender_port = None

    for pkt in channel:
        src_port, d_port, seq, seg = pkt
        if d_port == dst_port and seq == expected_seq:
            received.append(seg)
            sender_port = src_port
            expected_seq += 1

    return {
        "data": ''.join(received),
        "src_port": sender_port
    }
