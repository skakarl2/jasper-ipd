import unittest
from Qubit import Qubit
from Gates import HadamardGate, PauliXGate
from Circuit import QuantumCircuit
from Measurement import Measurement
from Noise import Noise
from QASM import QASM

class TestQuantumSimulator(unittest.TestCase):

    def test_qubit_initialization(self):
        qubit = Qubit()
        self.assertAlmostEqual(abs(qubit.state[0, 0]) ** 2, 1)
        self.assertAlmostEqual(abs(qubit.state[1, 0]) ** 2, 0)

    def test_hadamard_gate(self):
        qubit = Qubit()
        hadamard = HadamardGate()
        hadamard.apply(qubit)
        self.assertAlmostEqual(abs(qubit.state[0, 0]) ** 2, 0.5)
        self.assertAlmostEqual(abs(qubit.state[1, 0]) ** 2, 0.5)

    def test_circuit_execution(self):
        circuit = QuantumCircuit(1)
        qubit = Qubit()
        circuit.add_gate(HadamardGate(), [0])
        circuit.execute([qubit])
        self.assertAlmostEqual(abs(qubit.state[0, 0]) ** 2, 0.5)
        self.assertAlmostEqual(abs(qubit.state[1, 0]) ** 2, 0.5)

    def test_measurement(self):
        qubit = Qubit()
        result = Measurement.measure(qubit)
        self.assertIn(result, [0, 1])

    def test_noise(self):
        qubit = Qubit()
        Noise.apply_dephasing(qubit, 0.1)
        self.assertAlmostEqual(abs(qubit.state[0, 0]) ** 2, 1)

    def test_qasm_export(self):
        circuit = QuantumCircuit(1)
        circuit.add_gate(HadamardGate(), [0])
        qasm_code = QASM.export(circuit)
        self.assertIn("OPENQASM", qasm_code)

if __name__ == "__main__":
    unittest.main()