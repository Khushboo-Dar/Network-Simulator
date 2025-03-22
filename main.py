from physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology
from Data_link_layer.error_control import crc_simulation

def main():
    while True:
        print("\n========== NETWORK SIMULATOR MENU ==========")
        print("1. Dedicated Link (End-to-End Connection)")
        print("2. Simulation through Hub — STAR TOPOLOGY")
        print("3. CRC Error Detection Simulation")
        print("4. Exit")
        print("============================================")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == "1":
            print("\n[ Dedicated Link Simulation Selected ]")
            simulate_dedicated_link()

        elif choice == "2":
            print("\n[ Star Topology via Hub Simulation Selected ]")
            simulate_star_topology()

        elif choice == "3":
            print("\n[ CRC Error Detection Simulation Selected ]")
            crc_simulation()

        elif choice == "4":
            print("\nExiting Network Simulator. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

# Call the main function
if __name__ == "__main__":
    main()
