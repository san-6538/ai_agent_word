# main.py
from voice_assistant import listen
import torch

if __name__ == "__main__":
    device = "GPU" if torch.cuda.is_available() else "CPU"
    print(f"🎤 Voice-controlled AI Word Agent started using {device}.")
    print("Say a command (or just start dictating). Say 'exit' to quit.\n")
    listen()
