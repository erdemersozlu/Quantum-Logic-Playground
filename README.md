# 🌀 Quantum Logic Playground

Welcome to the **Quantum Logic Playground**! This repository is a curated collection of fundamental quantum algorithms and circuits. It serves as a technical sandbox to explore the core principles of quantum mechanics—such as **Superposition** and **Entanglement**—through practical implementation.

## 🚀 Overview
Before building complex hybrid models, one must master the "atomic" units of quantum computing: **Quantum Gates** and **Qubit Manipulation**. This project documents my journey in mastering these basics using **Qiskit**.

Each algorithm in this collection includes:
1.  **The Logic:** Mathematical background.
2.  **The Circuit:** Python implementation using Qiskit.
3.  **The Analysis:** Visualizing results via Histograms and Bloch Spheres.

---

## 🛠 Tech Stack
* **Language:** Python 3.x
* **Framework:** [Qiskit](https://qiskit.org/)
* **Simulators:** Qiskit Aer
* **Visualization:** Matplotlib, Qiskit Visualization Tools

---

## 📚 Algorithm Collection

### 1. Bell State ($|\Phi^+\rangle$)
The "Hello World" of quantum entanglement. This circuit demonstrates how two qubits can be perfectly correlated.
* **Gates used:** Hadamard ($H$), Controlled-NOT ($CX$).
* **Concept:** Creating a maximally entangled state where the outcome of one qubit determines the other.
* **[View Code](./src/bell_state.py)**

### 2. GHZ State (Greenberger–Horne–Zeilinger)
Taking entanglement further by involving three or more qubits.
* **Gates used:** $H$, multiple $CX$ gates in a chain.
* **Concept:** Multi-qubit entanglement, which is highly sensitive to noise—making it a perfect test for quantum hardware stability.
* **[View Code](./src/ghz_state.py)**

### 3. Bloch Sphere Exploration (Coming Soon)
A visual deep-dive into single-qubit rotations and the geometric representation of quantum states.

---

## 📊 Visualizing Results
Quantum computing is probabilistic. In this playground, every circuit is backed by a statistical analysis:

* **Circuit Diagrams:** Visualizing the gate sequence.
* **Probability Histograms:** Observing the collapse of the wave function after 1024 shots.
* **Hardware Comparison:** *Note: For a deep dive into how these circuits perform on real quantum hardware (IQM Spark), check out my [Quantum Hardware Analysis]https://github.com/erdemersozlu/Quantum-Entanglement-Benchmark-on-Real-QPU-Simulator-vs.-Lagrange-IQM repository.*

---

## ⚙️ Installation & Usage
Clone the repository:
```bash
git clone https://github.com/erdemersozlu/Quantum-Logic-Playground
cd quantum-logic-playground
```

Install dependencies:
```bash
pip install qiskit qiskit-aer matplotlib
```

Run the Bell State simulation:
```bash
python src/bell_state.py
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

