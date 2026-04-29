"""
Quantum Logic Playground: GHZ State (Greenberger–Horne–Zeilinger) Implementation
Author: [Senin Adın]

This script demonstrates multi-qubit entanglement.
Standard GHZ state is: (|000> + |111>) / sqrt(2)
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from visualization import plot_circuit_diagram, plot_results_histogram, plot_on_bloch_sphere


def create_ghz_circuit(n_qubits=3):
    """
    Creates a quantum circuit to generate an n-qubit GHZ state.
    """
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Step 1: Put the first qubit (q0) in superposition
    # |0> -> (|0> + |1>) / sqrt(2)
    qc.h(0)
    
    # Step 2: Entangle all subsequent qubits in a CNOT chain
    # This spreads the superposition to q1, q2, ... qn
    for i in range(n_qubits - 1):
        # Control qubit: i, Target qubit: i+1
        qc.cx(i, i+1)
        
    return qc

def add_measurements(qc: QuantumCircuit):
    n = qc.num_qubits
    qc.measure(range(n), range(n))
    return qc

def run_simulation(qc_with_meas):
    simulator = AerSimulator()
    # Running with 1024 shots to align with standard benchmarking
    job = simulator.run(qc_with_meas, shots=1024)
    result = job.result()
    counts = result.get_counts()
    return counts


# MAIN EXECUTION

if __name__ == "__main__":
    QUBIT_COUNT = 3  
    print(f"=== Creating a {QUBIT_COUNT}-Qubit GHZ State ===")
    
    ghz_base = create_ghz_circuit(QUBIT_COUNT)
    plot_circuit_diagram(ghz_base, title=f"{QUBIT_COUNT}-Qubit GHZ Circuit")
    plot_on_bloch_sphere(ghz_base, title=f"Pre-Measurement State ({QUBIT_COUNT} Quits)")
    ghz_full = add_measurements(ghz_base.copy()) # Copy to keep base circuit clean
    results = run_simulation(ghz_full)
    print("\nSimulation Counts:", results)
    plot_results_histogram(results, title=f"{QUBIT_COUNT}-Qubit GHZ Ideal Simulation")