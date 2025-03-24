import os
import sys

# Get the absolute path of the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project root to sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import random
import time
import threading
from Data_link_layer.error_control import CRC  # Import CRC class

class Frame:
    """Represents a data frame with sequence number and data."""
    
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data  # Data with CRC checksum

    def __repr__(self):
        return f"Frame(seq={self.seq_num}, data={self.data})"

class StopAndWaitARQ:
    """Implements Stop-and-Wait ARQ with CRC-based error detection."""

    def __init__(self, timeout):
        self.timeout = timeout
        self.sender_seq = 0
        self.receiver_seq = 0
        self.timer = None
        self.ack_received = threading.Event()
        self.crc = CRC()  # Initialize CRC class
        """In a Stop-and-Wait ARQ protocol (or similar network protocols), the sender sends a frame and waits for an acknowledgment (ACK) from the receiver before sending the next frame. 
        The threading.Event object is used to:
        Signal when an ACK is received.
        Wait for the ACK before proceeding to the next step."""
        """The threading.Event object has three key methods:
    
        set(): Sets the internal flag to True. This signals that the event has occurred (e.g., an ACK has been received).
    
        clear(): Resets the internal flag to False. This indicates that the event has not occurred (e.g., no ACK has been received yet).
    
        wait(timeout=None): Blocks the calling thread until the event is set (i.e., the internal flag becomes True). If a timeout is provided, the thread will wait for up to timeout seconds. If the event is not set within the timeout, the method returns False."""

    def start_timer(self, frame):
        """Starts a timer for retransmission."""
        self.ack_received.clear()
        self.timer = threading.Timer(self.timeout, self.timeout_handler, args=[frame])
        self.timer.start()
        """Creates a threading.Timer object that will call the timeout_handler method after self.timeout seconds.

        The args=[frame] parameter passes the current frame to the timeout_handler method."""

    def timeout_handler(self, frame):
        """Handles timeout and retransmits the frame."""
        print(f"Timeout! Retransmitting Frame {frame.seq_num}...")
        self.send_frame(frame.data)

    def send_frame(self, data):
        """Sends a frame with CRC checksum."""
        encoded_data = self.crc.crc_encode(data)
        corrupted_data = self.crc.introduce_error(encoded_data)  # Append CRC checksum
        frame = Frame(self.sender_seq, corrupted_data)
        print(f"\nSender: Sending frame + checksum: {frame}")

        # Simulate frame loss (10% probability)
        if random.random() < 0.1:
            print(f"Frame {frame.seq_num} lost!")
            return self.start_timer(frame)

        # Start timer for retransmission
        self.start_timer(frame)

        # Simulate transmission delay
        time.sleep(random.uniform(0.5, 2))

        # Receiver processes the frame
        self.receive_frame(frame)

    def receive_frame(self, frame):
        """Receives a frame and checks for errors using CRC."""
        if frame.seq_num != self.receiver_seq:
            print(f"Receiver: Duplicate Frame {frame.seq_num} ignored!")
            return  # No ACK sent

        if not self.crc.crc_check(frame.data):  # Verify CRC checksum
            print(f"Receiver: Frame {frame.seq_num} corrupted! Requesting retransmission...")
            return  # Discard frame, no ACK sent

        print(f"Receiver: Frame {frame.seq_num} received successfully!")

        # Send ACK
        self.send_ack(frame.seq_num)

    def send_ack(self, seq_num):
        """Sends an acknowledgment."""
        next_seq_num = seq_num ^ 1  # Toggle sequence number
        print(f"Sender: Sending ACK for Frame {next_seq_num}\n")
        
        self.ack_received.set()  # ACK received, stop timer
        if self.timer:
            self.timer.cancel()

        # Toggle sequence numbers
        self.sender_seq ^= 1  
        self.receiver_seq ^= 1 
        """The sequence number alternates (0 → 1 → 0 → 1), ensuring proper synchronization.

        This mimics the window moving forward by one frame after each successful transmission."""


        """The sequence numbers (self.sender_seq and self.receiver_seq) are toggled using the XOR (^) operation with 1.

        This is a common technique in protocols like the stop-and-wait protocol, where sequence numbers alternate between 0 and 1 to distinguish between consecutive frames.
        
        For example:
        
        If self.sender_seq is 0, it becomes 1 after the operation.
        
        If self.sender_seq is 1, it becomes 0 after the operation.
        

        The same logic applies to self.receiver_seq.""" 


    def send_data(self, frames):
        """Sends multiple frames using Stop-and-Wait ARQ."""
        for data in frames:
            self.send_frame(data)
            self.ack_received.wait()  # Wait for ACK before sending next frame

def simulate_stop_and_wait():
    """Runs the Stop-and-Wait simulation."""
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
