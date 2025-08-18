import re
import spacy

nlp = spacy.load("en_core_web_sm")

def apply_text_rules(text: str):
    """
    Rule-based grammar and style corrections.
    Returns (corrected_text, feedback_list).
    """
    doc = nlp(text)
    feedback = []
    corrected = text

    # 1. POS-based rules
    has_subject = any(t.dep_ == "nsubj" for t in doc)
    has_verb = any(t.pos_ == "VERB" for t in doc)
    if not has_subject:
        feedback.append("❗ Critical: Sentence may be missing a subject.")
    if not has_verb:
        feedback.append("❗ Critical: Sentence may be missing a verb.")

    # 2. Subject–Verb Agreement
    for token in doc:
        if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            if token.tag_ in ["NN", "NNP"] and token.head.tag_ in ["VBP", "VB"]:
                feedback.append("❗ Subject-verb agreement issue: singular subject with plural/base verb.")
                corrected = corrected.replace(token.head.text, token.head.text + "s")
            if token.tag_ == "NNS" and token.head.tag_ == "VBZ":
                feedback.append("❗ Subject-verb agreement issue: plural subject with singular verb.")
                corrected = corrected.replace(token.head.text, token.head.lemma_)

    # 3. Article usage
    for token in doc:
        if token.pos_ == "NOUN" and token.dep_ in ["dobj", "pobj", "nsubj"]:
            if not any(c.dep_ == "det" for c in token.children):
                feedback.append(f"ℹ️ Missing article before '{token.text}'.")

    # 4. Double negatives
    if re.search(r"\b(?:no|not|never)\b.*\b(?:no|not|never)\b", text.lower()):
        feedback.append("❗ Double negative detected — check intended meaning.")

    # 5. Tense consistency
    verbs = [t.tag_ for t in doc if t.pos_ == "VERB"]
    if len(set(verbs)) > 1 and any(v.startswith("VBD") for v in verbs) and any(v.startswith(("VBZ", "VBP")) for v in verbs):
        feedback.append("⚠️ Inconsistent verb tense — consider aligning tense.")

    # 6. Pronoun–Antecedent Agreement
    if ("they" in text.lower() or "them" in text.lower()) and ("he" in text.lower() or "she" in text.lower()):
        feedback.append("❗ Pronoun-antecedent agreement issue — mismatch in subject/pronoun.")

    # 7. Common Homophone Confusions
    homophones = {
        "their": "they're/there",
        "your": "you're",
        "its": "it's",
        "then": "than",
        "affect": "effect"
    }
    for wrong, right in homophones.items():
        if re.search(rf"\b{re.escape(wrong)}\b", text.lower()):
            feedback.append(f"⚠️ Check if '{wrong}' is correct; maybe you meant '{right}'.")

    # 🔥 Upgrade: auto-correct "its" → "it's"
    if re.search(r"\bits\b", corrected.lower()):
        corrected = re.sub(r"\bits\b", "it's", corrected, flags=re.IGNORECASE)
        feedback.append("⚠️ Replaced 'its' with 'it's' (contraction).")

    # 🔥 Upgrade: suggest comma before "it's"
    if re.search(r"\bit'?s\b", corrected.lower()):
        feedback.append("ℹ️ Consider adding a comma before 'it's' for readability.")

    # 8. Punctuation
    if corrected and corrected[-1] not in ".!?":
        feedback.append("ℹ️ Sentence should end with punctuation.")
        corrected += "."

    if len(re.findall(r"[.!?]", text)) == 0 and len(text.split()) > 20:
        feedback.append("⚠️ Possible run-on sentence — consider splitting.")

    # 9. Capitalization
    if corrected and not corrected[0].isupper():
        feedback.append("ℹ️ Sentence should start with a capital letter.")
        corrected = corrected[0].upper() + corrected[1:]

    # 10. Passive voice
    for token in doc:
        if token.dep_ == "auxpass":
            feedback.append("⚠️ Passive voice detected — consider rewriting in active voice.")

    # 11. Parallelism (fixed regex)
    # 11. Parallelism (fixed regex)
    if "," in text or " and " in text.lower() or " or " in text.lower():
        try:
            items = [w.strip() for w in re.split(r"(?:,|\s+(?:and|or)\s+)", text, flags=re.IGNORECASE)]
            items = [i for i in items if i]  # remove empties
            if len(items) >= 2:
                forms = []
                for i in items:
                    doc_item = nlp(i.strip())
                    if len(doc_item) > 0:
                        forms.append(doc_item[0].pos_)
                if len(set(forms)) > 1:
                    feedback.append("⚠️ Possible parallelism issue in list/series.")
        except re.error as e:
            feedback.append(f"⚠️ Regex error (parallelism): {e}")


    return corrected.strip(), feedback
