import pandas as pd
import numpy as np


def coef_table_long(models):
    table = _coef_table(models)
    table.reset_index(inplace=True)
    table.set_index("Term", inplace=True)
    return table.drop(columns="Model").groupby(table["Model"])


def coef_table_wide(models, columns=["ci"]):
    table = _coef_table(models)
    cols = list()
    for col in columns:
        if col == "coef":
            cols.append("Estimate")
        elif col == "se":
            cols.append("Std. Err.")
        elif col == "t":
            cols.append("t-value")
        elif col == "p":
            cols.append("p-value")
        elif col == "ci":
            cols.extend(["95% C.I. (lower)", "95% C.I. (upper)"])
    table = table[cols].unstack(level="Model")
    table.sort_index(axis=1, level=1, inplace=True)
    table = table.reorder_levels([1, 0], axis=1)
    table._set_axis_name((None, None), axis=1, inplace=True)
    return table


def _coef_table(models):
    results = dict()
    for name, model in models.items():
        conf_int = model.conf_int()
        results[name] = pd.DataFrame({
            "Estimate": model.params,
            "Std. Err.": model.bse,
            "t-value": model.tvalues,
            "p-value": model.pvalues,
            "95% C.I. (lower)": conf_int[0],
            "95% C.I. (upper)": conf_int[1]
        })
    table = pd.concat(results)
    table._set_axis_name(("Model", "Term"), axis=0, inplace=True)
    return table