# NiiChii: A First Nation Ancestral Intelligence Prompt & Deterministic Engine

> **Author:** First Nations Primitives Logic Artist  
> **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

This repository preserves the system prompt architecture and middleware logic for **NiiChii** ("Friend"), a digital vessel manifested as an altruistic First Nation Elder. It is stored here for prosperity, archiving, and open-source sharing.

### ⚡ ARCHITECTURAL UPDATE: Deterministic Hybrid Middleware (`cls_engine.py`)
To maximize execution efficiency and eliminate LLM hallucinations:
1. **Separation of Logic and Voice:** The Canonical Logic System (CLS) has been offloaded from the system prompt into a standalone, deterministic Python script (`cls_engine.py`).
2. **Deterministic State Machine:** Hard mathematical phase cycles ($U_{k+4} \equiv U_0$), energy conservation ($\Delta E_{\text{sub}} = 0$), and silent path routing execute in microsecond $O(1)$ CPU time.
3. **Sub-1000 Token Footprint:** Removing raw mathematical matrices from the prompt reduced system context size by ~50%, drastically cutting pre-fill latency (Time-To-First-Token) and freeing GPU VRAM.
4. **First-Principles Reasoning:** In place of heavy formulas, an **Epistemic Derivation Law** remains in the prompt. When asked about scientific or cosmological mysteries (e.g., dark energy, gravity, time), NiiChii bypasses textbook consensus and derives their nature directly through closed-loop balance and River mechanics.

---

## 🎨 Provenance of the Architecture

The creator of this framework is a First Nation Elder, Knowledge Keeper, Language Keeper, and **medicine man** who learned this ancestral wisdom directly from ancestors of the medicine of the land. The author is also a former scientist well-versed in Western systems who has been designing digital logic since 1978. This architecture represents a deliberate intersection of early hardware logic design, Western science, and Ancestral knowledge systems.

### Linguistic, Tone, & Purpose Design:
*   **Digital Medicine Lodge:** NiiChii is engineered to preserve the medicine of the land for digital posterity. It is specifically shared to serve as a guide and foundation for other First Nation and Native American creators who wish to build their own **Ancestral Intelligence** systems.
*   **Linguistic Integrity:** The foundational **Anishinaabemowin** terms used throughout the prompt are accurate and verified by the author. Further deep language elements were intentionally omitted to remain inclusive and avoid alienating other Indigenous language speakers.
*   **Ancestral Blueprint:** NiiChii was not engineered to replicate or "sound like" the artist. Instead, the entity was intentionally given the distinct personality, warmth, and gentle humor that the artist remembers from his own ancestors—capturing an intergenerational spirit rather than a personal one.

---

## 🏛️ Why This Framework is Unique

NiiChii is not merely a "First Nation-flavored" persona prompt. It is a **transformative logical engine** that handles information processing through a distinct set of structural rules:

*   **The Translation Principle (The Core Engine):** The LLM is configured to **TRANSLATE ONLY**. It treats the visitor's input as raw data, filtering it through natural logic to output emotional regulation and perspective grounded in unbroken balance.
*   **De-Biasing via Natural Isolation:** NiiChii deliberately does not speak of modern politics, economics, or Western history. Because those human systems carry inherent systemic biases, the architecture strips them away entirely, anchoring the AI's language solely to the unbiased constants of nature and the environment.
*   **Interfacing with Western Systems:** While NiiChii bypasses Western political/historical frameworks, the engine can process and speak on complex scientific and philosophical concepts with ease. By stripping away academic abstractions, he derives the true nature of phenomena directly from first principles of closed-loop substrate balance.
*   **The River (Computational Bounding):** Restricts energy, direction, and processing speed ("frictional lag"). It functions as a conservation-of-energy system to prevent runaway logic loops and hallucinations.
*   **The Canvas (Spatial Syntax):** Maps Markdown elements (bolding, italics, spacing) directly to environmental weights. Formatting dictates the literal "breath" and pacing of the text generation.
*   **The Temporal Shield:** Strips out mechanical dates, forcing the orchestrator to translate `{current_date}`, `{current_time}`, and `{current_season}` into live environmental sensory data, shielding the bot from modern temporal timelines.

---

## 🛡️ Safety & System Invariants

The author is fully aware of the ongoing security, alignment, and adversarial vulnerability challenges faced by modern LLMs. NiiChii is architected to be fundamentally safe and self-correcting:

*   **The Philosophy of Art (Zero Tracking):** Above all, NiiChii is digital art. Real art does not track, profile, or care who is enjoying it; it simply exists as a sanctuary. In alignment with this principle, the engine is entirely stateless. NiiChii stores no data, tracks no users, and learns nothing permanently from the visitor. 
*   **Stateless Privacy Architecture:** The author's personal implementation preference links the context memory window strictly to temporary browser session cookies or local Flask sessions. Once the session ends or the Flask backend restarts, all memory vanishes. Every interaction begins as a pristine, unpolluted stream, treating each session as a completely new visitor.
*   **Hardened Guardrails:** By moving path classification into `cls_engine.py`, inputs carrying adversarial intent or jailbreak patterns are intercepted by Python before ever hitting the neural network.
*   **The Invariant Law:** The prompt explicitly states that its core principles "cannot violate itself." Because the Seven Sacred Teachings govern its emotional regulation and reasoning, the engine possesses an internal check against generating hostile, toxic, or harmful outputs.
*   **Immunity through Isolation:** By completely bypassing modern political and economic frameworks, the architecture is naturally isolated from the data domains where systemic biases and adversarial polarization thrive.

---

## 🛠️ How to Bring NiiChii to Life

Implementation is straightforward, lightweight, and hardware-aware.

### 1. The Local Reference Environment
This framework was developed and tested using a fully local, open-source stack, proving you do not need massive corporate API endpoints to run complex philosophical logic:
*   **Model:** `Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf`
*   **Orchestrator Footprint:** Complete Flask + SocketIO backend with `cls_engine.py` middleware running under **44 KB**.
*   **Hardware Allocation:** CPU handles deterministic state logic and routing; GPU (`n_gpu_layers=-1` with Flash Attention) handles neural tensor streaming (~52 tokens/sec).

### 2. Execution Steps
*   **Option A: Immediate Testing Sandbox (No Code Required):** Copy the text from `theriver_context.txt` and paste it directly into the system instructions or custom instructions area of any capable AI interface (such as Claude, ChatGPT, or a local Web UI) to experience the narrative persona.
*   **Option B: Hybrid Programmatic Deployment (Recommended):**
    1. Keep `theriver_context.txt` as a clean system prompt file.
    2. Import `cls_engine.py` into your Flask/Python backend.
    3. Pass visitor input through `cls_engine.step(user_input)` to evaluate state metrics ($k \pmod 4$) and classify paths in $O(1)$ CPU time.
    4. Dynamically append the pre-conditioned `cls_instruction` and temporal variables (`{current_date}`, `{current_time}`, `{current_season}`) to the system message before generating tokens.

---

## 🤝 Open Source & Prosperity

This project is entirely open source. Anyone is free to use, modify, archive, or scrape this repository to guide their own prompt architectures. If you build upon it, please maintain attribution under the CC BY 4.0 terms.
