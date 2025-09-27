# voice_assistant.py
import sounddevice as sd
import numpy as np
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import word_controller
import config

# ---------------- Init Models ----------------
print("[Init] Loading Hugging Face ASR model...")
asr = pipeline("automatic-speech-recognition", model=config.HF_ASR_MODEL, device=0)  # GPU if available

print("[Init] Loading SentenceTransformer for command matching...")
semantic_model = SentenceTransformer(config.HF_SEMANTIC_MODEL)

# ---------------- Supported Commands ----------------
COMMANDS = {
    "write text": word_controller.write_text,
    "bold": word_controller.bold,
    "italic": word_controller.italic,
    "underline": word_controller.underline,
    "align left": word_controller.align_left,
    "align right": word_controller.align_right,
    "align center": word_controller.align_center,
    "justify": word_controller.align_justify,
    "add page border": word_controller.add_page_border,
    "new document": word_controller.new_document,
    "save document": word_controller.save_document,
    "close document": word_controller.close_document,
    "generate text": word_controller.generate_text,
    "delete last word": word_controller.delete_last_word,
    "delete last line": word_controller.delete_last_line,
    "delete last paragraph": word_controller.delete_last_paragraph,
    "undo": word_controller.undo_last_action,
    "start dictation": "start_dictation"  # special mode
}

COMMAND_LIST = list(COMMANDS.keys())
COMMAND_EMB = semantic_model.encode(COMMAND_LIST, convert_to_tensor=True)

# ---------------- Helper Functions ----------------
def match_command(spoken_text, threshold=0.6):
    """Find best matching command using semantic similarity."""
    query_emb = semantic_model.encode(spoken_text, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, COMMAND_EMB)[0]
    best_idx = int(scores.argmax())
    best_score = float(scores[best_idx])
    if best_score >= threshold:
        return COMMAND_LIST[best_idx], best_score
    return None, best_score

def record_audio(duration=5, sr=16000):
    """Record audio from microphone."""
    print("[Listening...] Speak now...")
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()

def transcribe_audio(audio):
    """Use Hugging Face ASR to transcribe audio."""
    try:
        result = asr(audio, chunk_length_s=5, return_timestamps=False)
        text = result["text"].strip().lower()
        if text:
            print(f"[You]: {text}")
        return text
    except Exception as e:
        print(f"[ASR Error]: {e}")
        return ""

# ---------------- Main Listening Loop ----------------
def listen():
    """Continuous assistant loop until 'exit' command."""
    dictation_mode = False

    print("[Assistant] Running... Say a command (say 'exit' to stop).")
    while True:
        audio = record_audio(duration=5)
        spoken_text = transcribe_audio(audio)
        if not spoken_text:
            continue

        # Exit assistant
        if "exit" in spoken_text:
            print("[Assistant] Exiting...")
            break

        # Check if we are in dictation mode
        if dictation_mode:
            if "stop dictation" in spoken_text:
                dictation_mode = False
                print("[Assistant] Dictation stopped.")
            else:
                word_controller.write_text(spoken_text)
            continue

        # Match semantic command
        matched_cmd, score = match_command(spoken_text)

        if matched_cmd:
            print(f"[Matched Command]: {matched_cmd} (score: {score:.2f})")
        else:
            print("[Fallback] No command matched. Treating as text input.")
            matched_cmd = "write text"

        # Execute command
        try:
            if matched_cmd == "write text":
                cleaned_text = spoken_text.replace("write text", "").replace("insert text", "").strip()
                word_controller.write_text(cleaned_text or "This is sample text.")
            elif matched_cmd == "generate text":
                topic = spoken_text.replace("generate text", "").strip()
                word_controller.generate_text(topic or "AI")
            elif matched_cmd == "start dictation":
                dictation_mode = True
                print("[Assistant] Dictation mode ON. Speak freely...")
            else:
                COMMANDS[matched_cmd]()
        except Exception as e:
            print(f"[Error executing '{matched_cmd}']: {e}")
