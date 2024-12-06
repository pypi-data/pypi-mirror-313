from typing import List


def calculate_similarity(a: str, b: str) -> float:
    """Calculate string similarity using Levenshtein distance."""
    if len(a) == 0 or len(b) == 0:
        return 0.0

    distance = levenshtein_distance(a.lower(), b.lower())
    max_length = max(len(a), len(b))
    return (max_length - distance) / max_length


def levenshtein_distance(a: str, b: str) -> int:
    """Calculate Levenshtein distance between strings."""
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)

    matrix = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        matrix[i][0] = i
    for j in range(len(b) + 1):
        matrix[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            )

    return matrix[len(a)][len(b)]


def round_decimal(value: float, precision: int) -> float:
    """Round a float to specified precision."""
    return round(value, precision)