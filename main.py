from data_link_layer.switch import Switch
from data_link_layer.frame import Frame
from physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology
from tests.test_data_link import test_case_1, test_case_2  # Import test cases

def main():
    while True:
        print("\n========== NETWORK SIMULATOR MENU ==========")
        print("1. Dedicated Link (End-to-End Connection)")
        print("2. Star Topology Simulation with Hub")
        print("3. Star Topology Simulation with Switch (5 End Devices)")
        print("4. Switch with Two Hubs (Each with 5 Devices)")
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
            print("[ Star Topology Simulation with Hub Selected ]")
            print("========================================\n")
            simulate_star_topology()

        elif choice == 3:
            print("\n========================================")
            print("[ Star Topology Simulation with Switch Selected ]")
            print("========================================\n")
            test_case_1()  # Call the test function

        elif choice == 4:
            print("\n========================================")
            print("[ Switch with Two Hubs (Each with 5 Devices) Selected ]")
            print("========================================\n")
            test_case_2()  # Call the test function

        elif choice == 5:
            print("\nExiting Network Simulator. Goodbye!\n")
            break  # Exit the loop

        else:
            print("\n[ERROR] Invalid choice. Please enter a number between 1-5.\n")

# Call the main function
if __name__ == "__main__":
    main()
