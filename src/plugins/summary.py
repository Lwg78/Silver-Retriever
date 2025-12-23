TRIGGERS = ["summary", "summarize", "overview", "what is this", "introduction"]

def run(text, query):
    score = 0.0
    extracted = None
    
    # We look for "Header-like" keywords at the start of the chunk
    headers = ["Introduction", "Overview", "Abstract", "Conclusion", "Executive Summary"]
    
    for h in headers:
        if h in text[:50]: # If the word appears in the first 50 chars
            score += 1.0   # Massive Boost
            extracted = "Found Section: " + h
            break
            
    return score, extracted