<<<<<<< HEAD
from data_link_layer.bridge import bridge_simulation
from data_link_layer.error_control import crc_simulation
from Data_link_layer.stop_n_wait import simulate_stop_and_wait
from physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology
from tests.test_data_link import test_case_1, test_case_2, test_case_3  # Import test cases of Data Link Layer
=======
from Data_link_layer.bridge import bridge_simulation
from Data_link_layer.error_control import crc_simulation
from Data_link_layer.stop_n_wait import simulate_stop_and_wait
from physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology
from tests.test_data_link import test_case_1, test_case_2, test_case_3  # Import test cases
>>>>>>> origin/data-link-khushboo


def main():
    while True:
        print("\n========== NETWORK SIMULATOR MENU ==========")
        print("1. Dedicated Link (End-to-End Connection)")
        print("2. Simulation through Hub — STAR TOPOLOGY")
        print("3. CRC Error Detection Simulation")
        print("4. Bridge Simulation")
        print("5. Stop and Wait Simulation")
        print("6.  Switch with 5 Devices")
        print("7.  Two Star Topologies with Hubs + Switch")
        print("8.  Testing CSMA/CD")
<<<<<<< HEAD

=======
>>>>>>> origin/data-link-khushboo
        print("9. Exit")
        print("============================================")

        choice = input("Enter your choice (1-9): ")

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
            print("\n[ Bridge Simulation Selected ]")
            bridge_simulation()

<<<<<<< HEAD

        elif choice == "5":
            print("\n[ Stop and Wait Simulation Selected ]")
            simulate_stop_and_wait()

        elif choice == "6":
            print("\n[ Test Case 1: Switch with 5 Devices Selected ]")
            test_case_1()

=======
        elif choice == "5":
          print("\n[ Stop and Wait Simulation Selected ]")
          simulate_stop_and_wait()
          
        elif choice == "6":
            print("\n[ Test Case 1: Switch with 5 Devices Selected ]")
            test_case_1()

>>>>>>> origin/data-link-khushboo
        elif choice == "7":
            print("\n[ Test Case 2: Two Star Topologies with Hubs + Switch Selected ]")
            test_case_2()

        elif choice == "8":
            print("\n[ Test Case 3: Testing CSMA/CD Selected ]")
            test_case_3()

<<<<<<< HEAD

=======
>>>>>>> origin/data-link-khushboo
        elif choice == "9":
            print("\nExiting Network Simulator. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

# Call the main function
if __name__ == "__main__":
    main()