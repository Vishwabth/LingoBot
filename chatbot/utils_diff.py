from chatbot.utils import text_diff

def generate_diff_report(original: str, corrected: str) -> str:
    """Create a readable diff report between original and corrected text."""
    if original.strip() == corrected.strip():
        return "No corrections made ✅"
    return text_diff(original, corrected)
