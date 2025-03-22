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

## Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Khushboo-Dar/Network-Simulator.git
cd Network-Simulator
```

### 2️⃣ Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.




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

## Troubleshooting

If you encounter a `ModuleNotFoundError`, ensure that the `data_link_layer` and `physical_layer` directories contain an `__init__.py` file. If the issue persists, run:

```bash
export PYTHONPATH=$(pwd)  # Linux/macOS
set PYTHONPATH=%CD%       # Windows (cmd)
```


