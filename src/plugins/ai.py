TRIGGERS = ["ai", "agent", "model", "neural", "network", "llm", "transformer", "robot"]

def run(text, query):
    score = 0.0
    extracted = None
    
    # Boost Definitions
    if "is a" in text or "refers to" in text:
        score += 0.3
        
    # Boost Key AI Concepts
    concepts = ["supervised", "unsupervised", "reinforcement", "attention mechanism"]
    for c in concepts:
        if c in text.lower():
            score += 0.4
            
    return score, extracted