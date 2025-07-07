import time
import random

__all__ = ['go_back_n_send', 'go_back_n_receive']  # Explicit exports

def go_back_n_send(data, channel, src_port, dst_port, window_size=4, segment_size=64):
    segments = [data[i:i+segment_size] for i in range(0, len(data), segment_size)]
    
    base = 0
    next_seq = 0
    acked = [False] * len(segments)

    print(f"[Go-Back-N] Sending {len(segments)} segments from {src_port} to {dst_port}")

    while base < len(segments):
        while next_seq < base + window_size and next_seq < len(segments):
            print(f"[Segment {next_seq}] Size: {len(segments[next_seq])} bytes")
            key = (src_port, dst_port)
            if key not in channel:
                channel[key] = []
            channel[key].append((next_seq, segments[next_seq]))
            next_seq += 1

        time.sleep(0.1)
        for i in range(base, next_seq):
            if random.random() > 0.1:  # 90% success rate
                acked[i] = True
                print(f"[ACK] Received for segment {i}")

        while base < len(segments) and acked[base]:
            base += 1

def go_back_n_receive(channel, dst_port, timeout=5):
    received_segments = {}
    sender_port = None
    start_time = time.time()

    while True:
        for key in list(channel.keys()):
            src_port, d_port = key
            if d_port != dst_port:
                continue

            for i, (seq, seg) in enumerate(channel[key]):
                received_segments[seq] = seg
                if sender_port is None:
                    sender_port = src_port
                del channel[key][i]
                break

        if received_segments:
            max_seq = max(received_segments.keys())
            if all(seq in received_segments for seq in range(max_seq + 1)):
                full_data = ''.join([received_segments[seq] for seq in sorted(received_segments.keys())])
                return {
                    "src_port": sender_port,
                    "data": full_data
                }

        if time.time() - start_time > timeout:
            break

        time.sleep(0.05)
    
    return {"src_port": sender_port, "data": ""}