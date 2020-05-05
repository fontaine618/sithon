import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sithon.model_output import coef_table_long, coef_table_wide
from sithon.latex import pd_to_tabular

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

dat = sm.datasets.get_rdataset("Guerry", "HistData").data

model1 = smf.ols('Lottery ~ Literacy ', data=dat).fit()
model2 = smf.ols('Lottery ~ Literacy + np.log(Pop1831)', data=dat).fit()
model3 = smf.ols('Lottery ~ Literacy * np.log(Pop1831)', data=dat).fit()

models = {
    "Literacy Only": model1,
    "Literacy + Population": model2,
    "Literacy * Population": model3
}

results = coef_table_wide(models)
print(pd_to_tabular(results))


results = coef_table_long(models)
print(pd_to_tabular(results))

