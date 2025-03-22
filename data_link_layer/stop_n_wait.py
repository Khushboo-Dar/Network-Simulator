import random
import time

class StopAndWait:
    def __init__(self, loss_prob=0.2):  # 20% chance of packet loss
        self.loss_prob = loss_prob

    def send_frame(self, frame):
        """Simulates sending a frame with possible loss."""
        print(f"Sending Frame: {frame}")
        time.sleep(1)  # Simulate transmission delay
        
        if random.random() < self.loss_prob:  # Simulate packet loss
            print(f"Frame {frame} lost! Retrying...\n")
            return False  # No ACK received (lost frame)
        else:
            print(f"Frame {frame} received successfully!")
            return True  # ACK received

    def send_data(self, frames):
        """Implements Stop-and-Wait flow control for multiple frames."""
        for frame in frames:
            while not self.send_frame(frame):  # Keep sending until ACK is received
                time.sleep(1)  # Wait before retrying
            print(f"ACK received for Frame: {frame} \n")


def simulate_stop_and_wait():
    """Function to run Stop-and-Wait simulation."""
    sender = StopAndWait()
    
    # Get number of frames from user
    num_frames = int(input("Enter the number of frames to send: "))
    data_frames = [f"Frame {i+1}" for i in range(num_frames)]

    print("\n--- Start Transmission ---\n")
    sender.send_data(data_frames)
    print("--- Transmission Completed ---")


# Example usage:
if __name__ == "__main__":
    simulate_stop_and_wait()
