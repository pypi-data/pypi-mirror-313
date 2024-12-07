import gurobipy as gp
import polars as pl

from xplor.gurobi import XplorGurobi, apply_eval, quicksum
from xplor.model import Xplor


def test_gurobi_model(xmodel: XplorGurobi) -> None:
    df = pl.DataFrame(
        {
            "i": [0, 0, 1, 2, 2],
            "j": [1, 2, 0, 0, 1],
            "u": [0.3, 1.2, 0.7, 0.9, 1.2],
            "c": [1.3, 1.7, 1.4, 1.1, 0.9],
            "obj": [2.5, 2.7, 1.2, 1.7, 3.9],
        }
    )

    df = (
        df.pipe(
            xmodel.add_vars,
            name="x",
            ub="u",
            obj="obj",
            indices=["i", "j"],
            vtype=gp.GRB.CONTINUOUS,
        )
        .pipe(apply_eval, "y = 2 * x - c")
        .group_by("i")
        .agg(quicksum("y"), pl.col("c").min())
        .pipe(xmodel.add_constrs, "y <= c", name="constr")
    )


def test_model() -> None:
    m = Xplor(gp.Model())
    df = pl.DataFrame(
        {
            "i": [0, 0, 1, 2, 2],
            "j": [1, 2, 0, 0, 1],
            "u": [0.3, 1.2, 0.7, 0.9, 1.2],
            "c": [1.3, 1.7, 1.4, 1.1, 0.9],
            "obj": [2.5, 2.7, 1.2, 1.7, 3.9],
        }
    )

    df = (
        df.pipe(
            m.add_vars,
            name="x",
            ub="u",
            obj="obj",
            indices=["i", "j"],
            vtype=gp.GRB.CONTINUOUS,
        )
        .pipe(apply_eval, "y = 2 * x - c")
        .group_by("i")
        .agg(quicksum("y"), pl.col("c").min())
        .pipe(m.add_constrs, "y <= c", name="constr")
    )
