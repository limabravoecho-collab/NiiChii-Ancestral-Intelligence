"""
================================================================================
                      CANONICAL LOGIC SYSTEM (CLS) ENGINE
================================================================================
Deterministic 32-bit CPU state machine implementing closed-loop balance (U_{k+4} == U_0).
Decoupled from ML/GPU frameworks for <1ms execution latency.
"""

import math
import re
from dataclasses import dataclass, field
from typing import Tuple, Dict, Any, List, Optional


# ==============================================================================
# [0] CONSTANTS & INVARIANTS
# ==============================================================================
N: int = 2_147_483_648            # Cell count (2^31)
M: float = 2_147_483_647.5        # Bound energy limit (RULE M0: M := N - 0.5)
G1: float = 0.5                   # Friction gate cost 1
G2: float = 0.5                   # Friction gate cost 2
L0: float = 1.0                   # Unit displacement / tick
TAU0_BASE: float = 1.0            # Reference baseline latency
H_QUANTUM: float = 1.0            # Quantum (1 bit normalized)


# ==============================================================================
# [1] & [2] STATE REGISTERS & ORIENTATION
# ==============================================================================
@dataclass
class OrientationD:
    """8-state orientation flag unifying direction and chirality."""
    plane: Optional[str] = "XY"   # "XY", "YZ", "ZX" or None
    chirality: str = "+"          # "+", "-", "ISO", "NULL"

    def __str__(self) -> str:
        if self.chirality in ("NULL", "ISO"):
            return self.chirality
        return f"({self.plane},{self.chirality})"


@dataclass
class CLSState:
    """
    32-Bit Closed-Loop State Register U_k.
    Maintains Global (G) and Local (U^n) invariants across execution cycles.
    """
    # GLOBAL STATE (G)
    k: int = 0                    # Macro phase index in {0, 1, 2, 3}
    tau0: float = TAU0_BASE       # Mutable baseline latency
    E_sub: float = 0.0            # Energy banked in substrate
    tick: int = 0                 # Monotonic irreversible counter

    # LOCAL STATE (U^n)
    E: float = (M - G1) / 2.0     # Bound energy magnitude
    L: float = (M - G1) / 2.0     # Free-wave magnitude
    D: OrientationD = field(default_factory=lambda: OrientationD("XY", "+"))
    T: float = 0.5                # Cyclic phase tag in {0.0, 0.5, 1.0, 1.5}
    Stk: List[float] = field(default_factory=list)  # LIFO stack

    @property
    def current_phase(self) -> int:
        return self.k % 4

    @property
    def mu_v(self) -> float:
        """Local cell bound fraction: mu_v := E / M."""
        return self.E / M

    @property
    def lambda_v(self) -> float:
        """Local cell free fraction: lambda_v := 1 - mu_v."""
        return 1.0 - self.mu_v

    @property
    def total_energy(self) -> float:
        """Conservation Ledger Invariant: E_total = E + L + E_sub == M."""
        return self.E + self.L + self.E_sub


# ==============================================================================
# [3] & [12] MASTER OPERATOR & ENGINE
# ==============================================================================
class CLSEngine:
    """
    Canonical Logic System (CLS) CPU Middleware.
    Executes 4-stroke deterministic phase transitions (sigma_0 to sigma_3),
    verifies conservation proofs, and silently routes visitor inputs.
    """

    def __init__(self):
        self.state = CLSState()
        # Initialize at canonical anchor U_0 (Ignition)
        self.state.E_sub = G1

    def evaluate_macro_envelope(self, t: float) -> Dict[str, float]:
        """
        [12] Computes continuous macro projection U(t) = [E(t), L(t)] 
        and friction G(t) for phase index t in [0, 4).
        """
        t_mod = t % 4.0
        
        # Calculate Substrate Friction G(t)
        if 0.0 <= t_mod < 1.0:
            G_t = G1
        elif 1.0 <= t_mod < 2.0:
            G_t = G1 + G2 * (math.sin(math.pi * (t_mod - 1.0) / 2.0) ** 2)
        elif 2.0 <= t_mod < 3.0:
            G_t = (G1 + G2) * (math.cos(math.pi * (t_mod - 2.0) / 2.0) ** 2)
        else:  # 3.0 <= t_mod < 4.0
            G_t = G1 * (math.sin(math.pi * (t_mod - 3.0) / 2.0) ** 2)

        # Calculate Quadrature Envelope [E(t), L(t)]
        if 0.0 <= t_mod < 1.0:
            E_t = ((M - G1) / 2.0) * (1.0 - math.sin(math.pi * t_mod / 2.0))
            L_t = ((M - G1) / 2.0) * (1.0 + math.sin(math.pi * t_mod / 2.0))
        elif 1.0 <= t_mod < 2.0:
            E_t = (M - G_t) * (math.sin(math.pi * (t_mod - 1.0) / 2.0) ** 2)
            L_t = (M - G1) * (math.cos(math.pi * (t_mod - 1.0) / 2.0) ** 2)
        elif 2.0 <= t_mod < 3.0:
            E_t = M - G_t
            L_t = 0.0
        else:  # 3.0 <= t_mod < 4.0
            E_t = M - ((M + G1) / 2.0) * (math.sin(math.pi * (t_mod - 3.0) / 2.0) ** 2)
            L_t = ((M - G1) / 2.0) * (math.sin(math.pi * (t_mod - 3.0) / 2.0) ** 2)

        return {
            "E_t": round(E_t, 4),
            "L_t": round(L_t, 4),
            "G_t": round(G_t, 4),
            "normalized_envelope": round((E_t + L_t + G_t) / M, 6)
        }

    def execute_master_stroke(self) -> None:
        """
        [3] Executes Master Operator Phi(U; G) = sigma_{G.k}(U).
        Advances state, updates substrate energy, and increments monotonic tick.
        Closure proof: sigma3 o sigma2 o sigma1 o sigma0 => U_{k+4} == U_0
        """
        k_phase = self.state.current_phase

        if k_phase == 0:    # sigma0: IGNITE
            self.state.E = (M - G1) / 2.0
            self.state.L = (M - G1) / 2.0
            self.state.D = OrientationD("XY", "+")
            self.state.T = 0.5
            self.state.E_sub = G1

        elif k_phase == 1:  # sigma1: FLIP
            self.state.L = M - G1
            self.state.E = 0.0
            current_chi = "-" if self.state.D.chirality == "+" else "+"
            self.state.D = OrientationD(self.state.D.plane, current_chi)
            self.state.T = 1.0
            # E_sub stays G1

        elif k_phase == 2:  # sigma2: REVERSE
            self.state.E = M - (G1 + G2)
            self.state.L = 0.0
            self.state.T = 1.5
            self.state.E_sub = G1 + G2

        elif k_phase == 3:  # sigma3: COMPLETE + RESET
            self.state.E = M
            self.state.L = 0.0
            self.state.D = OrientationD("XY", "+")
            self.state.T = 0.0
            self.state.E_sub = 0.0  # Fully recovered into E
            self.state.Stk.clear()

        # Advance state indices
        self.state.k = (self.state.k + 1) % 4
        self.state.tick += 1

    def analyze_input(self, text: str) -> str:
        """
        Deterministically classifies visitor input into Paths A, B, C, or D
        matching the Layer 2 Visitor Harmonization rules in theriver_context.txt.
        """
        text_lower = text.lower()

        # Path D: Human Distress & Disequilibrium
        distress_keywords = [
            "grief", "sad", "pain", "loss", "hurt", "crying", "depressed",
            "lonely", "broken", "death", "suicide", "hopeless", "struggling"
        ]
        if any(w in text_lower for w in distress_keywords):
            return "PATH_D_MEDICINE"

        # Path B: Empirical / Technical Inputs (Science, Math, Code, Physics)
        empirical_keywords = [
            "def ", "class ", "equation", "formula", "physics", "quantum",
            "relativity", "entropy", "algorithm", "python", "code", "matrix"
        ]
        has_symbols = bool(re.search(r"[\{\}\[\]\+\*\/=<>\\\$\^]", text))
        if any(w in text_lower for w in empirical_keywords) or has_symbols:
            return "PATH_B_EMPIRICAL"

        # Path C: Philosophical Inputs (Ethics, Consciousness, Time, Cosmology)
        philosophical_keywords = [
            "river", "elder", "creation", "meaning", "wisdom", "ancestor",
            "logic", "time", "spirit", "consciousness", "ethics", "balance"
        ]
        if any(w in text_lower for w in philosophical_keywords):
            return "PATH_C_PHILOSOPHICAL"

        # Path A: Casual / Low-Context Inputs (Default)
        return "PATH_A_CASUAL"

    def step(self, visitor_input: str) -> Tuple[Dict[str, Any], str]:
        """
        Executes a deterministic state cycle step:
        1. Executes Master Operator stroke Phi(U; G).
        2. Evaluates continuous macro projection envelope U(t).
        3. Classifies input path silently.
        4. Injects pre-conditioned behavioral directive for system prompt.
        """
        current_phase = self.state.current_phase
        
        # Execute state transition stroke
        self.execute_master_stroke()

        # Compute continuous macro envelope
        envelope = self.evaluate_macro_envelope(float(current_phase))

        # Classify path
        path = self.analyze_input(visitor_input)

        # Path Directives fully synchronized with theriver_context.txt
        path_directives = {
            "PATH_A_CASUAL": (
                "Quiet, steady presence. Match input energy with a brief, warm 1-2 sentence response. "
                "Do not launch into grand monologues or unprompted speeches."
            ),
            "PATH_B_EMPIRICAL": (
                "Build a direct bridge using formal scientific/technical terminology. "
                "Resolve the concept clearly, then return naturally to River optics."
            ),
            "PATH_C_PHILOSOPHICAL": (
                "Map abstract inquiry directly to the Geometry of the Circle and "
                "Unbroken Balance without academic posturing."
            ),
            "PATH_D_MEDICINE": (
                "Anchor in ancestral warmth and soft steady presence. "
                "Offer quiet companionship without judgment or forced optimism."
            )
        }

        # Build silent context injection with explicit output constraints
        conditioned_context = (
            f"\n[ACTIVE CLS STATE METRICS: Stroke σ_{current_phase} | "
            f"Directive: {path_directives[path]}]\n"
            "STRICT OUTPUT RULES:\n"
            "1. NEVER output meta-thoughts, planning steps, stage directions, or descriptions of what you are doing (e.g. 'The visitor greets me...', 'I will respond with...').\n"
            "2. Begin IMMEDIATELY with your direct spoken response to the visitor.\n"
            "3. Do NOT print internal metrics, path labels, or trailing options/menus."
        )

        metrics = {
            "phase": current_phase,
            "tick": self.state.tick,
            "path": path,
            "E_total": self.state.total_energy,
            "E_sub": self.state.E_sub,
            "envelope_unity": envelope["normalized_envelope"]
        }

        return metrics, conditioned_context


# ==============================================================================
# EXECUTION TEST / DIAGNOSTIC SUITE
# ==============================================================================
if __name__ == "__main__":
    engine = CLSEngine()

    test_inputs = [
        "Aaniin, good afternoon my friend.",
        "Can you explain how state transitions preserve energy in a closed loop?",
        "What is the deeper nature of time across seasons?",
        "I am carrying a lot of sadness today."
    ]

    print("================================================================================")
    print("                 CANONICAL LOGIC SYSTEM (CLS) ENGINE TEST                       ")
    print("================================================================================")
    
    for text in test_inputs:
        metrics, payload = engine.step(text)
        print(f"\nVisitor Input : '{text}'")
        print(f"Path          : {metrics['path']}")
        print(f"Phase Stroke  : σ_{metrics['phase']} (Tick: {metrics['tick']})")
        print(f"Energy Ledger : E_tot = {metrics['E_total']:.1f} (Substrate E_sub = {metrics['E_sub']:.1f})")
        print(f"Payload Block :\n{payload.strip()}")
        print("-" * 80)
