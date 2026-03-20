from __future__ import annotations


def search_log(log_text: str, patterns: list[str]) -> dict[str, list[str]]:
    """
    Simple "tool call" that searches the provided CI log text.

    Returns: pattern -> list of matching lines (trimmed).
    """
    lines = log_text.splitlines()
    results: dict[str, list[str]] = {p: [] for p in patterns}

    for line in lines:
        for p in patterns:
            if p.lower() in line.lower():
                results[p].append(line.strip())

    # Remove empty entries for readability.
    return {p: matches for p, matches in results.items() if matches}

