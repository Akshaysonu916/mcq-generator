DOMAIN_KEYWORDS = {
    "python": ["python", "django", "flask", "pandas", "numpy"],
    "mernstack": ["react", "node.js", "mongodb", "express.js"],
    "flutter": ["flutter", "dart", "mobile app", "cross-platform"],
    "java": ["java", "spring", "hibernate"],
    "data science": ["machine learning", "deep learning", "tensorflow", "scikit-learn"]
}

def detect_domain(resume_text):
    resume_text_lower = resume_text.lower()
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}

    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in resume_text_lower:
                scores[domain] += 1

    # Pick the domain with the highest score
    best_domain = max(scores, key=scores.get)
    return best_domain if scores[best_domain] > 0 else None
