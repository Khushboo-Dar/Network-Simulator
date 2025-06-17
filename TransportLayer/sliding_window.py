import time
import random

def go_back_n_send(data, channel, src_port, dst_port, window_size=4):
    segments = [data[i:i+4] for i in range(0, len(data), 4)]
    base = 0
    next_seq = 0
    acked = [False] * len(segments)

    print(f"[Go-Back-N] Sending {len(segments)} segments from port {src_port} to {dst_port}")

    while base < len(segments):
        while next_seq < base + window_size and next_seq < len(segments):
            print(f"[Go-Back-N] Sent segment {next_seq}: {segments[next_seq]}")
            key = (src_port, dst_port)
            if key not in channel:
                channel[key] = []
            channel[key].append((next_seq, segments[next_seq]))
            next_seq += 1

        time.sleep(0.1)
        for i in range(base, next_seq):
            if random.random() > 0.1:  # 90% ACK chance
                acked[i] = True
                print(f"[Go-Back-N] ACK received for segment {i}")

        while base < len(segments) and acked[base]:
            base += 1


def go_back_n_receive(channel, dst_port, timeout=5):
    received = []
    expected_seq = 0
    start_time = time.time()
    sender_port = None

    while True:
        to_remove = []

        for key in list(channel.keys()):
            src_port, d_port = key
            if d_port != dst_port:
                continue

            for i, (seq, seg) in enumerate(channel[key]):
                if seq == expected_seq:
                    if sender_port is None:
                        sender_port = src_port  # ✅ Remember who sent it
                    received.append(seg)
                    expected_seq += 1
                    to_remove.append((key, i))

        for key, i in reversed(to_remove):
            del channel[key][i]

        if time.time() - start_time > timeout or received:
            break

        time.sleep(0.05)

    full_data = ''.join(received)
    return {
        "src_port": sender_port,
        "data": full_data
    }
