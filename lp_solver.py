"""Transparent two-variable linear programming solver.

The solver deliberately enumerates boundary intersections so the graphical
method remains visible to students instead of hiding the calculation behind a
black-box optimizer.
"""

from dataclasses import dataclass
from math import isclose, isfinite
from typing import Sequence


EPSILON = 1e-9
RELATIVE_EPSILON = 1e-10


@dataclass(frozen=True)
class Constraint:
    """A less-than-or-equal resource constraint: a*x + b*y <= rhs."""

    name: str
    a: float
    b: float
    rhs: float


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Candidate:
    point: Point
    source: str
    feasible: bool
    reason: str
    objective_value: float


@dataclass(frozen=True)
class SolveResult:
    candidates: tuple[Candidate, ...]
    vertices: tuple[Point, ...]
    optimal_points: tuple[Point, ...]
    objective_value: float
    resource_usage: tuple[float, ...]
    slacks: tuple[float, ...]


def _validate_input(objective: Sequence[float], constraints: Sequence[Constraint]) -> None:
    if len(objective) != 2:
        raise ValueError("La funcion objetivo debe tener exactamente dos variables.")
    if not constraints:
        raise ValueError("Debe existir al menos una restriccion.")

    values = list(objective)
    for constraint in constraints:
        values.extend((constraint.a, constraint.b, constraint.rhs))

    if not all(isfinite(value) for value in values):
        raise ValueError("Todos los valores deben ser numeros finitos.")
    if any(value < 0 for value in objective):
        raise ValueError("Las utilidades no pueden ser negativas.")
    for constraint in constraints:
        if constraint.a < 0 or constraint.b < 0:
            raise ValueError("El consumo de recursos no puede ser negativo.")
        if constraint.rhs < 0:
            raise ValueError("La disponibilidad de recursos no puede ser negativa.")


def _intersection(
    first: tuple[float, float, float],
    second: tuple[float, float, float],
) -> Point | None:
    a1, b1, c1 = first
    a2, b2, c2 = second
    determinant = a1 * b2 - b1 * a2
    determinant_scale = max(abs(a1 * b2), abs(b1 * a2), 1e-300)
    if abs(determinant) <= RELATIVE_EPSILON * determinant_scale:
        return None

    x = (c1 * b2 - b1 * c2) / determinant
    y = (a1 * c2 - c1 * a2) / determinant
    return Point(x, y)


def _is_feasible(point: Point, constraints: Sequence[Constraint]) -> bool:
    if point.x < -EPSILON * max(1.0, abs(point.x)) or point.y < -EPSILON * max(1.0, abs(point.y)):
        return False
    return all(
        constraint.a * point.x + constraint.b * point.y
        <= constraint.rhs + EPSILON * max(1.0, abs(constraint.rhs))
        for constraint in constraints
    )


def _deduplicate(points: Sequence[Point]) -> tuple[Point, ...]:
    unique: list[Point] = []
    for point in points:
        if any(
            isclose(point.x, saved.x, rel_tol=EPSILON, abs_tol=EPSILON)
            and isclose(point.y, saved.y, rel_tol=EPSILON, abs_tol=EPSILON)
            for saved in unique
        ):
            continue
        unique.append(Point(max(0.0, point.x), max(0.0, point.y)))
    return tuple(sorted(unique, key=lambda value: (value.x, value.y)))


def _feasibility_reason(point: Point, constraints: Sequence[Constraint]) -> str:
    if point.x < -EPSILON * max(1.0, abs(point.x)):
        return "x es negativa"
    if point.y < -EPSILON * max(1.0, abs(point.y)):
        return "y es negativa"
    for constraint in constraints:
        used = constraint.a * point.x + constraint.b * point.y
        tolerance = EPSILON * max(1.0, abs(constraint.rhs))
        if used > constraint.rhs + tolerance:
            return f"supera el recurso {constraint.name}"
    return "cumple todas las restricciones"


def _merge_candidates(candidates: Sequence[Candidate]) -> tuple[Candidate, ...]:
    merged: list[Candidate] = []
    for candidate in candidates:
        existing = next(
            (
                item
                for item in merged
                if isclose(item.point.x, candidate.point.x, rel_tol=EPSILON, abs_tol=EPSILON)
                and isclose(item.point.y, candidate.point.y, rel_tol=EPSILON, abs_tol=EPSILON)
            ),
            None,
        )
        if existing is None:
            merged.append(candidate)
            continue
        merged[merged.index(existing)] = Candidate(
            point=existing.point,
            source=f"{existing.source}; {candidate.source}",
            feasible=existing.feasible and candidate.feasible,
            reason=existing.reason,
            objective_value=existing.objective_value,
        )
    return tuple(sorted(merged, key=lambda value: (value.point.x, value.point.y)))


def solve_graphical(
    objective: Sequence[float], constraints: Sequence[Constraint]
) -> SolveResult:
    """Solve a two-variable maximization problem using feasible vertices."""

    _validate_input(objective, constraints)

    if not any(constraint.a > 0 for constraint in constraints):
        raise ValueError("La variable x no esta acotada por los recursos.")
    if not any(constraint.b > 0 for constraint in constraints):
        raise ValueError("La variable y no esta acotada por los recursos.")

    boundaries: list[tuple[float, float, float, str]] = [
        (1.0, 0.0, 0.0, "x = 0"),
        (0.0, 1.0, 0.0, "y = 0"),
    ]
    boundaries.extend(
        (constraint.a, constraint.b, constraint.rhs, constraint.name)
        for constraint in constraints
        if constraint.a != 0 or constraint.b != 0
    )

    candidates: list[Candidate] = []
    for index, first in enumerate(boundaries):
        for second in boundaries[index + 1 :]:
            point = _intersection(first[:3], second[:3])
            if point is None:
                continue
            feasible = _is_feasible(point, constraints)
            candidates.append(
                Candidate(
                    point=point,
                    source=f"{first[3]} y {second[3]}",
                    feasible=feasible,
                    reason=_feasibility_reason(point, constraints),
                    objective_value=objective[0] * point.x + objective[1] * point.y,
                )
            )

    candidates = list(_merge_candidates(candidates))
    vertices = _deduplicate([candidate.point for candidate in candidates if candidate.feasible])
    if not vertices:
        raise ValueError("El modelo no tiene una region factible.")

    objective_values = [objective[0] * point.x + objective[1] * point.y for point in vertices]
    objective_value = max(objective_values)
    optimal_points = tuple(
        point
        for point, value in zip(vertices, objective_values)
        if abs(value - objective_value) <= EPSILON
    )
    best = optimal_points[0]

    usage = tuple(
        constraint.a * best.x + constraint.b * best.y for constraint in constraints
    )
    slacks = tuple(
        constraint.rhs - used for constraint, used in zip(constraints, usage)
    )

    return SolveResult(
        candidates=tuple(candidates),
        vertices=vertices,
        optimal_points=optimal_points,
        objective_value=objective_value,
        resource_usage=usage,
        slacks=slacks,
    )
