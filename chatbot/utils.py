import difflib

def text_diff(before: str, after: str) -> str:
    """Return a simple diff between before and after text for highlighting changes."""
    diff = difflib.ndiff(before.split(), after.split())
    changes = []
    for d in diff:
        if d.startswith("+ "):
            changes.append(f"**{d[2:]}**")  # additions bold
        elif d.startswith("- "):
            changes.append(f"~~{d[2:]}~~")  # deletions strikethrough
        elif d.startswith("  "):
            changes.append(d[2:])
    return " ".join(changes)
