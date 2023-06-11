# %%
import pandas as pd
import numpy as np


class OtreeDataFrame(pd.DataFrame):
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("OtreeDataFrame 类只接受一个 pandas.DataFrame 对象作为参数")

        super().__init__(data.copy())

    def select_app(self, app_name):
        cols = self.columns[self.columns.str.startswith(app_name + '.')]
        return self[cols].copy()

    def select_round(self, round_number):
        cols = [col for col in self.columns if col.split('.')[1] == str(round_number)]
        return self[cols].copy()


# %%

df = pd.read_excel('data/6-6日实验数据94人.xlsx')
df = df.dropna(how='all', axis=1)
df

# %%
odf = OtreeDataFrame(df)

odf.select_app('ug')[['ug.1.player.id_in_group']]
