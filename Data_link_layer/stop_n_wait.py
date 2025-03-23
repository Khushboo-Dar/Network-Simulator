import random
import time
import threading


class Frame:
    """Represents a data frame with sequence number and data."""
    
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data  # No checksum since error control is removed

    def __repr__(self):
        return f"Frame(seq={self.seq_num}, data={self.data})"

class StopAndWaitARQ:
    """Implements Stop-and-Wait ARQ protocol with timer-based retransmission only."""

    def __init__(self, timeout):
        self.timeout = timeout  # User-defined timeout period
        self.sender_seq = 0
        self.receiver_seq = 0
        self.timer = None
        self.ack_received = threading.Event()  # Event to track ACK
        """In a Stop-and-Wait ARQ protocol (or similar network protocols), the sender sends a frame and waits for an acknowledgment (ACK) from the receiver before sending the next frame. 
        The threading.Event object is used to:
        Signal when an ACK is received.
        Wait for the ACK before proceeding to the next step."""
        """The threading.Event object has three key methods:
    
        set(): Sets the internal flag to True. This signals that the event has occurred (e.g., an ACK has been received).
    
        clear(): Resets the internal flag to False. This indicates that the event has not occurred (e.g., no ACK has been received yet).
    
        wait(timeout=None): Blocks the calling thread until the event is set (i.e., the internal flag becomes True). If a timeout is provided, the thread will wait for up to timeout seconds. If the event is not set within the timeout, the method returns False."""

    def start_timer(self, frame):
        """Starts a timer that will trigger the timeout_handler method if an ACK is not received within the specified timeout period."""
        self.ack_received.clear()  # Ensure sender waits for a new ACK
        self.timer = threading.Timer(self.timeout, self.timeout_handler, args=[frame]) 
        """Creates a threading.Timer object that will call the timeout_handler method after self.timeout seconds.

        The args=[frame] parameter passes the current frame to the timeout_handler method."""
        self.timer.start()  # Starts the timer. If it expires, timeout_handler is called.

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

        # Start timer for retransmission
        self.start_timer(frame)

        # Simulate transmission delay
        time.sleep(random.uniform(0.5, 2))

        # Receiver processes the frame
        self.receive_frame(frame)

    def receive_frame(self, frame):
        """Receives a frame."""
        if frame.seq_num != self.receiver_seq:
            print(f"Receiver: Duplicate Frame {frame.seq_num} ignored!")
            return  # No ACK sent

        print(f"Receiver: Frame {frame.seq_num} received successfully!")

        # Send ACK
        self.send_ack(frame.seq_num)

    def send_ack(self, seq_num):
        """Sends an acknowledgment for the next frame to be sent."""
        next_seq_num = seq_num ^ 1  # Toggle to the next sequence number
        print(f"Sender: Sending ACK for Frame {next_seq_num}\n")
        
        self.ack_received.set()  # ACK received, stop timer
        if self.timer:
            self.timer.cancel()
        
        # Toggle sequence numbers for sender and receiver
        self.sender_seq ^= 1  # Toggle sender's sequence number
        self.receiver_seq ^= 1  # Toggle receiver's sequence number

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