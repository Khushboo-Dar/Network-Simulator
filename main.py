from data_link_layer.switch import Switch
from data_link_layer.frame import Frame
from physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology

def main():
    while True:
        print("\n========== NETWORK SIMULATOR MENU ==========")
        print("1. Dedicated Link (End-to-End Connection)")
        print("2. Star Topology Simulation (via Hub)")
        print("3. Bus Topology Simulation")
        print("4. Switch-based Network Simulation")
        print("5. Exit")
        print("============================================")

        try:
            choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print("\n[ERROR] Invalid input! Please enter a number between 1-5.\n")
            continue

        if choice == 1:
            print("\n========================================")
            print("[ Dedicated Link Simulation Selected ]")
            print("========================================\n")
            simulate_dedicated_link()

        elif choice == 2:
            print("\n========================================")
            print("[ Star Topology via Hub Simulation Selected ]")
            print("========================================\n")
            simulate_star_topology()

        elif choice == 3:
            print("\n========================================")
            print("[ Bus Topology Simulation Selected ]")
            print("========================================\n")
            print("[INFO] Bus topology functionality not yet implemented!")

        elif choice == 4:
            print("\n========================================")
            print("[ Switch-based Network Simulation Selected ]")
            print("========================================\n")

            switch = Switch()

            # Add 5 devices to the switch and learn their MAC addresses
            for i in range(1, 6):
                mac_address = f"AA:BB:CC:DD:EE:0{i}"
                switch.learn_mac(mac_address, i)

            sender = "AA:BB:CC:DD:EE:01"
            receiver = "AA:BB:CC:DD:EE:03"
            data = "Hello PC3!"

            print("\n========================================")
            print(f"[ Testing Packet Forwarding from {sender} to {receiver} ]")
            print("========================================\n")

            switch.forward_frame(sender, receiver, data)

        elif choice == 5:
            print("\nExiting Network Simulator. Goodbye!\n")
            break  # Exit the loop

        else:
            print("\n[ERROR] Invalid choice. Please enter a number between 1-5.\n")

# Call the main function
if __name__ == "__main__":
    main()
