import re

TRIGGERS = ["deadline", "due", "date", "when", "task", "deliverable", "submission"]

def run(text, query):
    score = 0.0
    extracted = None
    reason = None
    
    # Logic 1: Find Dates
    date_pattern = r"(\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})"
    match = re.search(date_pattern, text, re.IGNORECASE)
    
    if match:
        score += 0.5 
        reason = "Contains Date" # <--- NEW REASONING
        
        if "deadline" in query or "when" in query:
             extracted = match.group(1)

    # Logic 2: Find Tasks
    if "task" in query and "Task" in text:
        score += 0.4
        reason = "Matches Task Header"
            
    return score, extracted, reason