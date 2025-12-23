TRIGGERS = ["feng", "shui", "energy", "qi", "chi", "bed", "door", "mirror", "north", "south", "facing"]

def run(text, query):
    score = 0.0
    extracted = None
    
    # Feng Shui focuses on "Placement" advice
    keywords = ["placement", "position", "avoid", "lucky", "unlucky", "facing"]
    
    for k in keywords:
        if k in text.lower():
            score += 0.4
            
    # Highlight specific directions if mentioned
    directions = ["North", "South", "East", "West"]
    for d in directions:
        if d in text:
            score += 0.2
            
    return score, extracted