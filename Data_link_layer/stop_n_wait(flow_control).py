class SlidingWindow:
    def __init__(self, window_size):
        self.window_size = window_size
        self.send_base = 0
        self.next_seq_num = 0

    def send(self, total_frames):
        while self.next_seq_num < total_frames:
            if self.next_seq_num < self.send_base + self.window_size:
                print(f"Sending frame {self.next_seq_num}")
                self.next_seq_num += 1

    def acknowledge(self, ack):
        print(f"Acknowledgment received for frame {ack}")
        self.send_base = ack + 1
