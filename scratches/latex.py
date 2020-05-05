import pandas as pd
import numpy as np
from sithon.latex.pd_to_latex import pd_to_tabular, wrap_tabular

df = pd.DataFrame(np.random.uniform(0, 1, (5, 5)))

df["id"] = ["A", "A", "B", "B", "B"]


# simple df
df.index.name = "asdas"
table = pd_to_tabular(df, columns=range(4), column_format="lcccc",
                      title="My awesome table")
table = wrap_tabular(table, caption="asdasd", label="asdasd", pos="h")
print(table)

# groups
df_grouped = df.groupby("id")
table = pd_to_tabular(df_grouped, columns=range(4), column_format="lcccc",
                      title="My awesome table")
table = wrap_tabular(table, caption="asdasd", label="asdasd", pos="h")
print(table)


# simple df, multi index
df.index = pd.MultiIndex.from_tuples([(0, 1), (0, 2), (1, 1), (1, 3), (2, 1)], names=["id1", "id2"])
table = pd_to_tabular(df, columns=range(4), column_format="lccccc",
                      title="My awesome table")
table = wrap_tabular(table, caption="asdasd", label="asdasd", pos="h")
print(table)

# groups, multi index
df.index = pd.MultiIndex.from_tuples([(0, 1), (0, 2), (1, 1), (1, 3), (2, 1)], names=["id1", "id2"])
df_grouped = df.groupby("id")
table = pd_to_tabular(df_grouped, columns=range(4), column_format="lccccc",
                      title="My awesome table")
table = wrap_tabular(table, caption="asdasd", label="asdasd", pos="h")
print(table)

# multi index, multi columns
df.index = pd.MultiIndex.from_tuples([(0, 1), (0, 2), (1, 1), (1, 3), (2, 1)], names=["id1", "id2"])
df.columns = pd.MultiIndex.from_tuples([(0, 1), (0, 2), (1, 1), (1, 3), (1, 5), (2, 1)])
table = pd_to_tabular(df, column_format="llcccccc",
                      title="My awesome table")
table = wrap_tabular(table, caption="asdasd", label="asdasd", pos="h")
print(table)

# groups, multi index, multi columns
df.index = pd.MultiIndex.from_tuples([(0, 1), (0, 2), (1, 1), (1, 3), (2, 1)], names=["id1", "id2"])
df.columns = pd.MultiIndex.from_tuples([(0, 1), (0, 2), (1, 1), (1, 3), (1, 5), (2, 1)])
df_grouped = df.groupby((2, 1))
table = pd_to_tabular(df_grouped, column_format="llcccccc",
                      title="My awesome table")
table = wrap_tabular(table, caption="asdasd", label="asdasd", pos="h")
print(table)


