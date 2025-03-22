from Physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology

def main():
    print("\n========== NETWORK SIMULATOR MENU ==========")
    print("1. Dedicated Link (End-to-End Connection)")
    print("2. Simulation through Hub — STAR TOPOLOGY")
    print("============================================")

    choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        print("\n[ Dedicated Link Simulation Selected ]")
        simulate_dedicated_link()

    elif choice == 2:
        print("\n[ Star Topology via Hub Simulation Selected ]")
        simulate_star_topology()

    else:
        print("Invalid choice. Please enter 1 or 2.")

# Call the main function
if __name__ == "__main__":
    main()
