#convert matrix of possessions with players to a one hot encoded matrix of possessions
import pandas as pd
import numpy as np
import csv


def encode_matrix(possessions, file_path):
	print("starting one hot encoding")
	players = set(np.concatenate((possessions['O_P1'], possessions['O_P2'], possessions['O_P3'], possessions['O_P4'], possessions['O_P5'],
								possessions['D_P1'], possessions['D_P2'], possessions['D_P3'], possessions['D_P4'], possessions['D_P5']), axis=None))


	possessions_one_hot_encoded = possessions[['GAME_ID', 'O_HOME', 'TIME', 'OUTCOME']]
	for player in players:
		offense_rows = np.array([False]*possessions.shape[0])
		defense_rows = np.array([False]*possessions.shape[0])
		o_cols = ['O_P1', 'O_P2', 'O_P3', 'O_P4', 'O_P5']
		d_cols = ['D_P1', 'D_P2', 'D_P3', 'D_P4', 'D_P5']
		for o_col in o_cols:
			offense_rows += possessions[o_col] == player
		for d_col in d_cols:
			defense_rows += possessions[d_col] == player
		possessions_one_hot_encoded['O_'+player] = offense_rows*1
		possessions_one_hot_encoded['D_'+player] = defense_rows*-1

	encoded_possessions_file = file_path
	possessions_one_hot_encoded.to_csv(encoded_possessions_file)
	print("created one hot encoded matrix successfully")
	return possessions_one_hot_encoded