import sys
import subprocess
import re
import time
import random
import math
import struct
import wave
import os

# ANSI Color & Style Palette
COLOR_RESET = "\033[0m"
COLOR_CYAN = "\033[36m"     # Toy Animatronics / Blue
COLOR_RED = "\033[31m"      # Withered / Foxy / Marionette Accent
COLOR_YELLOW = "\033[93m"   # Chica / Golden Freddy
COLOR_PURPLE = "\033[35m"   # Shadow / Bonnie
COLOR_WHITE = "\033[97m"    # The Puppet
COLOR_PINK = "\033[95m"     # Mangle

# Visual Jumpscare Effects
BG_RED_FLASH = "\033[41m\033[97m\033[1m" # Bright Red Background + Bold White Text

# High-Detail ASCII Canvas
ASCII_ART_FNAF2 = {
    "1": fr"""{COLOR_CYAN}
       .---.
      /     \
     | () () |   [ TOY FREDDY ]
      \  =  /
      /`---`\
     /       \
{COLOR_RESET}""",
    "2": fr"""{COLOR_PURPLE}
      /\___/\
     /       \
    |  X   X  |  [ WITHERED BONNIE ]
    |   ___   |  (FACELESS / WIRED)
     \  |||  /
      `-----`
{COLOR_RESET}""",
    "3": fr"""{COLOR_WHITE}
       .---.
      / O O \
     |   |   |   [ THE PUPPET ]
     |  ===  |   (WIND THE MUSIC BOX!)
      \     /
       `---`
{COLOR_RESET}""",
    "4": fr"""{COLOR_RED}
      /\___/\
     /  o O  \   [ WITHERED FOXY ]
    |    V    |  (FLASH LIGHT TO RESET)
     \  ---  /
      `-----`
{COLOR_RESET}""",
    "5": fr"""{COLOR_PINK}
      /\___/\   /|__/\
     /  o O  \ /  o O \   [ MANGLE ]
    (    v    |    V   )  (THE TAKE-APART ATTRACTION)
     \   --- / \  --- /
      `-----`   `-----`
       /|/|/|   |\|\|\
{COLOR_RESET}""",
    "6": fr"""{COLOR_YELLOW}
      / \___/ \
     /   O   O \   [ WITHERED CHICA ]
    |    /---\  |  (UNHINGED JAW / WIRED HANDS)
    |   |     | |
     \   \___/ /
      `-------`
{COLOR_RESET}"""
}

# Jumpscare Screen Canvas
JUMPSCARES = [
    fr"""{BG_RED_FLASH}
       __    __    __    __    __    __
      /  \  /  \  /  \  /  \  /  \  /  \
     ( O  )( O  )( O  )( O  )( O  )( O  )  !!! WITHERED FOXY LUNGES !!!
      \__/  \__/  \__/  \__/  \__/  \__/
     /|  \  /  |  /|  \  /  |  /|  \  /  |
    / |   \/   | / |   \/   | / |   \/   |
{COLOR_RESET}""",
    fr"""{BG_RED_FLASH}
      .=================================.
      |  () ()  [ PUPPET POP-UP ]       |
      |  |||||  GET OUT OF THE OFFICE!  |
      |  (===)                          |
      '================================='
{COLOR_RESET}""",
    fr"""{BG_RED_FLASH}
        /\____/\
       /  X   X \   !!! WITHERED BONNIE FACELESS JUMPSCARE !!!
      |   /---\  |
      |  ||||||| |
       \_______/
{COLOR_RESET}"""
]

# FNaF 2 Fast-Path Hardcoded Overrides
FNAF2_FAST_PATH = {
    r"puppet|music box|marionette": "Wind CAM 11 continuously. If the music box runs out, the Puppet ignores the Freddy Mask entirely and will force a game over.",
    r"withered foxy|foxy": "The Freddy Mask DOES NOT work on Withered Foxy. You must flash your flashlight at him in the hallway 3-4 times to reset his movement timer.",
    r"mangle": "When Mangle reaches the Right Air Vent, equip the Freddy Mask until the static radio noise stops completely.",
    r"withered chica": "If Withered Chica appears in the Right Air Vent or inside the office, put on the Freddy Mask immediately within 0.8 seconds."
}

# Hardened Zero-Latency Firewall Blocklist
FNAF2_HOAXES = [
    "purple guy playable", "shadow bonnie death code", "chrome freddy",
    "kitchen camera visual", "sparky the dog", "save them beatable",
    "ventilation manhole", "manhole", "vents flash red", "hall light fails",
    "clogged vent", "desk cover"
]

def generate_jumpscare_tone(duration=0.8, sample_rate=22050):
    """Synthesizes raw PCM 16-bit audio bytes using sine wave modulation."""
    num_samples = int(duration * sample_rate)
    audio_data = bytearray()
    
    for i in range(num_samples):
        t = i / sample_rate
        freq = 800 - (650 * (i / num_samples))
        noise = random.randint(-2000, 2000)
        
        sample = int(25000 * math.sin(2 * math.pi * freq * t)) + noise
        sample = max(-32768, min(32767, sample))
        
        audio_data.extend(struct.pack('<h', sample))
        
    return bytes(audio_data)

def play_synthetic_audio(pcm_data, sample_rate=22050):
    """Pipes raw PCM math bytes into a temp WAV and outputs via Termux API."""
    wav_path = "jumpscare.wav"
    
    try:
        with wave.open(wav_path, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            f.writeframes(pcm_data)

        subprocess.run(["termux-media-player", "play", wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        pass

def trigger_jumpscare():
    pcm_bytes = generate_jumpscare_tone()
    
    for _ in range(3):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        time.sleep(0.04)
        sys.stdout.write(BG_RED_FLASH)
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        time.sleep(0.04)
        
    print(random.choice(JUMPSCARES))
    play_synthetic_audio(pcm_bytes)
    time.sleep(1.0)

def render_loading_screen():
    bar_width = 20
    print("\033[2J", end="")
    
    for i in range(bar_width + 1):
        progress = "=" * i
        spaces = " " * (bar_width - i)
        percent = int((i / bar_width) * 100)
        
        sys.stdout.write("\033[H")
        sys.stdout.write(f"{COLOR_CYAN}")
        sys.stdout.write("       .---.       \033[K\n")
        sys.stdout.write("      /     \\      \033[K\n")
        sys.stdout.write("     | () () |     [ INITIALIZING ENGINE... ]\033[K\n")
        sys.stdout.write("      \\  =  /      \033[K\n")
        sys.stdout.write("      /`---`\\---o  \033[K\n")
        sys.stdout.write(f"     /       \\  [{progress}>{spaces}] {percent}%\033[K\n")
        sys.stdout.write(f"{COLOR_RESET}")
        sys.stdout.flush()
        time.sleep(0.05)
    
    print("\n[ SYSTEM READY ]\n")
    time.sleep(0.3)

def query_fnaf2_engine(user_question, mode="dispatcher"):
    lower_q = user_question.lower()
    
    # Layer 1: Firewall Intercept
    if any(hoax in lower_q for hoax in FNAF2_HOAXES):
        return "[ENGINE REJECTION]: Query references non-existent FNaF 2 game code, fake mechanics, or hoaxes."

    if mode == "dispatcher":
        # Layer 2: Fast-Path
        for pattern, response in FNAF2_FAST_PATH.items():
            if re.search(pattern, lower_q):
                return f"[FAST-PATH RESPONSE]: {response}"
                
        # Layer 3: LLM Guardrails
        system_framing = (
            "You are an exact numerical UI mechanic guide for Five Nights at Freddy's 2. "
            "ONLY use these exact mechanics: Freddy Mask, Flashlight, Music Box (CAM 11), Main Hallway, Left Vent, Right Vent. "
            "If the user asks about mechanics, objects, or lights that DO NOT exist in FNaF 2 (like desk manholes, red flashing vents, or broken hall lights), state directly: 'That mechanic does not exist in FNaF 2.' "
            "Never invent fake repair steps or non-existent desk items."
        )
    elif mode == "phone_guy":
        system_framing = (
            "You are Phone Guy working the night shift at the 1987 FNaF 2 Freddy Fazbear's Pizza location. "
            "Respond in-character using nervous, casual, recorded-call dialogue style. "
            "Keep responses under 3 sentences."
        )
    elif mode == "foxy":
        system_framing = (
            "You are Withered Foxy lurking in the dark main hallway of the 1987 Freddy Fazbear's Pizza. "
            "You speak like a broken, sinister animatronic pirate who hates bright flashlight beams and masks. "
            "Keep responses aggressive, erratic, pirate-themed, and under 3 sentences."
        )

    full_prompt = f"{system_framing}\n\nUser Input: {user_question}\nResponse:"
    
    # Daemon Auto-Check
    try:
        subprocess.run(["pgrep", "ollama"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        res = subprocess.run(
            ["ollama", "run", "llama3.2:1b", full_prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return f"[Error connecting to local LLM: {e}]"

def show_art():
    while True:
        print("\n--- FNAF 2 CANVAS ART GALLERY ---")
        print("1. Toy Freddy")
        print("2. Withered Bonnie")
        print("3. The Puppet")
        print("4. Withered Foxy")
        print("5. Mangle")
        print("6. Withered Chica")
        print("b. Back")
        
        c = input("\nSelect art: ").strip().lower()
        if c == 'b':
            break
        elif c in ASCII_ART_FNAF2:
            print(ASCII_ART_FNAF2[c])
        else:
            print("Invalid entry.")

def main():
    render_loading_screen()
    
    while True:
        print("========================================")
        print(" FNAF 2: ADVANCED ENGINE & RP SYSTEM ")
        print("========================================")
        print("1. Mechanics Dispatcher Mode")
        print("2. Phone Guy RP Mode")
        print("3. Withered Foxy RP Mode")
        print("4. Open Character Art Canvas")
        print("5. Trigger Random Jumpscare")
        print("q. Quit")
        
        choice = input("\nSelect Option: ").strip().lower()
        if choice == 'q':
            sys.exit(0)
        elif choice == '1':
            q = input("\n[DISPATCHER] Ask about a mechanic: ")
            print(f"\n{query_fnaf2_engine(q, mode='dispatcher')}\n")
        elif choice == '2':
            q = input("\n[PHONE GUY RP] Speak to Phone Guy: ")
            print(f"\n{query_fnaf2_engine(q, mode='phone_guy')}\n")
        elif choice == '3':
            q = input("\n[WITHERED FOXY RP] Talk into the dark hallway: ")
            print(f"\n{query_fnaf2_engine(q, mode='foxy')}\n")
        elif choice == '4':
            show_art()
        elif choice == '5':
            trigger_jumpscare()

if __name__ == "__main__":
    main()

