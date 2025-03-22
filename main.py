from data_link_layer.switch import Switch
from data_link_layer.frame import Frame
from physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology

def main():
    print("\n========== NETWORK SIMULATOR MENU ==========")
    print("1. Dedicated Link (End-to-End Connection)")
    print("2. Simulation through Hub — STAR TOPOLOGY")
    print("3. Bus Topology Simulation")
    print("4. Switch-based Network Simulation")
    print("5. Exit")
    print("============================================")

    choice = int(input("Enter your choice (1-5): "))

    if choice == 1:
        print("\n[ Dedicated Link Simulation Selected ]")
        simulate_dedicated_link()

    elif choice == 2:
        print("\n[ Star Topology via Hub Simulation Selected ]")
        simulate_star_topology()

    elif choice == 4:
        print("\n========================================")
        print("[ Switch-based Network Simulation Selected ]")
        print("========================================\n")

        switch = Switch()
        
        # Adding 5 devices to the switch
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
        print("\nExiting Network Simulator successfully \n")

    else:
        print("\nInvalid choice. Please enter a number between 1-5.\n")

# Call the main function
if __name__ == "__main__":
    main()
