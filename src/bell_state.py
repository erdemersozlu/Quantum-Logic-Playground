"""
Quantum Logic Playground: Bell State Implementation
Author: [Taha Erdem Ersözlü]
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def create_bell_state():
    qc = QuantumCircuit(2, 2)
    qc.h(0)

    qc.cx(0, 1)

    qc.measure([0, 1], [0, 1])
    
    return qc

def run_simulation(qc):
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts()
    return counts

if __name__ == "__main__":
    bell_circuit = create_bell_state()
    print("bell state circuit is ready")
    print(bell_circuit)
    
    results = run_simulation(bell_circuit)
    print("\nSonuçlar (Counts):", results)
    
    plot_histogram(results)
    plt.show()