"""Dulce Trigo Optimizer: graphical linear programming demonstration."""

from math import atan2

import matplotlib.pyplot as plt
import streamlit as st

from lp_solver import Constraint, Point, SolveResult, solve_graphical


PRODUCT_A = "Galletas"
PRODUCT_B = "Cupcakes"

DEFAULT_CONSTRAINTS = (
    Constraint("Harina", 2.0, 3.0, 120.0),
    Constraint("Mano de obra", 3.0, 2.0, 120.0),
    Constraint("Capacidad", 1.0, 1.0, 45.0),
)


def _format_number(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return f"{int(round(value)):,}"
    return f"{value:,.2f}"


def _format_equation(constraint: Constraint) -> str:
    return (
        f"{constraint.a:g}x + {constraint.b:g}y <= {constraint.rhs:g}"
    )


def _ordered_vertices(vertices: tuple[Point, ...]) -> list[Point]:
    center_x = sum(point.x for point in vertices) / len(vertices)
    center_y = sum(point.y for point in vertices) / len(vertices)
    return sorted(
        vertices,
        key=lambda point: atan2(point.y - center_y, point.x - center_x),
    )


def _plot_model(
    constraints: tuple[Constraint, ...], result: SolveResult
) -> plt.Figure:
    vertex_points = list(result.vertices)
    x_intercepts = [
        constraint.rhs / constraint.a
        for constraint in constraints
        if constraint.a > 0
    ]
    y_intercepts = [
        constraint.rhs / constraint.b
        for constraint in constraints
        if constraint.b > 0
    ]
    max_x = max([point.x for point in vertex_points] + x_intercepts + [1.0]) * 1.2
    max_y = max([point.y for point in vertex_points] + y_intercepts + [1.0]) * 1.2

    x_values = [max_x * index / 200 for index in range(201)]
    figure, axis = plt.subplots(figsize=(9, 6))

    for constraint in constraints:
        if constraint.b > 0:
            y_values = [
                (constraint.rhs - constraint.a * x_value) / constraint.b
                for x_value in x_values
            ]
            axis.plot(x_values, y_values, label=f"{constraint.name}: { _format_equation(constraint) }")
        elif constraint.a > 0:
            axis.axvline(
                constraint.rhs / constraint.a,
                label=f"{constraint.name}: { _format_equation(constraint) }",
            )

    polygon = _ordered_vertices(result.vertices)
    axis.fill(
        [point.x for point in polygon],
        [point.y for point in polygon],
        color="#2f7f75",
        alpha=0.2,
        label="Region factible",
    )
    axis.scatter(
        [point.x for point in result.vertices],
        [point.y for point in result.vertices],
        color="#1f2937",
        zorder=4,
        label="Puntos extremos",
    )
    axis.scatter(
        [point.x for point in result.optimal_points],
        [point.y for point in result.optimal_points],
        color="#e07a5f",
        marker="*",
        s=220,
        zorder=5,
        label="Solucion optima",
    )

    axis.set_xlim(0, max_x)
    axis.set_ylim(0, max_y)
    axis.set_xlabel(f"Lotes de {PRODUCT_A.lower()} (x)")
    axis.set_ylabel(f"Lotes de {PRODUCT_B.lower()} (y)")
    axis.set_title("Region factible y solucion optima")
    axis.grid(alpha=0.25)
    axis.legend(fontsize=8, loc="upper right")
    figure.tight_layout()
    return figure


def _show_results(
    constraints: tuple[Constraint, ...], objective_a: float, objective_b: float, result: SolveResult
) -> None:
    best = result.optimal_points[0]
    st.success(
        f"La solucion optima es producir {_format_number(best.x)} lotes de {PRODUCT_A.lower()} "
        f"y {_format_number(best.y)} lotes de {PRODUCT_B.lower()}.",
    )

    first, second, third = st.columns(3)
    first.metric(f"Lotes de {PRODUCT_A}", _format_number(best.x))
    second.metric(f"Lotes de {PRODUCT_B}", _format_number(best.y))
    third.metric("Margen maximo", f"Q{_format_number(result.objective_value)}")

    st.subheader("Evaluacion de puntos extremos")
    vertex_rows = [
        {
            "Punto": f"({_format_number(point.x)}, {_format_number(point.y)})",
            "Margen": f"Q{_format_number(objective_a * point.x + objective_b * point.y)}",
            "Optimo": "Si" if point in result.optimal_points else "No",
        }
        for point in result.vertices
    ]
    st.table(vertex_rows)

    st.subheader("Intersecciones evaluadas")
    candidate_rows = [
        {
            "Interseccion": candidate.source,
            "Punto": f"({_format_number(candidate.point.x)}, {_format_number(candidate.point.y)})",
            "Factible": "Si" if candidate.feasible else "No",
            "Motivo": candidate.reason,
            "Margen": f"Q{_format_number(candidate.objective_value)}",
        }
        for candidate in result.candidates
    ]
    st.table(candidate_rows)

    st.subheader("Uso de recursos en la solucion")
    resource_rows = [
        {
            "Recurso": constraint.name,
            "Utilizado": _format_number(used),
            "Disponible": _format_number(constraint.rhs),
            "Holgura": _format_number(slack),
        }
        for constraint, used, slack in zip(constraints, result.resource_usage, result.slacks)
    ]
    st.table(resource_rows)

    figure = _plot_model(constraints, result)
    st.pyplot(figure)
    plt.close(figure)

    if len(result.optimal_points) > 1:
        st.info("El modelo tiene mas de un punto optimo con el mismo margen.")


st.set_page_config(
    page_title="Sistema de Optimización de Producción",
    layout="wide",
)

st.title("Sistema de Optimización de Producción")

st.markdown(
    "Caso de estudio: Dulce Trigo. Esta herramienta determina la combinacion "
    "de dos productos que maximiza el margen de contribucion respetando hasta "
    "tres recursos limitados."
)

with st.form("model_form"):
    st.subheader("Datos de los productos")
    product_column_a, product_column_b = st.columns(2)
    with product_column_a:
        objective_a = st.number_input(
            f"Margen por lote de {PRODUCT_A} (Q)",
            min_value=0.0,
            value=40.0,
            step=1.0,
        )
    with product_column_b:
        objective_b = st.number_input(
            f"Margen por lote de {PRODUCT_B} (Q)",
            min_value=0.0,
            value=50.0,
            step=1.0,
        )

    st.subheader("Recursos disponibles")
    constraints_input: list[Constraint] = []
    for index, default in enumerate(DEFAULT_CONSTRAINTS):
        name_column, a_column, b_column, rhs_column = st.columns([2.2, 1.4, 1.4, 1.4])
        with name_column:
            name = st.text_input(
                f"Recurso {index + 1}",
                value=default.name,
                key=f"constraint_name_{index}",
            )
        with a_column:
            coefficient_a = st.number_input(
                f"Uso en {PRODUCT_A}",
                min_value=0.0,
                value=default.a,
                step=1.0,
                key=f"constraint_a_{index}",
            )
        with b_column:
            coefficient_b = st.number_input(
                f"Uso en {PRODUCT_B}",
                min_value=0.0,
                value=default.b,
                step=1.0,
                key=f"constraint_b_{index}",
            )
        with rhs_column:
            rhs = st.number_input(
                "Disponibilidad",
                min_value=0.0,
                value=default.rhs,
                step=1.0,
                key=f"constraint_rhs_{index}",
            )
        constraints_input.append(Constraint(name or f"Recurso {index + 1}", coefficient_a, coefficient_b, rhs))

    submitted = st.form_submit_button("Resolver modelo", type="primary", use_container_width=True)

if submitted:
    try:
        constraints = tuple(constraints_input)
        result = solve_graphical((objective_a, objective_b), constraints)

        st.subheader("Modelo matematico")
        st.latex(rf"\max Z = {objective_a:g}x + {objective_b:g}y")
        for constraint in constraints:
            st.latex(
                rf"{constraint.a:g}x + {constraint.b:g}y \leq {constraint.rhs:g}"
            )
        st.latex(r"x \geq 0,\quad y \geq 0")
        _show_results(constraints, objective_a, objective_b, result)
    except ValueError as error:
        st.error(str(error))
else:
    st.info("Los valores iniciales corresponden al caso Dulce Trigo. Presiona 'Resolver modelo' para ver los resultados.")

st.divider()
st.caption("Proyecto de Investigacion de Operaciones | Programacion lineal y metodo grafico")
