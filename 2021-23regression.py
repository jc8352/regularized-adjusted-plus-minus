#performing the regression on 2021-22 and 2022-23 seasons
from regression import rapm_regression

import pandas as pd
from pathlib import Path

cwd = Path.cwd()

print("reading 2021-22 one hot encoded possessions csv to dataframe")
possessions_21_22 = pd.read_csv(cwd / 'created_possession_data' / 'possessions_OHE' / '2021_reg_possessions_encoded.csv', index_col=0)
print("completed reading 2021-22 one hot encoded possessions csv to dataframe")

print("reading 2022-23 one hot encoded possessions csv to dataframe")
possessions_22_23 = pd.read_csv(cwd / 'created_possession_data' / 'possessions_OHE' / '2022_reg_possessions_encoded.csv', index_col=0)
print("completed reading 2022-23 one hot encoded possessions csv to dataframe")

possessions_21_23 = pd.concat([possessions_21_22, possessions_22_23])
possessions_21_23.reset_index(drop=True, inplace=True)
possessions_21_23.fillna(0, inplace=True)

rapm_file_path = cwd / 'regression_results' / '2021-23_rapm.csv'
rapm_regression.perform_regression(possessions_21_23, rapm_file_path)
