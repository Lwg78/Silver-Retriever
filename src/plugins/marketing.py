TRIGGERS = ["marketing", "seo", "sem", "click", "conversion", "funnel", "ads", "traffic"]

def run(text, query):
    score = 0.0
    extracted = None
    
    # Prioritize Definitions of Acronyms
    if "SEO" in text and "Search Engine Optimization" in text:
        score += 0.6
        extracted = "Definition: SEO"
        
    if "SEM" in text and "Search Engine Marketing" in text:
        score += 0.6
        extracted = "Definition: SEM"

    return score, extracted