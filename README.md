# Network Simulator

## Project Description

This project is a **Network Simulator** that implements key networking concepts at the **Data Link Layer** and **Physical Layer**. It simulates how frames are transmitted, how collision detection (CSMA/CD) works, and how flow control mechanisms like Stop-and-Wait operate. The simulation also includes basic **switching functionality**.

## Project Structure

```markdown
network-simulator/
│── data_link_layer/         # Implements Data Link Layer components
│   ├── __init__.py
│   ├── access_control.py    # CSMA/CD implementation
│   ├── bridge.py            # Bridge functionality
│   ├── end_device.py        # End devices in the network
│   ├── error_control.py     # Error detection mechanisms (parity/CRC)
│   ├── frame.py             # Frame structure definition
│   ├── switch.py            # Switch with MAC learning functionality
│
│── physical_layer/          # Implements Physical Layer simulation
│   ├── __init__.py
│   ├── physical_layer.py    # Physical layer logic
│
│── tests/                   # Contains test scripts
│   ├── __init__.py
│   ├── test_data_link.py    # Tests for data link layer
│   ├── test_simulation.py   # Overall simulation tests
│
│── general/                 # Environment setup files
│   ├── bin/
│   ├── lib/
│   ├── .gitignore
│   ├── pyvenv.cfg
│
│── main.py                  # Entry point of the simulation
│── README.md                # Project documentation
```

## Features

- **Dedicated Link Simulation**: Simulate end-to-end connections between two devices. This feature demonstrates a direct communication link where data is transmitted without any intermediate devices.
- **Star Topology Simulation**: Simulate a network topology using hubs and switches. This feature shows how devices are connected in a star configuration, with a central hub or switch managing the communication.
- **CRC Error Detection**: Simulate Cyclic Redundancy Check (CRC) error detection mechanisms. This feature demonstrates how CRC is used to detect errors in transmitted data.
- **Bridge Simulation**: Simulate network bridges that connect multiple network segments. This feature shows how bridges can be used to divide a network into smaller segments, reducing collisions and improving performance.
- **Stop-and-Wait ARQ**: Simulate the Stop-and-Wait Automatic Repeat reQuest protocol for reliable data transmission. This feature demonstrates a simple flow control mechanism where the sender waits for an acknowledgment before sending the next frame.
- **CSMA/CD Testing**: Test the Carrier Sense Multiple Access with Collision Detection (CSMA/CD) protocol used in Ethernet networks. This feature shows how devices detect collisions and manage retransmissions to ensure successful communication.

## Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Khushboo-Dar/Network-Simulator.git
cd Network-Simulator
```

### 2️⃣ Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```



### 4️⃣ Running Tests

To test the **Data Link Layer** implementation:

```bash
python tests/test_data_link.py
```

## Running the Simulation

To run the complete network simulation:

```bash
python main.py
```

You will be presented with a menu to select different simulations:
```
========== NETWORK SIMULATOR MENU ==========
1. Dedicated Link (End-to-End Connection)
2. Simulation through Hub — STAR TOPOLOGY
3. CRC Error Detection Simulation
4. Bridge Simulation
5. Stop and Wait Simulation
6. Switch with 5 Devices
7. Two Star Topologies with Hubs + Switch
8. Testing CSMA/CD
9. Exit
============================================
Enter your choice (1-9):
```

Enter the number corresponding to the simulation you want to run.

## Troubleshooting

If you encounter a `ModuleNotFoundError`, ensure that the `data_link_layer` and `physical_layer` directories contain an `__init__.py` file. If the issue persists, run:

```bash
export PYTHONPATH=$(pwd)  # Linux/macOS
set PYTHONPATH=%CD%       # Windows (cmd)
```

## Contributors

- **Khushboo**
- **Afsheen**
- **Sibgat**

```bash
python3 -m test_cases.test_arp_resolution
python3 -m test_cases.test_assign_classless_ips
python3 -m test_cases.test_router_basic
python3 -m test_cases.test_static_routing
```