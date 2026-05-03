"""

Quantum Logic Playground — visualization.py                                                                           
Central visualization module for all quantum circuits.         
Supports: Circuit diagrams, Bloch spheres, probability         
histograms, density matrices, Q-sphere plots.        

"""

import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

matplotlib.use("Agg")

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace
from qiskit_aer import AerSimulator
from qiskit.visualization import (
    plot_histogram,
    plot_bloch_multivector,
    plot_bloch_vector,
    plot_state_city,
    plot_state_qsphere,
    plot_state_hinton,
    circuit_drawer,
)


# Global Style
# ─────────────────────────────────────────────────────────────────

STYLE = {
    "bg":      "#0d1117",
    "panel":   "#161b22",
    "accent":  "#58a6ff",
    "accent2": "#3fb950",
    "accent3": "#f78166",
    "text":    "#e6edf3",
    "subtext": "#8b949e",
    "grid":    "#21262d",
}

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _apply_dark_style() -> None:
    plt.rcParams.update({
        "figure.facecolor":  STYLE["bg"],
        "axes.facecolor":    STYLE["panel"],
        "axes.edgecolor":    STYLE["grid"],
        "axes.labelcolor":   STYLE["text"],
        "axes.titlecolor":   STYLE["text"],
        "xtick.color":       STYLE["subtext"],
        "ytick.color":       STYLE["subtext"],
        "text.color":        STYLE["text"],
        "grid.color":        STYLE["grid"],
        "grid.linestyle":    "--",
        "grid.alpha":        0.6,
        "font.family":       "monospace",
        "figure.dpi":        130,
        "savefig.dpi":       150,
        "savefig.bbox":      "tight",
        "savefig.facecolor": STYLE["bg"],
    })

_apply_dark_style()


# 1. Circuit Diagram
# ─────────────────────────────────────────────────────────────────

def plot_circuit(
    circuit: QuantumCircuit,
    title: str = "Quantum Circuit",
    filename: str | None = None,
    style: str = "iqp-dark",
    fold: int = -1,
) -> str:
    fig, ax = plt.subplots(figsize=(max(8, circuit.num_qubits * 2), 4))
    fig.patch.set_facecolor(STYLE["bg"])

    circuit_drawer(circuit, output="mpl", style=style, fold=fold, ax=ax, initial_state=True)
    ax.set_title(title, color=STYLE["accent"], fontsize=14, pad=12, fontweight="bold")

    return _save(fig, filename or f"circuit_{title.lower().replace(' ', '_')}.png")



# 2. Probability Histogram
# ─────────────────────────────────────────────────────────────────

def plot_measurement_histogram(
    counts: dict[str, int],
    title: str = "Measurement Results",
    shots: int | None = None,
    filename: str | None = None,
    color: str | None = None,
) -> str:
    bar_color = color or STYLE["accent"]

    fig = plot_histogram(counts, color=bar_color, bar_labels=True, figsize=(10, 5), title=None)
    fig.patch.set_facecolor(STYLE["bg"])
    ax = fig.axes[0]
    ax.set_facecolor(STYLE["panel"])
    ax.tick_params(colors=STYLE["subtext"])
    for spine in ax.spines.values():
        spine.set_edgecolor(STYLE["grid"])
    ax.yaxis.grid(True, color=STYLE["grid"], linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)

    fig.suptitle(title, color=STYLE["accent"], fontsize=14, fontweight="bold", y=1.02)
    if shots:
        ax.set_title(f"{shots:,} shots", color=STYLE["subtext"], fontsize=10, pad=6)

    total = sum(counts.values())
    for bar in ax.patches:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + total * 0.005,
                f"{h / total:.1%}",
                ha="center", va="bottom",
                color=STYLE["text"], fontsize=9,
            )

    return _save(fig, filename or f"histogram_{title.lower().replace(' ', '_')}.png")



# 3. Bloch Sphere
# ─────────────────────────────────────────────────────────────────

def plot_bloch(
    circuit: QuantumCircuit,
    title: str = "Bloch Sphere",
    filename: str | None = None,
    qubit_index: int | None = None,
) -> str:
    sv = Statevector.from_instruction(circuit)
    n = circuit.num_qubits

    if qubit_index is not None or n == 1:
        idx = qubit_index or 0
        keep = list(range(n))
        keep.remove(idx)
        dm = partial_trace(sv, keep) if keep else DensityMatrix(sv)
        fig = plot_bloch_vector(_dm_to_bloch_vector(dm), title=title, figsize=(5, 5))
    else:
        fig = plot_bloch_multivector(sv, title=title, figsize=(5 * n, 5))

    fig.patch.set_facecolor(STYLE["bg"])
    fig.suptitle(title, color=STYLE["accent"], fontsize=14, fontweight="bold")
    return _save(fig, filename or f"bloch_{title.lower().replace(' ', '_')}.png")


def _dm_to_bloch_vector(dm: DensityMatrix) -> list[float]:
    rho = dm.data
    return [2 * rho[0, 1].real, 2 * rho[0, 1].imag, (rho[0, 0] - rho[1, 1]).real]



# 4. Density Matrix (City Plot)
# ─────────────────────────────────────────────────────────────────

def plot_density_matrix(
    circuit: QuantumCircuit,
    title: str = "Density Matrix",
    filename: str | None = None,
) -> str:
    sv = Statevector.from_instruction(circuit)
    fig = plot_state_city(sv, title=title, figsize=(10, 6))
    fig.patch.set_facecolor(STYLE["bg"])
    fig.suptitle(title, color=STYLE["accent"], fontsize=14, fontweight="bold")
    return _save(fig, filename or f"density_{title.lower().replace(' ', '_')}.png")



# 5. Q-Sphere
# ─────────────────────────────────────────────────────────────────

def plot_qsphere(
    circuit: QuantumCircuit,
    title: str = "Q-Sphere",
    filename: str | None = None,
) -> str:
    sv = Statevector.from_instruction(circuit)
    fig = plot_state_qsphere(sv, figsize=(8, 8))
    fig.patch.set_facecolor(STYLE["bg"])
    fig.suptitle(title, color=STYLE["accent"], fontsize=14, fontweight="bold")
    return _save(fig, filename or f"qsphere_{title.lower().replace(' ', '_')}.png")



# 6. Hinton Diagram
# ─────────────────────────────────────────────────────────────────

def plot_hinton(
    circuit: QuantumCircuit,
    title: str = "Hinton Diagram",
    filename: str | None = None,
) -> str:
    sv = Statevector.from_instruction(circuit)
    fig = plot_state_hinton(sv, title=title, figsize=(8, 6))
    fig.patch.set_facecolor(STYLE["bg"])
    fig.suptitle(title, color=STYLE["accent"], fontsize=14, fontweight="bold")
    return _save(fig, filename or f"hinton_{title.lower().replace(' ', '_')}.png")


# 7. Full Analysis Dashboard
# ─────────────────────────────────────────────────────────────────

def full_analysis(
    circuit: QuantumCircuit,
    label: str = "State",
    shots: int = 1024,
    save_individual: bool = True,
) -> dict[str, str]:
    paths: dict[str, str] = {}
    slug = label.lower().replace(" ", "_").replace("|", "").replace("⟩", "").replace("⟨", "")

    if save_individual:
        paths["circuit"] = plot_circuit(circuit, title=f"{label} — Circuit", filename=f"{slug}_circuit.png")

    meas_circuit = circuit.copy()
    meas_circuit.measure_all()
    counts = AerSimulator().run(meas_circuit, shots=shots).result().get_counts()

    if save_individual:
        paths["histogram"] = plot_measurement_histogram(counts, title=f"{label} — Histogram", shots=shots, filename=f"{slug}_histogram.png")
        paths["bloch"]     = plot_bloch(circuit, title=f"{label} — Bloch", filename=f"{slug}_bloch.png")
        paths["qsphere"]   = plot_qsphere(circuit, title=f"{label} — Q-Sphere", filename=f"{slug}_qsphere.png")
        paths["density"]   = plot_density_matrix(circuit, title=f"{label} — Density Matrix", filename=f"{slug}_density.png")
        paths["hinton"]    = plot_hinton(circuit, title=f"{label} — Hinton", filename=f"{slug}_hinton.png")

    sv = Statevector.from_instruction(circuit)
    paths["dashboard"] = _build_dashboard(circuit, sv, counts, label, shots, f"{slug}_dashboard.png")

    print(f"\n✅  Analysis complete for: {label}")
    for name, p in paths.items():
        print(f"    [{name:>12}] → {p}")
    return paths


# Dashboard


def _build_dashboard(circuit, sv, counts, label, shots, filename) -> str:
    fig = plt.figure(figsize=(22, 14), facecolor=STYLE["bg"])
    fig.suptitle(f"Quantum Logic Playground  ·  {label}", color=STYLE["accent"], fontsize=18, fontweight="bold", y=0.97)

    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.38, wspace=0.3, left=0.05, right=0.97, top=0.90, bottom=0.06)

    ax_circ = fig.add_subplot(gs[0, 0])
    circuit_drawer(circuit, output="mpl", style="iqp-dark", ax=ax_circ, initial_state=True)
    ax_circ.set_title("Circuit Diagram", color=STYLE["accent2"], fontsize=11, pad=8)

    ax_hist = fig.add_subplot(gs[0, 1])
    _draw_histogram_on_ax(ax_hist, counts, shots)
    ax_hist.set_title(f"Measurement Histogram  ({shots:,} shots)", color=STYLE["accent2"], fontsize=11, pad=8)

    for idx, (gs_pos, plot_fn, title) in enumerate([
        (gs[0, 2], lambda: plot_bloch_multivector(sv, figsize=(6, 4)), "Bloch Sphere(s)"),
        (gs[1, 0], lambda: plot_state_qsphere(sv, figsize=(5, 5)),     "Q-Sphere"),
        (gs[1, 1], lambda: plot_state_city(sv, figsize=(6, 5)),        "Density Matrix (City)"),
        (gs[1, 2], lambda: plot_state_hinton(sv, figsize=(6, 5)),      "Hinton Diagram"),
    ]):
        ax = fig.add_subplot(gs_pos)
        ax.axis("off")
        ax.set_title(title, color=STYLE["accent2"], fontsize=11, pad=8)
        sub_fig = plot_fn()
        sub_fig.canvas.draw()
        buf = np.frombuffer(sub_fig.canvas.tostring_rgb(), dtype=np.uint8)
        buf = buf.reshape(sub_fig.canvas.get_width_height()[::-1] + (3,))
        ax.imshow(buf)
        plt.close(sub_fig)

    fig.text(0.5, 0.01, "Quantum Logic Playground  ·  github.com/erdemersozlu", ha="center", color=STYLE["subtext"], fontsize=8)
    return _save(fig, filename)


def _draw_histogram_on_ax(ax, counts, shots) -> None:
    states = sorted(counts.keys())
    values = [counts[s] for s in states]
    total  = sum(values)
    probs  = [v / total for v in values]
    colors = [STYLE["accent"] if p == max(probs) else STYLE["subtext"] for p in probs]

    bars = ax.bar(states, probs, color=colors, width=0.5, zorder=3, edgecolor=STYLE["bg"])
    for bar, p in zip(bars, probs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{p:.1%}", ha="center", va="bottom", color=STYLE["text"], fontsize=9)

    ax.set_facecolor(STYLE["panel"])
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Probability", color=STYLE["subtext"], fontsize=9)
    ax.set_xlabel("Basis State",  color=STYLE["subtext"], fontsize=9)
    ax.tick_params(colors=STYLE["subtext"])
    ax.yaxis.grid(True, color=STYLE["grid"], linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_edgecolor(STYLE["grid"])



# Utility
# ─────────────────────────────────────────────────────────────────

def _save(fig, filename) -> str:
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path)
    plt.close(fig)
    return path


# Smoke-test  →  python visualization.py
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    full_analysis(bell, label="Bell State |Φ+⟩")

    ghz = QuantumCircuit(3)
    ghz.h(0)
    ghz.cx(0, 1)
    ghz.cx(0, 2)
    full_analysis(ghz, label="GHZ State")