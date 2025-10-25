#!/usr/bin/env python3
"""
Grade Calculator (interactive)

Features:
- Define grading components (e.g., Homework, Midterm, Final) and their weights.
- Enter scores for one or many students.
- Computes final percentage and maps to a letter grade.
- Validates weights and normalizes if they don't sum to 100.
- Easy to adapt for different grading scales.

Usage: python grade_calculator.py
"""
from typing import List, Tuple, Dict


DEFAULT_SCALE = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
    (0,  "F"),
]


def input_positive_float(prompt: str) -> float:
    while True:
        try:
            v = float(input(prompt).strip())
            if v < 0:
                print("Please enter a non-negative number.")
                continue
            return v
        except ValueError:
            print("Invalid number, try again.")


def get_components() -> List[Tuple[str, float]]:
    print("Define grading components and their weights (e.g., Homework 30, Midterm 30, Final 40).")
    comps: List[Tuple[str, float]] = []
    while True:
        name = input("Component name (or press Enter to finish): ").strip()
        if not name:
            if comps:
                break
            else:
                print("You must add at least one component.")
                continue
        weight = input_positive_float(f"Weight for '{name}' (as percent, e.g., 30): ")
        comps.append((name, weight))
    total = sum(w for _, w in comps)
    if abs(total - 100.0) > 1e-6:
        print(f"Total weights sum to {total:.2f}%. We'll normalize the weights so they add up to 100%.")
        comps = [(n, w * 100.0 / total) for n, w in comps]
    return comps


def get_student_scores(components: List[Tuple[str, float]]) -> Dict[str, float]:
    name = input("Student name (or press Enter to cancel student entry): ").strip()
    if not name:
        return {}
    scores: Dict[str, float] = {"__name__": name}
    for comp_name, _ in components:
        s = input_positive_float(f"Score for {comp_name} (enter absolute score; use same scale for all components): ")
        scores[comp_name] = s
    return scores


def compute_percentage(scores: Dict[str, float], components: List[Tuple[str, float]]) -> float:
    # The function assumes that the maximum possible for every component is the same scale the user used.
    # To support different maxima you'd need to collect max scores per component.
    total = 0.0
    for comp_name, weight in components:
        total += scores.get(comp_name, 0.0) * (weight / 100.0)
    return total


def letter_grade(percent: float, scale=DEFAULT_SCALE) -> str:
    for cutoff, letter in scale:
        if percent >= cutoff:
            return letter
    return "F"


def main():
    print("Welcome to the interactive Grade Calculator.\n")
    components = get_components()
    print("\nComponents and normalized weights:")
    for n, w in components:
        print(f" - {n}: {w:.2f}%")
    students: List[Dict[str, float]] = []
    print("\nEnter student scores. Press Enter at student name prompt to finish.")
    while True:
        s = get_student_scores(components)
        if not s:
            break
        students.append(s)

    if not students:
        print("No students entered. Exiting.")
        return

    print("\nResults:")
    for s in students:
        name = s["__name__"]
        percent = compute_percentage(s, components)
        grade = letter_grade(percent)
        print(f"{name}: {percent:.2f}% -> {grade}")

    print("\nDone.")


if __name__ == "__main__":
    main()
