# word_controller.py
import win32com.client
from win32com.client import constants
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import config
from text_generator import generate_text as hf_generate_text

# ---------------- Microsoft Word Initialization ----------------
_word_app = None
_doc = None
_action_stack = []  # For undo functionality

def _init_word():
    global _word_app, _doc
    if _word_app is None:
        _word_app = win32com.client.Dispatch("Word.Application")
        _word_app.Visible = True
        print("[Word] Microsoft Word opened.")
    if _word_app.Documents.Count == 0 or _doc is None:
        _doc = _word_app.Documents.Add()
        print("[Word] New document created.")

# ---------------- Core Operations ----------------
def new_document():
    global _doc
    _init_word()
    _doc = _word_app.Documents.Add()
    print("[Word] New document created.")

def save_document(path=config.WORD_SAVE_PATH):
    _doc.SaveAs(path)
    print(f"[Word] Document saved at {path}")

def close_document():
    _doc.Close(False)
    print("[Word] Document closed.")

def write_text(text):
    _init_word()
    sel = _word_app.Selection
    sel.TypeText(text)
    sel.TypeParagraph()
    _action_stack.append(("insert", text))
    print(f"[Word] Written: {text}")

def generate_text(topic="AI"):
    """Generate text using Gemini API via text_generator.py"""
    text = hf_generate_text(topic)
    write_text(text)

# ---------------- Formatting ----------------
def bold(on=True):
    _word_app.Selection.Font.Bold = on
    print(f"[Word] Bold {'ON' if on else 'OFF'}")

def italic(on=True):
    _word_app.Selection.Font.Italic = on
    print(f"[Word] Italic {'ON' if on else 'OFF'}")

def underline(on=True):
    _word_app.Selection.Font.Underline = on
    print(f"[Word] Underline {'ON' if on else 'OFF'}")

def align_left():
    _word_app.Selection.ParagraphFormat.Alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    print("[Word] Aligned Left")

def align_right():
    _word_app.Selection.ParagraphFormat.Alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    print("[Word] Aligned Right")

def align_center():
    _word_app.Selection.ParagraphFormat.Alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    print("[Word] Aligned Center")

def align_justify():
    _word_app.Selection.ParagraphFormat.Alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    print("[Word] Justified")

def add_page_border():
    _doc.Sections(1).Borders.Enable = True
    print("[Word] Page border added.")

def bullet_points():
    _word_app.Selection.Range.ListFormat.ApplyBulletDefault()
    print("[Word] Bullet points applied")

def font_increase():
    _word_app.Selection.Font.Size += 2
    print("[Word] Font size increased")

def font_decrease():
    _word_app.Selection.Font.Size = max(1, _word_app.Selection.Font.Size - 2)
    print("[Word] Font size decreased")

# ---------------- Delete / Undo ----------------
def delete_last_word():
    sel = _word_app.Selection
    sel.MoveLeft(Unit=constants.wdWord, Count=1, Extend=1)
    deleted_text = sel.Text
    sel.Delete()
    _action_stack.append(("delete", deleted_text))
    print(f"[Word] Last word deleted: '{deleted_text}'")

def delete_last_line():
    sel = _word_app.Selection
    sel.MoveUp(Unit=constants.wdLine, Count=1, Extend=1)
    deleted_text = sel.Text
    sel.Delete()
    _action_stack.append(("delete", deleted_text))
    print(f"[Word] Last line deleted: '{deleted_text}'")

def delete_last_paragraph():
    sel = _word_app.Selection
    sel.MoveUp(Unit=constants.wdParagraph, Count=1, Extend=1)
    deleted_text = sel.Text
    sel.Delete()
    _action_stack.append(("delete", deleted_text))
    print(f"[Word] Last paragraph deleted: '{deleted_text}'")

def undo_last_action():
    if not _action_stack:
        print("[Word] Nothing to undo.")
        return
    action, content = _action_stack.pop()
    sel = _word_app.Selection
    if action == "insert":
        sel.MoveLeft(Unit=constants.wdWord, Count=len(content.split()), Extend=1)
        sel.Delete()
        print(f"[Word] Undo: removed inserted text '{content}'")
    elif action == "delete":
        sel.TypeText(content)
        print(f"[Word] Undo: restored deleted text '{content}'")

# ---------------- Expose Commands for Voice Assistant ----------------
COMMANDS = {
    "write text": write_text,
    "generate text": generate_text,
    "bold": bold,
    "italic": italic,
    "underline": underline,
    "align left": align_left,
    "align right": align_right,
    "align center": align_center,
    "justify": align_justify,
    "add page border": add_page_border,
    "new document": new_document,
    "save document": save_document,
    "close document": close_document,
    "bullet points": bullet_points,
    "font increase": font_increase,
    "font decrease": font_decrease,
    "delete last word": delete_last_word,
    "delete last line": delete_last_line,
    "delete last paragraph": delete_last_paragraph,
    "undo": undo_last_action,
}

# ---------------- Main Initialization ----------------
if __name__ == "__main__":
    _init_word()
    write_text("Hello! AI Word Agent is ready.")
