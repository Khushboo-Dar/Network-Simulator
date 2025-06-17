import os
import sys

# Get the absolute path of the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project root to sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data_link_layer.bridge import bridge_simulation
from data_link_layer.error_control import crc_simulation
from physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology
from data_link_layer.test_data_link import test_case_1, test_case_2, test_case_3
from NetworkLayer.testcase1 import testcase1
from NetworkLayer.testcase2 import testcase2
from data_link_layer.gbn import simulate_go_back_n
from TransportLayer.test_transport_app import simulate_transport_layer

def main():
    while True:
        print("\n========== NETWORK SIMULATOR MENU ==========")
        print("1. Dedicated Link (End-to-End Connection)")
        print("2. Simulation through Hub — STAR TOPOLOGY")
        print("3. CRC Error Detection Simulation")
        print("4. Bridge Simulation")
        print("5. Go Back N Simulation")
        print("6.  Switch with 5 Devices")
        print("7.  Two Star Topologies with Hubs + Switch")
        print("8.  Testing CSMA/CD")
        print("9. Network Test Case 1 (Basic Router)")
        print("10. Network Test Case 2 (Three Routers with RIP)")
        print("11. Transport Layer And Application Layer")
        print("12. Exit")
        print("============================================")

        choice = input("Enter your choice (1-12): ")

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

        elif choice == "5":
          print("\n[ Stop and Wait Simulation Selected ]")
          simulate_go_back_n()
          
        elif choice == "6":
            print("\n[ Test Case 1: Switch with 5 Devices Selected ]")
            test_case_1()

        elif choice == "7":
            print("\n[ Test Case 2: Two Star Topologies with Hubs + Switch Selected ]")
            test_case_2()

        elif choice == "8":
            print("\n[ Test Case 3: Testing CSMA/CD Selected ]")
            test_case_3()

        elif choice == '9':
            print("\nRunning Network Test Case 1...")
            testcase1()
        elif choice == '10':
            print("\nRunning Network Test Case 2...")
            testcase2()
        elif choice == '11':
            print("\nRunning Transport Layer And Application Layer...")
            simulate_transport_layer()
    
        elif choice == '12':
            print("\nExiting Network Simulator. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Call the main function
if __name__ == "__main__":
    main()
#----------------------------------------------------------------------------------

#-------------------FULL  STACK IMPLEMENTATION-------------------------------------

#----------------------------------------------------------------------------------

# import threading
# from physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology
# from Data_link_layer.bridge import bridge_simulation
# from Data_link_layer.error_control import crc_simulation
# from Data_link_layer.stop_n_wait import simulate_stop_and_wait
# from NetworkLayer.testcase1 import testcase1
# from NetworkLayer.testcase2 import testcase2

# def run_full_simulation():
#     threads = [
#         threading.Thread(target=simulate_dedicated_link, name="PhysicalLayer-DedicatedLink"),
#         threading.Thread(target=simulate_star_topology, name="PhysicalLayer-StarTopology"),
#         threading.Thread(target=bridge_simulation, name="DataLinkLayer-Bridge"),
#         threading.Thread(target=crc_simulation, name="DataLinkLayer-CRC"),
#         threading.Thread(target=simulate_stop_and_wait, name="DataLinkLayer-StopNWait"),
#         threading.Thread(target=testcase1, name="NetworkLayer-Test1"),
#         threading.Thread(target=testcase2, name="NetworkLayer-Test2"),
#     ]

#     for t in threads:
#         t.start()
#     for t in threads:
#         t.join()

# if __name__ == "__main__":
#     run_full_simulation()