# Jasper
A flexible and powerful issue reader for GitHub

- https://jasperapp.io/
- https://docs.jasperapp.io/

![](https://jasperapp.io/image/ss.png)

You will be able to read, track and discover many active issues very flexibly by using Jasper in GitHub. It is enabled by a powerful function called "stream" of Jasper.

example `repo:nodejs/node is:issue label:bug`

## For Developers

[DEVELOP.md](https://github.com/jasperapp/jasper/blob/master/DEVELOP.md)

## Internal TODO
- [x] Refactoring React components
- [x] `nodeIntegration: false`
- [x] `enableRemoteModule: false`
- [ ] `SameSite` of cookie
- [ ] Unit Test

# Quantum Circuit Simulator

## Overview
This project is a Python-based quantum circuit simulator that allows users to define, simulate, and visualize quantum circuits. It supports common quantum gates, measurements, noise simulation, and OpenQASM integration.

## Features
- **Qubit Representation**: Simulate qubits as state vectors.
- **Quantum Gates**: Includes Hadamard, Pauli-X, Pauli-Z, and custom gates.
- **Quantum Circuits**: Define circuits with multiple qubits and gates.
- **Measurement**: Measure qubits with probabilistic outcomes.
- **Visualization**: Visualize circuits using NetworkX and Matplotlib.
- **Noise Simulation**: Simulate dephasing and amplitude damping noise.
- **OpenQASM Integration**: Export circuits to OpenQASM format.
- **Command-Line Interface**: Interact with the simulator via CLI.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Command-Line Interface
Run the CLI to define and simulate circuits:
```bash
python src/quantum/cli.py --num_qubits 2 --visualize
```

### Example Code
```python
from Qubit import Qubit
from Gates import HadamardGate, PauliXGate
from Circuit import QuantumCircuit
from Measurement import Measurement

# Create a circuit with 2 qubits
circuit = QuantumCircuit(2)
qubit1 = Qubit()
qubit2 = Qubit()

# Add gates
circuit.add_gate(HadamardGate(), [0])
circuit.add_gate(PauliXGate(), [1])

# Execute the circuit
circuit.execute([qubit1, qubit2])

# Measure the qubits
results = Measurement.measure_all([qubit1, qubit2])
print(f"Measurement results: {results}")
```

## Testing
Run unit tests to verify functionality:
```bash
python -m unittest discover test
```

## Contributing
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License.<!-- __ipd:s=sess_d5b8da375c34:i=intr_d5b8da375c34_0001 -->
