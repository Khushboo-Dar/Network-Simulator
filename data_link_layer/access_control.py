import random
import time
import logging

class CSMA_CD:
    def __init__(self):
        self.channel_busy = False
        logging.basicConfig(level=logging.INFO)

    def send_frame(self, frame, sender, medium):
        """Simulate CSMA/CD: check if the channel is busy"""
        while self.channel_busy:
            logging.info(f"{sender.name} detects collision. Waiting...")
            time.sleep(random.uniform(0.1, 0.5))  # Random backoff

        self.channel_busy = True
        logging.info(f"{sender.name} is sending: {frame}")
        transmission_time = len(frame.data) * 0.01  # Simulate transmission time based on frame size
        time.sleep(transmission_time)
        self.channel_busy = False
        medium.receive_frame(frame, sender)