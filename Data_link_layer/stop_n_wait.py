import random
import time
import threading
from Data_link_layer.error_control import crc_division, crc_check  # Importing CRC functions

class Frame:
    """Represents a data frame with sequence number, checksum, and data."""
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data
        self.checksum = crc_division(data)  # Compute checksum using custom CRC

    def __repr__(self):
        return f"Frame(seq={self.seq_num}, data={self.data}, checksum={self.checksum})"

class StopAndWaitARQ:
    """Implements Stop-and-Wait ARQ protocol with timer and CRC error detection."""

    def __init__(self, timeout):
        self.timeout = timeout  # User-defined timeout period
        self.sender_seq = 0
        self.receiver_seq = 0
        self.timer = None
        self.ack_received = threading.Event()  # Event to track ACK

    def start_timer(self, frame):
        """Starts a timer for retransmission if ACK is not received."""
        self.ack_received.clear()
        self.timer = threading.Timer(self.timeout, self.timeout_handler, args=[frame])
        self.timer.start()

    def timeout_handler(self, frame):
        """Handles timeout and retransmits the frame."""
        print(f"Timeout! Retransmitting Frame {frame.seq_num}...")
        self.send_frame(frame.data)

    def send_frame(self, data):
        """Sends a frame and waits for acknowledgment."""
        frame = Frame(self.sender_seq, data)
        print(f"\nSender: Sending {frame}")

        # Simulate frame loss (10% probability)
        if random.random() < 0.1:
            print(f"Frame {frame.seq_num} lost!")
            return self.start_timer(frame)

        # Simulate corruption (10% probability)
        if random.random() < 0.1:
            corrupted_data = self.corrupt_data(frame.data)
            frame = Frame(self.sender_seq, corrupted_data)  # Recompute checksum
            print(f"Frame {frame.seq_num} corrupted!")

        # Start timer for retransmission
        self.start_timer(frame)

        # Simulate transmission delay
        time.sleep(random.uniform(0.5, 2))

        # Receiver processes the frame
        self.receive_frame(frame)

    def corrupt_data(self, data):
        """Introduces a minor corruption in the data string."""
        if len(data) > 1:
            index = random.randint(0, len(data) - 1)
            corrupted_char = chr(ord(data[index]) ^ 1)  # Flip a bit
            return data[:index] + corrupted_char + data[index + 1:]
        return data

    def receive_frame(self, frame):
        """Receives a frame and checks for errors."""
        if not crc_check(frame.data, frame.checksum):
            print(f"Receiver: Checksum error! Discarding Frame {frame.seq_num}")
            return  # No ACK sent

        if frame.seq_num != self.receiver_seq:
            print(f"Receiver: Duplicate Frame {frame.seq_num} ignored!")
            return  # No ACK sent

        print(f"Receiver: Frame {frame.seq_num} received successfully!")

        # Send ACK
        self.send_ack(frame.seq_num)

    def send_ack(self, seq_num):
        """Sends an acknowledgment."""
        print(f"📨 Sender: Received ACK for Frame {seq_num}\n")
        self.ack_received.set()  # ACK received, stop timer
        if self.timer:
            self.timer.cancel()
        self.sender_seq ^= 1  # Toggle sequence number
        self.receiver_seq ^= 1  # Toggle sequence number

    def send_data(self, frames):
        """Sends multiple frames using Stop-and-Wait ARQ."""
        for data in frames:
            self.send_frame(data)
            self.ack_received.wait()  # Wait until ACK is received before sending next frame


def simulate_stop_and_wait():
    """Function to run Stop-and-Wait simulation."""
    timeout = int(input("Enter timeout period (seconds): "))
    sender = StopAndWaitARQ(timeout)

    # Get number of frames from user
    num_frames = int(input("Enter the number of frames to send: "))
    data_frames = [f"Frame {i+1}" for i in range(num_frames)]

    print("\n--- Start Transmission ---\n")
    sender.send_data(data_frames)
    print("--- Transmission Completed ---")


# Run simulation
if __name__ == "__main__":
    simulate_stop_and_wait()
