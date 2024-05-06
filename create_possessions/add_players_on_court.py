#take nba play-by-play data and add the players that were on the court during each play
from . import nba_on_court
import pandas as pd


def add_players(pbp_df, file_path):
	print("starting add players on court")
	new_pbp = pd.DataFrame()
	for game_id in pbp_df['GAME_ID'].unique():
		plays = pbp_df[pbp_df['GAME_ID'] == game_id].reset_index(drop=True)
		pbp_with_players = nba_on_court.players_on_court(plays)
		new_pbp = new_pbp.append(pbp_with_players)

	cols = ["PLAYER1", "PLAYER2", "PLAYER3", "PLAYER4", "PLAYER5", "PLAYER6", "PLAYER7", "PLAYER8", "PLAYER9", "PLAYER10"]
	new_pbp.loc[:, cols] = new_pbp.loc[:, cols].apply(nba_on_court.players_name, result_type="expand")
	new_pbp.to_csv(file_path)
	print("added players on court successfully")
	return new_pbp

