import unittest

from lp_solver import Constraint, solve_graphical


class GraphicalSolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.constraints = (
            Constraint("Harina", 2, 3, 120),
            Constraint("Mano de obra", 3, 2, 120),
            Constraint("Capacidad", 1, 1, 45),
        )

    def test_dulce_trigo_optimum(self) -> None:
        result = solve_graphical((40, 50), self.constraints)

        self.assertAlmostEqual(result.objective_value, 2100)
        self.assertEqual(len(result.optimal_points), 1)
        self.assertAlmostEqual(result.optimal_points[0].x, 15)
        self.assertAlmostEqual(result.optimal_points[0].y, 30)
        self.assertEqual(tuple(round(value) for value in result.slacks), (0, 15, 0))

    def test_vertices_are_feasible(self) -> None:
        result = solve_graphical((40, 50), self.constraints)

        expected = {(0, 0), (0, 40), (15, 30), (30, 15), (40, 0)}
        actual = {(round(point.x), round(point.y)) for point in result.vertices}
        self.assertEqual(actual, expected)

    def test_rejects_more_than_two_variables(self) -> None:
        with self.assertRaises(ValueError):
            solve_graphical((40, 50, 60), self.constraints)

    def test_rejects_unbounded_variable(self) -> None:
        constraints = (Constraint("Mano de obra", 0, 2, 120),)

        with self.assertRaisesRegex(ValueError, "x no esta acotada"):
            solve_graphical((40, 50), constraints)

    def test_handles_small_coefficients_without_dropping_constraints(self) -> None:
        constraints = (
            Constraint("Recurso X", 1e-10, 0, 1),
            Constraint("Recurso Y", 0, 1e-10, 1),
        )

        result = solve_graphical((1, 1), constraints)

        self.assertAlmostEqual(result.optimal_points[0].x, 10_000_000_000)
        self.assertAlmostEqual(result.optimal_points[0].y, 10_000_000_000)
        self.assertAlmostEqual(result.objective_value, 20_000_000_000)

    def test_keeps_infeasible_intersections_for_explanation(self) -> None:
        result = solve_graphical((40, 50), self.constraints)

        self.assertTrue(any(not candidate.feasible for candidate in result.candidates))


if __name__ == "__main__":
    unittest.main()
