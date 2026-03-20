from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, END

from agent.tools import search_log


class AgentState(TypedDict):
    # Inputs
    log_text: str

    # Planning step output
    plan: list[str]

    # Tool call step output
    matches: dict[str, list[str]]

    # Self-reflection step output
    reflection: list[str]

    # Final answer
    category: str
    recommendation: list[str]


def planning_node(state: AgentState) -> AgentState:
    """
    Planning step: decides which patterns to search for.
    """
    state["plan"] = [
        "No files were found with the provided path",
        "SpotBugs",
        "Checkstyle",
        "jacoco",
        "JUnit",
        "exit code",
        "ERROR:",
        "FAILURE:",
    ]

    print("\n--- Planning step ---")
    print("Plan:", state["plan"])
    return state


def tool_call_node(state: AgentState) -> AgentState:
    """
    Tool call step: searches the log text.
    """
    print("\n--- Tool call step (search_log) ---")
    state["matches"] = search_log(state["log_text"], state["plan"])

    if state["matches"]:
        for pattern, lines in state["matches"].items():
            print(f"\nMatches for: {pattern}")
            # Print only first 3 lines for readability.
            for l in lines[:3]:
                print(" -", l)
    else:
        print("No matches found for planned patterns.")

    return state


def self_reflection_node(state: AgentState) -> AgentState:
    """
    Self-reflection step: validate classification based on evidence.
    """
    print("\n--- Self-reflection step ---")
    reflection: list[str] = []

    if "No files were found with the provided path" in state["matches"]:
        reflection.append("There is evidence of missing build report artifacts.")

    if any("SpotBugs" in k for k in state["matches"].keys()):
        reflection.append("SpotBugs-related keywords appeared in logs.")

    if any("Checkstyle" in k for k in state["matches"].keys()):
        reflection.append("Checkstyle-related keywords appeared in logs.")

    if "exit code" in state["matches"]:
        reflection.append("The log shows a non-zero exit code indicator.")

    if not reflection:
        reflection.append("Evidence is weak; classification should remain tentative.")

    state["reflection"] = reflection

    for r in reflection:
        print(" -", r)
    return state


def final_answer_node(state: AgentState) -> AgentState:
    """
    Final answer: category + recommendation.
    """
    print("\n--- Final answer (classification) ---")

    if "No files were found with the provided path" in state["matches"]:
        state["category"] = "Reports/Artifacts missing (pipeline didn’t generate expected outputs)"
        state["recommendation"] = [
            "Check whether `gradle check` actually ran to completion before artifact upload.",
            "Ensure tasks that generate reports run: Checkstyle, JaCoCo, SpotBugs.",
            "Inspect CI console output around the Gradle failure (look for ERROR/FAILURE).",
            "Make artifact upload paths match the actual report directories.",
        ]
    elif "Checkstyle" in state["matches"]:
        state["category"] = "Style/Checkstyle failure"
        state["recommendation"] = [
            "Open the Checkstyle report output (CI artifacts).",
            "Fix formatting/style violations and re-run the pipeline.",
        ]
    elif "SpotBugs" in state["matches"]:
        state["category"] = "SAST/SpotBugs failure"
        state["recommendation"] = [
            "Review the SpotBugs findings in the CI artifacts.",
            "Suppress only specific false positives; fix real issues where possible.",
        ]
    else:
        state["category"] = "Unknown / mixed failure (insufficient log evidence)"
        state["recommendation"] = [
            "Provide the full Gradle output (the part near ERROR/FAILURE).",
            "Ensure the workflow prints the last N lines of Gradle before uploading artifacts.",
        ]

    print("Category:", state["category"])
    print("Recommendations:")
    for rec in state["recommendation"]:
        print(" -", rec)

    return state


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("planning", planning_node)
    g.add_node("tool_call", tool_call_node)
    g.add_node("self_reflection", self_reflection_node)
    g.add_node("final", final_answer_node)

    g.set_entry_point("planning")
    g.add_edge("planning", "tool_call")
    g.add_edge("tool_call", "self_reflection")
    g.add_edge("self_reflection", "final")
    g.add_edge("final", END)
    return g.compile()


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify CI/CD failures from logs.")
    parser.add_argument("--log-file", required=True, help="Path to a CI log text file")
    args = parser.parse_args()

    log_path = Path(args.log_file)
    log_text = log_path.read_text(encoding="utf-8", errors="ignore")

    app = build_graph()

    # Initial state
    state: AgentState = {
        "log_text": log_text,
        "plan": [],
        "matches": {},
        "reflection": [],
        "category": "",
        "recommendation": [],
    }

    _ = app.invoke(state)


if __name__ == "__main__":
    main()

