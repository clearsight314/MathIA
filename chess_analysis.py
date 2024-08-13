import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib as mpl # fancy graphs and charts!
import matplotlib.pyplot as plt # easy reference for pyplot
import os
import data_processing as dprocess
import chess_utilities as util
import chess_visualization as vis

print("executing code...")

#OLD CODE FOR CREATING games_df.csv which contains the Pandas Dataframe with all the data
"""
#get all the filenames from the Lichess Elite folder
all_pgn_filenames = dprocess.get_filenames("/Users/hsprague/Documents/Code/Lichess Elite Database")

#add folder path to filenames
for i in range(len(all_pgn_filenames)):
    all_pgn_filenames[i] = "/Users/hsprague/Documents/Code/Lichess Elite Database/" + all_pgn_filenames[i]

games = dprocess.build_dataframe(all_pgn_filenames) #dataframe of relevant game infos
games.to_csv('games_df.csv') 
print(games.head())
"""

games = pd.read_csv('gen_games.csv')

print(games.head())

#THIS SECTION DEDICATED TO QUESTION 1: CHECKMATE SQUARES
# obtain the list of all checkmate moves
checkmate_moves = dprocess.get_checkmate_moves(games)

# convert move list into square list
checkmate_squares = dprocess.get_square_list(checkmate_moves)
util.print_first(checkmate_squares, 2)

# get frequency matrix for checkmate squares
checkmate_freq_matrix = dprocess.get_frequency_matrix(checkmate_squares) # this will go in data section!!
print("Checkmate Frequency Matrix:")
print(checkmate_freq_matrix)

# convert above matrix into percentages for display in heatmap -- include calculation in IA
checkmate_percentage_matrix = dprocess.percentage_matrix_from_frequencies(checkmate_freq_matrix)

#create heatmap for IA diagram
vis.create_heatmap(checkmate_percentage_matrix, "Checkmate Percentages, general Lichess users")


#THIS SECTION DEDICATED TO QUESTION 2: CASTLING MOVE NUMBER
castle_data = dprocess.get_castle_data(games) #gathers data related to castling & puts it in a dataframe
aggregate_castle_data = dprocess.aggregate_castle_data(castle_data) #sorts castle data by move number

print("Aggregate Castling Data:")
print(aggregate_castle_data) 

#sort castling data into a 3x3 matrix based on result and which player castled first
castling_matrix = dprocess.castling_matrix(castle_data) 
print("Castling Matrix:")
print(castling_matrix)
vis.castling_chart(castling_matrix, "Castling Matrix")


#THIS SECTION DEDICATED TO QUESTION 3: PAWN STRUCTURE
pawn_positions = dprocess.pawn_positions_data(games)  #obtains the position of each pawn prior to first capture per game
print("Pawn Positions Data:")
print(dprocess.aggregate_pawn_positions_data(pawn_positions)) #gets average and standard deviation of that position information

print("done!")
