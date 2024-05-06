from create_possessions import add_players_on_court
from create_possessions import create_possessions_matrix
from create_possessions import OHE_matrix
from regression import rapm_regression

import pandas as pd
from pathlib import Path


cwd = Path.cwd()


YEAR = 2021 #can change year 2021 is 2021-22 season, 2022 is 2022-23 season
pbp_file_name = 'nbastats_'+str(YEAR)+'.csv'
play_by_play = pd.read_csv(cwd / 'pbp_data' / pbp_file_name) #play-by-play to dataframe

#add players that were on the court for each play
pbp_w_players_file_path = cwd / 'created_possession_data' / 'pbp_with_players' / ('pbp_'+str(YEAR)+'_reg.csv')
pbp_w_players = add_players_on_court.add_players(play_by_play, pbp_w_players_file_path)

#convert play-by-play with players to matrix of possessions that includes the players that were on the court and the result of the possession
possessions_matrix_file_path = cwd / 'created_possession_data' / 'possessions' / (str(YEAR)+'_reg_possessions.csv')
possessions_matrix = create_possessions_matrix.create_matrix(pbp_w_players, possessions_matrix_file_path)

#convert matrix of possessions with players to a one hot encoded matrix of possessions
OHE_matrix_file_path = cwd / 'created_possession_data' / 'possessions_OHE' / (str(YEAR)+'_reg_possessions_encoded.csv')
OHE_matrix = OHE_matrix.encode_matrix(possessions_matrix, OHE_matrix_file_path)

#perform the regression
rapm_file_path = cwd / 'regression_results' / (str(YEAR)+'_rapm.csv')
rapm_regression.perform_regression(OHE_matrix, rapm_file_path)




