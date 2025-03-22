import random
import time

class CSMA_CD:
    def __init__(self, collision_probability=0.3):
        """Initialize CSMA/CD protocol with collision probability."""
        self.collision_probability = collision_probability

    def send_frame(self, frame):
        """Simulate sending a frame using CSMA/CD."""
        print("\n===========================")
        print("   CSMA/CD TRANSMISSION   ")
        print("===========================")

        print(f"Sending Frame: {frame}")
        time.sleep(1)

        if random.random() < self.collision_probability:
            print("\n[CSMA/CD] Collision detected! Retrying...\n")
            backoff_time = random.randint(1, 3)
            print(f"[CSMA/CD] Waiting for {backoff_time} seconds before retrying...")
            time.sleep(backoff_time)
            self.send_frame(frame)  # Retry after backoff
        else:
            print("\n[CSMA/CD] Frame sent successfully!\n")

        print("===========================\n")
