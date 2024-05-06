#perform regression trying to predict the outcome of each possession based only on the players that were on the court
import pandas as pd
import matplotlib.pyplot as plt
import json
import csv
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def perform_regression(possessions, file_path):
	print("starting regression")
	X = possessions.drop(['GAME_ID', 'TIME', 'OUTCOME'], axis=1)
	Y = possessions['OUTCOME']

	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

	ridgeCV = RidgeCV(alphas=[.1,1,2,3,4,5,6,10,50,100,200,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500,11000,11500,12000,12500], store_cv_values=True)

	ridgeCV.fit(X, Y)
	print("ridge regression score:", ridgeCV.score(X, Y))
	print("ridge regression test score:", ridgeCV.score(X_test, Y_test))
	print("Alpha:", ridgeCV.alpha_)


	file_name = str(file_path).split('/')[-1]
	year = file_name.split('_')[0]
	with open(file_path, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(['Player', 'O_POSSESSIONS', 'O_RAPM_'+str(year), 'D_POSSESSIONS', 'D_RAPM_'+str(year), 'TOTAL_POSSESSIONS', 'RAPM_'+str(year)])
		writer.writerow(['HOME', possessions.shape[0], int((ridgeCV.coef_[0]*100)*100)/100, 0, 0, possessions.shape[0], int((ridgeCV.coef_[0]*100)*100)/100])
		for i in range(1, len(ridgeCV.coef_), 2):
			o_rapm = ridgeCV.coef_[i]*100
			o_rapm = int(o_rapm*100)/100
			d_rapm = ridgeCV.coef_[i+1]*100
			d_rapm = int(d_rapm*100)/100

			rapm = int((o_rapm+d_rapm)*100)/100

			o_possessions = possessions[possessions[X.columns[i]]==1].shape[0]
			d_possessions = possessions[possessions[X.columns[i+1]]==-1].shape[0]
			total_possessions = o_possessions+d_possessions

			writer.writerow([X.columns[i][2:], o_possessions, o_rapm, d_possessions, d_rapm, total_possessions, rapm])
	print("performed regression successfully")


