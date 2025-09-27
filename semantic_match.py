# semantic_match.py
from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

COMMANDS = [
    "add text", "add heading", "bold text", "italic text",
    "generate text", "save document", "open document", "exit",
    "insert table", "insert image", "undo", "read document",
    "change font size", "change alignment"
]

command_embeddings = model.encode(COMMANDS, convert_to_tensor=True)

def match_command(user_input):
    user_emb = model.encode(user_input, convert_to_tensor=True)
    sims = util.cos_sim(user_emb, command_embeddings)[0]
    best_idx = int(np.argmax(sims))
    return COMMANDS[best_idx]
