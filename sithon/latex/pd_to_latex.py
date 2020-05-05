import pandas as pd
import numpy as np


def pd_to_tabular(df, group_names=None, title=None, group_name_align="c", **kwargs):
    dfs = dict()
    df_names = dict()
    if isinstance(df, pd.core.groupby.DataFrameGroupBy):
        grouped = True
        for name, sub_df in df:
            dfs[name] = sub_df
            df_names[name] = name if group_names is None else group_names[name]
    elif isinstance(df, pd.DataFrame):
        grouped = False
        dfs[0] = df
        df_names[0] = None
    # get column format and header
    n, d = next(iter(dfs.items()))
    kwargs["multicolumn_format"] = "c"
    tmp_table = d.to_latex(**kwargs)
    header = _extract_header(tmp_table)
    header, n_col = _format_header(header)
    col_format = _get_column_format(tmp_table)
    # build table
    table = "\\begin{{tabular}}{{{}}}\n".format(col_format)
    table += "\\toprule\n"
    if title is not None:
        table += "\\multicolumn{{{}}}{{{}}}{{\\normalsize\\textbf{{{}}}}}".format(n_col, "l", title)
        table += "\\\\\\addlinespace\n"
    table += header
    for n, d in dfs.items():
        table += "\\midrule\n"
        if df_names[n] is not None:
            table += "\\multicolumn{{{}}}{{{}}}{{\\textbf{{{}}}}}".format(n_col, group_name_align, df_names[n])
            table += "\\\\\\addlinespace\n"
        table += _add_line_space_multi_index(_extract_rows(d.to_latex(**kwargs)), d)
    table += "\\bottomrule\n\\end{tabular}"
    return table


def _extract_rows(table):
    start = table.find("midrule")
    end = table.find("bottomrule")
    result = table[(start+8):(end-1)]
    return result


def _add_line_space_multi_index(table, d):
    id0 = d.index.get_level_values(0)
    id_end = np.where(id0[1:].values == id0[:-1].values)[0] + 1
    rows = table.split("\n")[:-1]
    for i in id_end:
        if i == len(rows) - 1:  # dont add if last row
            break
        rows[i] = rows[i] + "\\addlinespace"
    table = "\n".join(rows)
    return table + "\n"


def _extract_header(table):
    start = table.find("toprule") + 8
    end = table.find("midrule") - 1
    result = table[start:end]
    return result


def _format_header(header):
    n_row = header.count("\n")
    rows = header.split("\n")[:-1]
    n_col = rows[-1].count("&") + 1
    if n_row == 1:  # nothing to do
        return header, n_col
    # check if empty last line when index name
    cells = [row[:-2].split("&") for row in rows]
    if cells[-1][-1].strip() == "":
        ids = [cell for cell in cells[-1] if cell.strip() != ""]
        cols = [cell for cell in cells[-2][len(ids):]]
        last_row = ids + cols
        last_row = " & ".join(last_row) + "\\\\"
        rows = rows[:-2] + [last_row]
        n_row -= 1
    # now we have n + 1 rows; for the n top rows, we add lines
    for i, row in enumerate(rows[:-1]):
        lines = list()
        cells = row[:-2].split("&")
        start = 1
        end = 1
        for cell in cells:
            cell = cell.strip()
            if cell != "":
                # non-empty cell
                # check if multicolumn
                if "multicolumn" in cell:
                    m = int(cell[13])
                    end += m-1
                lines.append((start, end))
            # next cell
            start = end + 1
            end = start
        for line in lines:
            start, end = line
            lr = ""
            if start > 0:
                lr = "l"
            if end < n_col:
                lr += "r"
            row += "\n\\cmidrule({}){{{}}}".format(lr, "{}-{}".format(start, end))
        rows[i] = row
    header = "\n".join(rows) + "\n"
    return header, n_col


def _get_column_format(table):
    start = table.find("tabular") + 9
    end = table[start:].find("}") + start
    return table[start:end]


def wrap_tabular(table, caption=None, label=None, pos="t!"):
    table = "\\begin{{table}}[{}]\n\\centering\n\\small\n".format(pos) + table
    if caption is not None:
        table += "\n\\caption{{{}}}\n".format(caption)
        if label is not None:
            table += "\\label{{{}}}\n".format(label)
    table += "\\end{table}"
    return table