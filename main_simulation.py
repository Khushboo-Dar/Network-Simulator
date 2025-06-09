from Data_link_layer.bridge import bridge_simulation
from Data_link_layer.error_control import crc_simulation
from Data_link_layer.stop_n_wait import simulate_stop_and_wait
from Physical_layer.physical_layer import simulate_dedicated_link, simulate_star_topology
from tests.test_data_link import test_case_1, test_case_2, test_case_3

def simulate_network():
    print("\n========== NETWORK SIMULATOR STARTED ==========\n")

    # Physical Layer
    print("[PHYSICAL LAYER] Simulating dedicated link...")
    simulate_dedicated_link()

    print("[PHYSICAL LAYER] Simulating star topology using Hub...")
    simulate_star_topology()

    # Data Link Layer
    print("\n[DATA LINK LAYER] Performing CRC Error Detection...")
    crc_simulation()

    print("[DATA LINK LAYER] Running Bridge Simulation...")
    bridge_simulation()

    print("[DATA LINK LAYER] Running Stop-and-Wait ARQ Protocol...")
    simulate_stop_and_wait()

    print("\n[SWITCH] Running test case with 5 Devices...")
    test_case_1()

    print("[SWITCH + HUB] Running test case with Two Star Topologies and Switch...")
    test_case_2()

    print("[CSMA/CD] Running test case for CSMA/CD...")
    test_case_3()

    print("\n========== NETWORK SIMULATOR COMPLETED ==========\n")

# Entry point
if __name__ == "__main__":
    simulate_network()
