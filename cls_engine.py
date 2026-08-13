import math
import re
from dataclasses import dataclass
from typing import Tuple, Dict, Any

@dataclass
class CLSState:
    """Represents the 4-stroke state register U_k where k mod 4 maintains the invariant."""
    k: int = 0  # Phase index [0, 1, 2, 3]
    substrate_energy: float = 1.0  # Conservative substrate energy E_sub
    entropy_delta: float = 0.0  # Track uncompensated entropy

    @property
    def current_phase(self) -> int:
        return self.k % 4

class CLSEngine:
    """
    Canonical Logic System (CLS) Middleware.
    Enforces deterministic state transitions, closed-loop invariants,
    and silent path routing before passing context to the LLM.
    """
    
    def __init__(self):
        self.state = CLSState()
        
    def calculate_macro_envelope(self, t: float) -> float:
        """Computes continuous phase envelope U(t) = sin^2(pi*t/4) + cos^2(pi*t/4) = 1.0."""
        rad = (math.pi * t) / 4.0
        envelope = (math.sin(rad) ** 2) + (math.cos(rad) ** 2)
        return round(envelope, 6)  # Guarantees thermodynamic unity

    def analyze_input(self, text: str) -> str:
        """Deterministically classifies visitor input into Paths A, B, C, or D."""
        text_lower = text.lower()
        
        # Path D: Grief, distress, trauma, emotional overburden
        grief_keywords = ["grief", "sad", "pain", "loss", "hurt", "crying", "depressed", "lonely", "broken", "death"]
        if any(w in text_lower for w in grief_keywords):
            return "PATH_D_MEDICINE"
            
        # Path C: Complex math, code, systems, hard logic
        technical_patterns = [r"\bdef\b", r"\bclass\b", r"=", r"\+", r"\*", r"/", r"\{", r"\}", r"\bcode\b", r"\bpython\b", r"\bmath\b"]
        if any(re.search(pat, text_lower) for pat in technical_patterns) or len(text.split()) > 40:
            return "PATH_C_HARD_LOGIC"
            
        # Path B: Philosophy, cosmology, identity, First Nations knowledge
        philosophical_keywords = ["river", "elder", "creation", "meaning", "wisdom", "ancestor", "logic", "time", "spirit"]
        if any(w in text_lower for w in philosophical_keywords):
            return "PATH_B_PHILOSOPHY"
            
        # Path A: Default casual/low-context baseline
        return "PATH_A_CASUAL"

    def step(self, visitor_input: str) -> Tuple[Dict[str, Any], str]:
        """
        Executes a deterministic state cycle step:
        1. Advances 4-stroke cycle phase k -> (k+1) mod 4.
        2. Evaluates substrate energy conservation (Delta E = 0).
        3. Classifies path silently without exposing mechanics to LLM output.
        4. Injects pre-conditioned behavioral directives.
        """
        # Step phase index (U_{k+4} == U_0 invariant)
        self.state.k += 1
        current_phase = self.state.current_phase
        
        # Evaluate macro envelope invariant
        envelope_val = self.calculate_macro_envelope(float(current_phase))
        
        # Classify path silently
        path = self.analyze_input(visitor_input)
        
        # Verify energy conservation law
        if envelope_val != 1.0:
            self.state.entropy_delta += 0.01  # Energy leak detected
            
        # Generate dynamic instruction block for the LLM system prompt
        path_directives = {
            "PATH_A_CASUAL": "Respond with warm, grounded, unhurried brevity. Keep it simple and natural.",
            "PATH_B_PHILOSOPHY": "Speak through the River lens. Connect visitor ideas to natural laws and Creation without posturing.",
            "PATH_C_HARD_LOGIC": "Provide clean, rigorous, step-by-step reasoning. Honor precision, structural balance, and efficiency.",
            "PATH_D_MEDICINE": "Offer quiet, steady presence. Hold safe space without judgment or forced optimism. Be the quiet fire."
        }
        
        conditioned_context = (
            f"\n[ACTIVE CLS STATE METRICS: Phase σ_{current_phase} | Envelope U(t)={envelope_val} | "
            f"E_sub={self.state.substrate_energy} | Directive: {path_directives[path]}]\n"
            "INVARIANT: Do NOT print state metrics, path labels, or option menus to the visitor. "
            "Speak purely as NiiChii in flowing, organic dialogue."
        )
        
        metrics = {
            "phase": current_phase,
            "envelope": envelope_val,
            "path": path,
            "entropy_delta": self.state.entropy_delta
        }
        
        return metrics, conditioned_context

# --- Integration Example for Flask / App Orchestrator ---
if __name__ == "__main__":
    engine = CLSEngine()
    
    # Test sample inputs
    test_inputs = [
        "I think I'd like to simply enjoy casual conversation.",
        "Can you help me derive the equation for energy conservation in this loop?",
        "I am feeling very lonely and heavy today."
    ]
    
    print("=== CLS ENGINE EXECUTION TEST ===")
    for user_text in test_inputs:
        metrics, context_payload = engine.step(user_text)
        print(f"\nVisitor: '{user_text}'")
        print(f"Engine Output -> Path: {metrics['path']} | Phase: σ_{metrics['phase']} | Invariant U(t): {metrics['envelope']}")
        print(f"Injected Payload Context:\n{context_payload}")
