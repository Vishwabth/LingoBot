import re
import difflib
from spellchecker import SpellChecker
from transformers import pipeline
from .text_rules import apply_text_rules
from .constants import WHITELIST, STOPWORDS

# ----------------------------
# Type Safety Guards
# ----------------------------
assert isinstance(WHITELIST, dict), f"WHITELIST must be dict, got {type(WHITELIST)}"
assert isinstance(STOPWORDS, (set, list, tuple)), f"STOPWORDS must be set/list, got {type(STOPWORDS)}"

# ----------------------------
# Load models
# ----------------------------
grammar_corrector = pipeline(
    "text2text-generation",
    model="pszemraj/flan-t5-large-grammar-synthesis"
)
sentiment_analyzer = pipeline("sentiment-analysis")
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

spell = SpellChecker()

# ----------------------------
# Spellcheck helper
# ----------------------------
def simple_spellcheck(text: str) -> str:
    words = text.split()
    corrected_words = []

    for word in words:
        # Safe whitelist check (dict keys only)
        if word.lower() in WHITELIST.keys() or word[0].isupper():
            corrected_words.append(word)
            continue

        if word.isalpha():
            suggestion = spell.correction(word.lower())
            if suggestion and suggestion != word.lower():
                corrected_words.append(suggestion)
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)

    return " ".join(corrected_words)

# ----------------------------
# Diff report
# ----------------------------
def text_diff(before: str, after: str) -> str:
    """Highlight only meaningful word changes (ignore punctuation noise)."""
    diff = difflib.ndiff(before.split(), after.split())
    changes = []
    for d in diff:
        token = d[2:]
        if token in [".", ",", "!", "?"]:
            continue  # skip standalone punctuation diffs
        if d.startswith("+ "):
            changes.append(f"**{token}**")
        elif d.startswith("- "):
            changes.append(f"~~{token}~~")
        elif d.startswith("  "):
            changes.append(token)
    return " ".join(changes) if changes else "No corrections made ✅"

# ----------------------------
# Safe ML Grammar Correction
# ----------------------------
def safe_correction(original: str, candidate: str) -> str:
    # Token-level similarity
    orig_tokens = original.lower().split()
    cand_tokens = candidate.lower().split()

    # 1. Too much change → reject
    ratio = difflib.SequenceMatcher(None, orig_tokens, cand_tokens).ratio()
    if ratio < 0.75:  # stricter than before
        return original

    # 2. Preserve whitelist words
    for w in WHITELIST.keys():
        if w in orig_tokens and w not in cand_tokens:
            return original

    # 3. Avoid single-word swaps (hallucinations like "python" -> "pigs")
    replaced = sum(1 for o, c in zip(orig_tokens, cand_tokens) if o != c)
    if replaced > len(orig_tokens) * 0.4:
        return original

    return candidate

# ----------------------------
# Main Pipeline
# ----------------------------
def analyze_text(user_input: str):
    results = {}

    # Step 1: Spellcheck
    spellchecked = simple_spellcheck(user_input)
    results["spellcheck"] = spellchecked

    # Step 2: Rule-based correction
    rule_corrected, feedback = apply_text_rules(spellchecked)

    # Step 3: Grammar correction (ML, only if needed)
    try:
        ml_correction = grammar_corrector(rule_corrected, max_length=128, num_beams=4)[0]['generated_text']
        correction = safe_correction(rule_corrected, ml_correction)
    except Exception:
        correction = rule_corrected

    # Step 3.1: Enforce whitelist capitalization
    for w, proper in WHITELIST.items():
        pattern = re.compile(rf"\b{w}\b", flags=re.IGNORECASE)
        correction = pattern.sub(proper, correction)

    # Step 3.2: Prevent STOPWORDS from being capitalized (unless sentence start)
    words = correction.split()
    if len(words) > 1:
        corrected_words = [words[0].capitalize()]  # always capitalize first word
        for w in words[1:]:
            if w.lower() in STOPWORDS:
                corrected_words.append(w.lower())
            else:
                corrected_words.append(w)
        correction = " ".join(corrected_words)

    # Step 4: Ensure capitalization + punctuation
    if correction and not correction[0].isupper():
        correction = correction[0].upper() + correction[1:]
    if correction[-1] not in ".!?":
        correction += "."

    results["grammar"] = correction
    results["feedback"] = feedback
    results["diff"] = text_diff(user_input, correction)

    return results
