# 🐻 FNaF 2 Engine & RP Dispatcher 

An authentic, feature-complete Five Nights at Freddy's 2 terminal assistant and roleplay simulation built specifically for Android via **Termux**, powered by a local **Ollama** LLM instance (`llama3.2:1b`).

![License](https://img.shields.io/badge/license-MIT-red.svg)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Android-green.svg)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)

---

## ⚡ Core Features

* **3-Layer Defense Architecture:**
  * **Layer 1 (Zero-Latency Firewall):** Blocks community hoaxes, fake mechanics, and fan-made myths (e.g., *desk covers, ventilation manholes, red flashing vents*) before touching the model.
  * **Layer 2 (Deterministic Fast-Path):** Instant regex-matched responses for core gameplay mechanics (Puppet music box timer, Withered Foxy flashlight resets).
  * **Layer 3 (Guardrailed LLM):** Local `llama3.2:1b` engine constrained strictly to official FNaF 2 lore and mechanics.
* **Pure Math Audio Synthesis:**
  * Generates PCM jumpscare sound waves programmatically via sine modulation and uniform random noise equations:
    $$y(t) = A \cdot \sin(2\pi \cdot f(t) \cdot t) + \text{noise}$$
  * Writes sample streams directly to valid WAV structures and outputs via `termux-media-player` to bypass Android terminal sandbox locks.
* **Interactive TUI & ASCII Gallery:** Animated Toy Freddy progress loader, ANSI color schemes, and canvas art gallery.

---

## 📋 Prerequisites

Before running the application, make sure you have installed the required Termux packages and pulled the local model:

```bash
# Update and install dependencies
pkg update && pkg upgrade -y
pkg install python git termux-api -y

# Install and start Ollama
pkg install ollama -y
ollama serve > /dev/null 2>&1 &
ollama pull llama3.2:1b
