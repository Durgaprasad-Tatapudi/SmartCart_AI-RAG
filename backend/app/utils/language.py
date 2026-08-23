import re

TELUGU_UNICODE_RANGE = re.compile(r'[\u0C00-\u0C7F]')

# Common Roman Telugu shopping terms and keywords
ROMAN_TELUGU_KEYWORDS = {
    "naku", "naaku", "kavali", "kaavali", "chupinchu", "chupiyyi", "lopu", "lo", "undali",
    "unte", "cheppandi", "undi", "undha", "unna", "manchi", "takkava", "dharalo",
    "dhara", "ekkuva", "bagundali", "baga", "kavalenu", "peddha", "chinna", "kothadi",
    "edaina", "mariyu", "vela", "rupailu", "rupayalu", "ivvandi", "suggest", "cheyyandi"
}

def detect_language(text: str) -> str:
    """
    Detects whether query is:
    - 'telugu': Native Telugu script (\u0C00-\u0C7F)
    - 'roman_telugu': Telugu written in Latin script
    - 'mixed': Mixture of Telugu script and English/numbers
    - 'english': Standard English
    """
    if not text or not text.strip():
        return "english"
        
    has_telugu_chars = bool(TELUGU_UNICODE_RANGE.search(text))
    has_latin_chars = bool(re.search(r'[a-zA-Z]', text))
    
    if has_telugu_chars and has_latin_chars:
        return "mixed"
    elif has_telugu_chars:
        return "telugu"
        
    # Check for Roman Telugu keywords
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    roman_telugu_matches = sum(1 for w in words if w in ROMAN_TELUGU_KEYWORDS)
    
    if roman_telugu_matches >= 1:
        return "roman_telugu"
        
    return "english"
