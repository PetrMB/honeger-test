"""Fuzzy matching utilities (migrated from check-sales-improved.py)"""
from difflib import SequenceMatcher

def normalize_product_name(name: str) -> str:
    """Normalize product name for matching."""
    name_lower = name.lower()
    # Remove common suffixes
    suffixes = [' osivo', ' sazenice', ' pytlíčky', ' granule', ' krmivo', ' stelivo']
    for suffix in suffixes:
        if name_lower.endswith(suffix):
            name_lower = name_lower[:-len(suffix)].strip()
    return name_lower

def fuzzy_match(a: str, b: str) -> float:
    """
    Calculate similarity between two strings (0-1).
    Returns higher score for better matches.
    """
    a_norm = normalize_product_name(a)
    b_norm = normalize_product_name(b).replace('-', ' ')
    
    # Calculate base similarity
    base_score = SequenceMatcher(None, a_norm, b_norm).ratio()
    
    # Check for stem/prefix matching
    a_words = set(a_norm.split())
    b_words = set(b_norm.split())
    
    stem_match = False
    for a_word in a_words:
        if len(a_word) < 3:
            continue
        for b_word in b_words:
            if len(b_word) < 3:
                continue
            min_len = min(len(a_word), len(b_word), 4)
            if a_word[:min_len] == b_word[:min_len]:
                stem_match = True
                break
        if stem_match:
            break
    
    if stem_match:
        return min(1.0, base_score + 0.35)
    
    # Exact word match bonus
    common_words = a_words & b_words
    if common_words:
        boost = min(0.3, len(common_words) * 0.15)
        return min(1.0, base_score + boost)
    
    return base_score
