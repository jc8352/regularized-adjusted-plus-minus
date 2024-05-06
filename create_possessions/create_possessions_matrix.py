#convert play-by-play with players to matrix of possessions that includes the players that were on the court and the result of the possession
import pandas as pd
import csv

GAME_ID_COL = 0

HOME_COLUMN = 7
NEUTRAL_COLUMN = 8
AWAY_COLUMN = 9

PLAYER1 = 34
PLAYER2 = 35
PLAYER3 = 36
PLAYER4 = 37
PLAYER5 = 38

PLAYER6 = 39
PLAYER7 = 40
PLAYER8 = 41
PLAYER9 = 42
PLAYER10 = 43

PCTIMESTRING = 6


def find_poss_end(start_index, team_col, opp_team_col, current_points, pbp): #return final number of points on possession and current index
	if 'MISS' in pbp.iloc[start_index, team_col] and 'Free Throw' not in pbp.iloc[start_index, team_col]:
		start_index += 1
		if 'REBOUND' in pbp.iloc[start_index, opp_team_col] or 'Rebound' in pbp.iloc[start_index, opp_team_col]:
			return (current_points, start_index)
		elif 'REBOUND' in pbp.iloc[start_index, team_col] or 'Rebound' in pbp.iloc[start_index, team_col]:
			if pbp.iloc[start_index, PCTIMESTRING] % 720 == 0:
				return (current_points, start_index)
			elif 'End of' in pbp.iloc[start_index+1, NEUTRAL_COLUMN] and pbp.iloc[start_index+1, PCTIMESTRING] % 720 == 0:
				return (current_points, start_index)
			else:
				return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
		elif 'Tip Layup' in pbp.iloc[start_index, team_col] and 'MISS' not in pbp.iloc[start_index, team_col]:
			return (current_points+2, start_index)
		elif 'Tip Layup' in pbp.iloc[start_index, team_col] and 'MISS' in pbp.iloc[start_index, team_col]:
			start_index += 1
			if 'REBOUND' in pbp.iloc[start_index, team_col] and ('REBOUND' in pbp.iloc[start_index+1, opp_team_col] or 'Rebound' in pbp.iloc[start_index+1, opp_team_col]):
				return (current_points, start_index)
			else:
				return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
		elif 'Tip Dunk' in pbp.iloc[start_index, team_col] and 'MISS' not in pbp.iloc[start_index, team_col]:
			return (current_points+2, start_index)
		else:
			return (current_points, start_index)
	elif 'Turnover' in pbp.iloc[start_index, team_col]:
		return (current_points, start_index)
	elif 'PTS' in pbp.iloc[start_index, team_col] and '3PT' in pbp.iloc[start_index, team_col] and 'Free Throw' not in pbp.iloc[start_index, team_col]: #3 made
		current_points += 3
		if 'FOUL' in pbp.iloc[start_index+1, opp_team_col] and 'T.FOUL ' not in pbp.iloc[start_index+1, opp_team_col]:#3 point and 1
			start_index+=1
			if 'FLAGRANT' in pbp.iloc[start_index, opp_team_col]:
				while 'Free Throw' not in pbp.iloc[start_index, team_col]:
					start_index+=1
				if '1 of 1' in pbp.iloc[start_index, team_col]:
					current_points+=1
					return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
				else:
					while '2 of 2' not in pbp.iloc[start_index, team_col]:
						start_index+=1
					if 'MISS' in pbp.iloc[start_index, team_col]:
						return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
					else:
						current_points+=1
						return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
			else:
				while 'Free Throw 1 of 1' not in pbp.iloc[start_index, team_col]:
					start_index+=1
				if 'MISS' in pbp.iloc[start_index, team_col]:
					start_index+=1
					if 'REBOUND' in pbp.iloc[start_index, opp_team_col] or 'Rebound' in pbp.iloc[start_index, opp_team_col]:
						return (current_points, start_index)
					elif 'REBOUND' in pbp.iloc[start_index, team_col] or 'Rebound' in pbp.iloc[start_index, team_col]:
						return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
					elif 'Lane' in pbp.iloc[start_index, opp_team_col]:
						return (current_points, start_index)
				else:
					return (current_points+1, start_index)
		else:
			return (current_points, start_index)
	elif 'PTS' in pbp.iloc[start_index, team_col] and 'Free Throw' not in pbp.iloc[start_index, team_col]: #2 made
		current_points += 2
		if 'FOUL' in pbp.iloc[start_index+1, opp_team_col] and 'T.FOUL ' not in pbp.iloc[start_index+1, opp_team_col]:#2 point and 1
			start_index+=1
			if 'FLAGRANT' in pbp.iloc[start_index, opp_team_col]:
				while 'Free Throw' not in pbp.iloc[start_index, team_col]:
					start_index+=1
				if '1 of 1' in pbp.iloc[start_index, team_col]:
					current_points+=1
					return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
				else:
					while '2 of 2' not in pbp.iloc[start_index, team_col]:
						start_index+=1
					if 'MISS' in pbp.iloc[start_index, team_col]:
						return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
					else:
						current_points+=1
						return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
			else:
				while 'Free Throw 1 of 1' not in pbp.iloc[start_index, team_col]:
					if 'Rivers L.B.FOUL' in pbp.iloc[start_index, opp_team_col]:
						return (current_points, start_index)
					start_index+=1
				if 'MISS' in pbp.iloc[start_index, team_col]:
					start_index+=1
					if 'REBOUND' in pbp.iloc[start_index, opp_team_col] or 'Rebound' in pbp.iloc[start_index, opp_team_col]:
						return (current_points, start_index)
					elif 'REBOUND' in pbp.iloc[start_index, team_col] or 'Rebound' in pbp.iloc[start_index, team_col]:
						return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
					elif 'Tip Layup' in pbp.iloc[start_index, team_col] and 'MISS' not in pbp.iloc[start_index, team_col]:
						return (current_points+2, start_index)
					elif 'Tip Layup' in pbp.iloc[start_index, team_col] and 'MISS' in pbp.iloc[start_index, team_col]:
						start_index += 1
						if 'REBOUND' in pbp.iloc[start_index, team_col] and ('REBOUND' in pbp.iloc[start_index+1, opp_team_col] or 'Rebound' in pbp.iloc[start_index+1, opp_team_col]):
							return (current_points, start_index)
						else:
							return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
					else:
						return (current_points, start_index)
				else:
					return (current_points+1, start_index)
		else:
			return (current_points, start_index)
	elif 'FLAGRANT' in pbp.iloc[start_index, opp_team_col]:
		start_index+=1
		while ('Timeout' in pbp.iloc[start_index, team_col] or 'Timeout' in pbp.iloc[start_index, opp_team_col]) or ('SUB' in pbp.iloc[start_index, team_col] or 'SUB' in pbp.iloc[start_index, opp_team_col]) or ('Instant Replay' in pbp.iloc[start_index, NEUTRAL_COLUMN]):
			start_index+=1
		if 'Free Throw Flagrant 1 of 2' in pbp.iloc[start_index, team_col]:
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
			start_index+=1
			while 'Free Throw Flagrant 2 of 2' not in pbp.iloc[start_index, team_col]:
				start_index+=1
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
		elif 'Free Throw Flagrant 1 of 3' in pbp.iloc[start_index, team_col]:
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
			start_index+=1
			while 'Free Throw Flagrant 2 of 3' not in pbp.iloc[start_index, team_col] and 'Free Throw 2 of 3' not in pbp.iloc[start_index, team_col]:
				start_index+=1
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
			start_index+=1
			while 'Free Throw Flagrant 3 of 3' not in pbp.iloc[start_index, team_col] and 'Free Throw 3 of 3' not in pbp.iloc[start_index, team_col]:
				start_index+=1
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
		return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
	elif 'FOUL' in pbp.iloc[start_index, opp_team_col]:
		start_index+=1
		while ('Timeout' in pbp.iloc[start_index, team_col] or 'Timeout' in pbp.iloc[start_index, opp_team_col]) or ('SUB' in pbp.iloc[start_index, team_col] or 'SUB' in pbp.iloc[start_index, opp_team_col]) or ('Instant Replay' in pbp.iloc[start_index, NEUTRAL_COLUMN]):
			start_index+=1
		if 'Free Throw 1 of 2' in pbp.iloc[start_index, team_col]:
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
			start_index+=1
			while 'Free Throw 2 of 2' not in pbp.iloc[start_index, team_col]:
				start_index+=1
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
				return (current_points, start_index)
			else:
				start_index+=1
				if 'REBOUND' in pbp.iloc[start_index, opp_team_col] or 'Rebound' in pbp.iloc[start_index, opp_team_col]:
					return (current_points, start_index)
				elif 'REBOUND' in pbp.iloc[start_index, team_col] or 'Rebound' in pbp.iloc[start_index, team_col]:
					return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
				elif ('SUB' in pbp.iloc[start_index, opp_team_col] or 'SUB' in pbp.iloc[start_index, team_col] or 'Timeout' in pbp.iloc[start_index, opp_team_col] or 'Timeout' in pbp.iloc[start_index, team_col]): #and 'REBOUND' in pbp.iloc[start_index+1, opp_team_col]:
					while ('SUB' in pbp.iloc[start_index, opp_team_col] or 'SUB' in pbp.iloc[start_index, team_col]):
						start_index+=1
					if 'REBOUND' in pbp.iloc[start_index, opp_team_col] or 'Rebound' in pbp.iloc[start_index, opp_team_col]:
						return (current_points, start_index)
					else:
						return find_poss_end(start_index, team_col, opp_team_col, current_points, pbp)
				elif 'Lane' in pbp.iloc[start_index, opp_team_col]:
					return (current_points, start_index)
				elif 'T.FOUL' in pbp.iloc[start_index, opp_team_col]:
					return (current_points, start_index)
				elif 'S.FOUL' in pbp.iloc[start_index, opp_team_col]:
					return (current_points, start_index)
				else:
					return (current_points, start_index)
		elif 'Free Throw 1 of 3' in pbp.iloc[start_index, team_col]:
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
			start_index+=1
			while 'Free Throw 2 of 3' not in pbp.iloc[start_index, team_col]:
				start_index+=1
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
			start_index+=1
			while 'Free Throw 3 of 3' not in pbp.iloc[start_index, team_col]:
				start_index+=1
			if 'MISS' not in pbp.iloc[start_index, team_col]:
				current_points+=1
				return (current_points, start_index)
			else:
				start_index+=1
				if 'REBOUND' in pbp.iloc[start_index, opp_team_col] or 'Rebound' in pbp.iloc[start_index, opp_team_col]:
					return (current_points, start_index)
				elif 'REBOUND' in pbp.iloc[start_index, team_col] or 'Rebound' in pbp.iloc[start_index, team_col]:
					return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)
				elif ('SUB' in pbp.iloc[start_index, opp_team_col] or 'SUB' in pbp.iloc[start_index, team_col]): #and 'REBOUND' in pbp.iloc[start_index+1, opp_team_col]:
					while ('SUB' in pbp.iloc[start_index, opp_team_col] or 'SUB' in pbp.iloc[start_index, team_col]):
						start_index+=1
					if 'REBOUND' in pbp.iloc[start_index, opp_team_col] or 'Rebound' in pbp.iloc[start_index, opp_team_col]:
						return (current_points, start_index)
					else:
						return find_poss_end(start_index, team_col, opp_team_col, current_points, pbp)
				else:
					return (current_points, start_index)
		else:
			return find_poss_end(start_index, team_col, opp_team_col, current_points, pbp)

	else:
		return find_poss_end(start_index+1, team_col, opp_team_col, current_points, pbp)



def create_matrix(pbp, file_path):
	print("starting creating possession matrix")
	total_plays = pbp.shape[0]


	possession_matrix = []

	pbp['HOMEDESCRIPTION'] = pbp['HOMEDESCRIPTION'].fillna('0')
	pbp['NEUTRALDESCRIPTION'] = pbp['NEUTRALDESCRIPTION'].fillna('0')
	pbp['VISITORDESCRIPTION'] = pbp['VISITORDESCRIPTION'].fillna('0')


	i = 0
	misses = 0
	turnovers = 0
	threes = 0
	twos = 0
	no_poss_change = 0

	while i < total_plays:
		if 'MISS' in pbp.iloc[i, HOME_COLUMN] and 'Free Throw' not in pbp.iloc[i, HOME_COLUMN]:#missed shots
			misses += 1
			time = pbp.iloc[i, PCTIMESTRING]
			i += 1
			if 'REBOUND' in pbp.iloc[i, AWAY_COLUMN] or 'Rebound' in pbp.iloc[i, AWAY_COLUMN]:#defensive rebound
				outcome = 0
				possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, time, outcome])
			elif 'Rebound' in pbp.iloc[i, HOME_COLUMN]:#end of quarter missed shot
				outcome = 0
				if pbp.iloc[i, PCTIMESTRING] % 720 == 0:
					possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, time, outcome])
				elif 'End of' in pbp.iloc[i+1, NEUTRAL_COLUMN] and pbp.iloc[i+1, PCTIMESTRING] % 720 == 0:
					possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, time, outcome])
			elif 'Tip Layup' in pbp.iloc[i, HOME_COLUMN] and 'MISS' not in pbp.iloc[i, HOME_COLUMN]:
				outcome = 2
				possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, time, outcome])
			elif 'Tip Layup' in pbp.iloc[i, HOME_COLUMN] and 'MISS' in pbp.iloc[i, HOME_COLUMN]:
				i += 1
				if 'REBOUND' in pbp.iloc[i, HOME_COLUMN] and ('REBOUND' in pbp.iloc[i+1, AWAY_COLUMN] or 'Rebound' in pbp.iloc[i+1, AWAY_COLUMN]):
					outcome = 0
					possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, time, outcome])
			else:
				no_poss_change += 1
		elif 'Turnover' in pbp.iloc[i, HOME_COLUMN]:#turnover
			outcome = 0
			turnovers += 1
			possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, pbp.iloc[i, PCTIMESTRING], outcome])
		elif 'PTS' in pbp.iloc[i, HOME_COLUMN] and '3PT' in pbp.iloc[i, HOME_COLUMN] and 'Free Throw' not in pbp.iloc[i, HOME_COLUMN]:#made 3
			outcome, j = find_poss_end(i, HOME_COLUMN, AWAY_COLUMN, 0, pbp)
			possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, pbp.iloc[i, PCTIMESTRING], outcome])
			i = j
		elif 'PTS' in pbp.iloc[i, HOME_COLUMN] and 'Free Throw' not in pbp.iloc[i, HOME_COLUMN]:#made 2
			outcome, j = find_poss_end(i, HOME_COLUMN, AWAY_COLUMN, 0, pbp)
			possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, pbp.iloc[i, PCTIMESTRING], outcome])
			i = j
		elif 'FOUL' in pbp.iloc[i, AWAY_COLUMN] and 'T.FOUL ' not in pbp.iloc[i, AWAY_COLUMN]:
			temp_ind = i
			temp_ind+=1
			while ('Timeout' in pbp.iloc[temp_ind, HOME_COLUMN] or 'Timeout' in pbp.iloc[temp_ind, AWAY_COLUMN]) or ('SUB' in pbp.iloc[temp_ind, HOME_COLUMN] or 'SUB' in pbp.iloc[temp_ind, AWAY_COLUMN]) or ('Instant Replay' in pbp.iloc[temp_ind, NEUTRAL_COLUMN]):
				temp_ind+=1
			if 'Free Throw' in pbp.iloc[temp_ind, HOME_COLUMN]:
				outcome, j = find_poss_end(i, HOME_COLUMN, AWAY_COLUMN, 0, pbp)
				possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], 1, pbp.iloc[i, PCTIMESTRING], outcome])
				i = j




		elif 'MISS' in pbp.iloc[i, AWAY_COLUMN] and 'Free Throw' not in pbp.iloc[i, AWAY_COLUMN]:#missed shots
			misses += 1
			time = pbp.iloc[i, PCTIMESTRING]
			i += 1
			if 'REBOUND' in pbp.iloc[i, HOME_COLUMN] or 'Rebound' in pbp.iloc[i, HOME_COLUMN]:#defensive rebound
				outcome = 0
				possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, time, outcome])
			elif 'Rebound' in pbp.iloc[i, AWAY_COLUMN]:#end of quarter missed shot
				outcome = 0
				if pbp.iloc[i, PCTIMESTRING] % 720 == 0:
					possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, time, outcome])
				elif 'End of' in pbp.iloc[i+1, NEUTRAL_COLUMN] and pbp.iloc[i+1, PCTIMESTRING] % 720 == 0:
					possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, time, outcome])
			elif 'Tip Layup' in pbp.iloc[i, AWAY_COLUMN] and 'MISS' not in pbp.iloc[i, AWAY_COLUMN]:
				outcome = 2
				possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, time, outcome])
			elif 'Tip Layup' in pbp.iloc[i, AWAY_COLUMN] and 'MISS' in pbp.iloc[i, AWAY_COLUMN]:
				i += 1
				if 'REBOUND' in pbp.iloc[i, AWAY_COLUMN] and ('REBOUND' in pbp.iloc[i+1, HOME_COLUMN] or 'Rebound' in pbp.iloc[i+1, HOME_COLUMN]):
					outcome = 0
					possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, time, outcome])
			else:
				no_poss_change += 1
		elif 'Turnover' in pbp.iloc[i, AWAY_COLUMN]:#turnover
			outcome = 0
			turnovers += 1
			possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, pbp.iloc[i, PCTIMESTRING], outcome])
		elif 'PTS' in pbp.iloc[i, AWAY_COLUMN] and '3PT' in pbp.iloc[i, AWAY_COLUMN] and 'Free Throw' not in pbp.iloc[i, AWAY_COLUMN]:#made 3
			outcome, j = find_poss_end(i, AWAY_COLUMN, HOME_COLUMN, 0, pbp)
			possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, pbp.iloc[i, PCTIMESTRING], outcome])
			i = j
		elif 'PTS' in pbp.iloc[i, AWAY_COLUMN] and 'Free Throw' not in pbp.iloc[i, AWAY_COLUMN]:#made 2
			outcome, j = find_poss_end(i, AWAY_COLUMN, HOME_COLUMN, 0, pbp)
			possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, pbp.iloc[i, PCTIMESTRING], outcome])
			i = j
		elif 'FOUL' in pbp.iloc[i, HOME_COLUMN] and 'T.FOUL ' not in pbp.iloc[i, HOME_COLUMN]:
			temp_ind = i
			temp_ind+=1
			while ('Timeout' in pbp.iloc[temp_ind, HOME_COLUMN] or 'Timeout' in pbp.iloc[temp_ind, AWAY_COLUMN]) or ('SUB' in pbp.iloc[temp_ind, HOME_COLUMN] or 'SUB' in pbp.iloc[temp_ind, AWAY_COLUMN]) or ('Instant Replay' in pbp.iloc[temp_ind, NEUTRAL_COLUMN]):
				temp_ind+=1
			if 'Free Throw' in pbp.iloc[temp_ind, AWAY_COLUMN]:
				outcome, j = find_poss_end(i, AWAY_COLUMN, HOME_COLUMN, 0, pbp)
				possession_matrix.append([pbp.iloc[i, GAME_ID_COL], pbp.iloc[i, PLAYER1], pbp.iloc[i, PLAYER2], pbp.iloc[i, PLAYER3], pbp.iloc[i, PLAYER4], pbp.iloc[i, PLAYER5], pbp.iloc[i, PLAYER6], pbp.iloc[i, PLAYER7], pbp.iloc[i, PLAYER8], pbp.iloc[i, PLAYER9], pbp.iloc[i, PLAYER10], 0, pbp.iloc[i, PCTIMESTRING], outcome])
				i = j
		i += 1


	print("total number of possessions:", len(possession_matrix))

	col_names = ['GAME_ID', 'O_P1', 'O_P2', 'O_P3', 'O_P4', 'O_P5', 'D_P1', 'D_P2', 'D_P3', 'D_P4', 'D_P5', 'O_HOME', 'TIME', 'OUTCOME']
	with open(file_path, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(col_names)
		for possession in possession_matrix:
			writer.writerow(possession)
	print("created possessions matrix successfully")
	possessions = pd.DataFrame(possession_matrix, columns=col_names)
	return possessions

from pathlib import Path

cwd = Path.cwd()

root = cwd.parent.absolute()

pbp_2022_23 = pd.read_csv(root / 'created_possession_data' / 'pbp_with_players' / 'pbp_2022_reg.csv', index_col=0)
create_matrix(pbp_2022_23, 'compare.csv')

