import spacy
from datetime import datetime, timedelta

nlp = spacy.load("en_core_web_sm")

# ---------------- NLP Parsing ---------------- #

def parse_task_from_text(text):
    """
    Parse a natural language task description into structured fields.
    Example: "Remind me to submit report by Friday"
    Returns: title, description, deadline (ISO string)
    """
    doc = nlp(text)
    title = text  # fallback
    deadline = None

    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            try:
                deadline = parse_natural_date(ent.text)
                title = text.replace(ent.text, "").strip().capitalize()
            except:
                continue

    return title, text, deadline

def parse_natural_date(text):
    """
    Convert natural language date to ISO format.
    Example: "tomorrow" => "2025-04-05"
    """
    text = text.lower()
    now = datetime.now()

    if "today" in text:
        return now.isoformat()
    elif "tomorrow" in text:
        return (now + timedelta(days=1)).isoformat()
    elif "next week" in text:
        return (now + timedelta(days=7)).isoformat()
    elif "friday" in text:
        days_ahead = (4 - now.weekday()) % 7  # Friday = 4
        return (now + timedelta(days=days_ahead)).isoformat()

    raise ValueError("Unrecognized date format")

# ---------------- Priority Suggestion ---------------- #

def suggest_priority(title, description):
    keywords = {
        "high": ["urgent", "asap", "immediately", "critical", "important"],
        "medium": ["soon", "next", "important"],
        "low": ["whenever", "someday", "optional", "low"]
    }
    combined = f"{title.lower()} {description.lower()}"
    for level, words in keywords.items():
        if any(word in combined for word in words):
            return level.capitalize()
    return "Medium"

# ---------------- Scheduling Helper ---------------- #

def is_task_delayed(deadline_str, status):
    if not deadline_str or status.lower() == "done":
        return False
    deadline = datetime.fromisoformat(deadline_str)
    now = datetime.now()
    return deadline < now + timedelta(days=1)  # approaching or past

def suggest_status(deadline_str):
    if not deadline_str:
        return "To Do"
    deadline = datetime.fromisoformat(deadline_str)
    now = datetime.now()
    if deadline < now:
        return "Overdue"
    elif deadline.date() == now.date():
        return "Due Today"
    return "Upcoming"
