# import OS module
import os
import pandas as pd
import numpy as np
import chess
import chess.pgn
import math
import re

def get_filenames (path): # lists filenames in a directory
    dir_list = os.listdir(path)
    return dir_list

def extract_column(column_name, pgn_filename): # obtains just one column of a pgn file
    f = open(pgn_filename, "r")
    column = []
    for line in f:
        if column_name in line:
            data = line[line.index('"')+1:] #isolate data between quotation marks
            data = data[:data.index('"')]
            column.append(data)
    return column

def extract_moves(pgn_filename): # gets just the moves from a pgn
    f = open(pgn_filename, "r")
    column = []
    start_reading = False
    current_moveset = ""
    for line in f:
        if line == "\n":
            if start_reading == False:
                start_reading = True
            elif start_reading == True:
                start_reading = False
                column.append(current_moveset)
                current_moveset = ""
        elif start_reading == True:
            current_moveset += line.strip()
    return column
            
def build_dataframe(filename_list): # builds one single dataframe from a list of files full of data
    results = []
    white_elos = []
    black_elos = []
    moves = []
    for file_name in filename_list:
        results += extract_column('Result', file_name)
        white_elos += extract_column('WhiteElo', file_name)
        black_elos += extract_column('BlackElo', file_name)
        moves += extract_moves(file_name)
    df_setup = {'Result': results, 'WhiteElo': white_elos, 'BlackElo': black_elos, 'Moves': moves}
    return pd.DataFrame(data=df_setup)

def get_checkmate_moves(games_dataframe): # lists all the moves that include a checkmate
    checkmate_moves = []
    for moves in games_dataframe['Moves']:
        move_list = moves.split(' ')
        for i in range(len(move_list)):
            if move_list[i][-1] == "#":
                checkmate_moves.append(move_list[i])     
                
    return checkmate_moves

def get_square_list(move_list): #converts a list of moves into a list of squares by stripping off the piece name
    square_list = []
    for m in move_list:
        square_list.append(m[-3]+m[-2])
    return square_list

def get_frequency_matrix(square_list): # takes a list of squares and counts how many times each comes up
    square_frequencies = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
    y_labels = ["8", "7", "6", "5", "4", "3", "2", "1"]
    x_labels = ["a", "b", "c", "d", "e", "f", "g", "h"]

    for square in square_list:
        coords = [0,0]
        for i in range(8):
            if square[0] == x_labels[i]:
                coords[0] = i

            if square[1] == y_labels[i]:
                coords[1] = i

        square_frequencies[coords[1]][coords[0]] += 1

    return square_frequencies

def percentage_matrix_from_frequencies(frequency_matrix): # calculates percentages from raw frequencies
    total = 0
    for r in range(len(frequency_matrix)):
        for c in range(len(frequency_matrix)):
            total+=frequency_matrix[r][c]
    for i in range(len(frequency_matrix)):
        for j in range(len(frequency_matrix[i])):
            # calculate percent, rounded to 2 decimal places
            frequency_matrix[i][j] = round(frequency_matrix[i][j]/total*100,2) 
    return frequency_matrix

def get_castle_data(games_dataframe):
    move_nums = []
    castled_first = []
    results = []

    for index, moves in enumerate(games_dataframe['Moves']):

        castle_index = moves.find("O-O")
        if castle_index != -1:
            try:
                move_number = get_move_number(moves, castle_index)
                if next_chunk_contains(moves, castle_index, "O-O"):
                    castled_first.append("same")
                elif was_white(moves, castle_index):
                    castled_first.append("w")
                else:
                    castled_first.append("b")

                move_nums.append(move_number)
                results.append(games_dataframe['Result'].iloc[index])
            except Exception as e:
                pass

    df_setup = {"Move Number": move_nums, "Castled First": castled_first, "Result": results}
    result_df = pd.DataFrame(data=df_setup)

    # Print the DataFrame to inspect results
    print(result_df)

    return result_df

def get_move_number(moves, move_index): #chatgpt helped debug and comment
    """
    Extracts the move number from a moves string given a specific move index using regular expressions.
    
    Args:
    - moves (str): The string containing all the moves.
    - move_index (int): The index within the moves string where the castling move occurs.
    
    Returns:
    - int: The move number if found, or None if not found or invalid.
    """
    # Regular expression to match move numbers (e.g., "1.", "2.", "10.")
    # Look for move numbers before the given index
    pattern = r'(\d+)\.\s'
    
    # Extract all matches before the given index
    snippet = moves[:move_index]
    matches = re.findall(pattern, snippet)
    
    if matches:
        # Return the most recent move number
        return int(matches[-1])
    else:
        print(f"Move number not found before index {move_index}")
        return None
    

def next_chunk_contains(moves, move_index, check): #checks whether the next "chunk" separated by a space includes a character or string
    next_chunk_index = moves.find(" ", move_index)
    if next_chunk_index == -1:
        print(f"Next chunk start not found for move at index {move_index}")
        return False

    next_chunk_end = moves.find(" ", next_chunk_index + 1)
    if next_chunk_end == -1:
        next_chunk_end = len(moves)

    next_chunk = moves[next_chunk_index + 1:next_chunk_end]
    return check in next_chunk

def was_white(moves, move_index): #determines whether a move was made by the white or black player
    if next_chunk_contains(moves, move_index, "."):
        return False
    return True

def aggregate_castle_data(castle_data): # sums castling data into single array
    occurrences_by_num = [0]*75
    for num in castle_data['Move Number']:
        try:
            occurrences_by_num[int(num)]+=1
        except:
            pass
    return occurrences_by_num

def castling_matrix(castle_data): # organizes castle data into a matrix by result and which player castled first
    square_frequencies = np.array([[0,0,0],[0,0,0],[0,0,0]])
    for i in range(len(castle_data)):
        if castle_data['Result'][i] == "1-0": #white won
            if castle_data['Castled First'][i] == "w": #white castled first and won
                square_frequencies[0][0]+=1
            elif castle_data['Castled First'][i] == "same": #white castled on the same move and won
                square_frequencies[0][1]+=1
            else: #white castled second and won
                square_frequencies[0][2] +=1
        elif castle_data['Result'][i] == "1/2-1/2": #draw
            if castle_data['Castled First'][i] == "w": #white castled first and drew
                square_frequencies[1][0]+=1
            elif castle_data['Castled First'][i] == "same": #white castled on the same move and drew
                square_frequencies[1][1]+=1
            else: #white castled second and drew
                square_frequencies[1][2]+=1
        else: #black won
            if castle_data['Castled First'][i] == "w": #white castled first and lost
                square_frequencies[2][0]+=1
            elif castle_data['Castled First'][i] == "same": #white castled on the same move and lost
                square_frequencies[2][1]+=1
            else:
                square_frequencies[2][2]+=1
    return square_frequencies

def pgn_to_matrix(pgn_moves): #also got ChatGPT to help with this; finds final board state from a list of moves
    # Initialize the chess board
    board = chess.Board()

    # Apply each move to the board
    for move in pgn_moves:
        board.push_san(move)
    
    # Initialize an empty 8x8 matrix
    board_matrix = np.full((8, 8), "", dtype='<U2')

    # Map the pieces to the matrix
    piece_map = board.piece_map()
    for square, piece in piece_map.items():
        row, col = divmod(square, 8)
        board_matrix[7 - row][col] = piece.symbol()

    return board_matrix

def get_pawn_positions(pieceSymbol, board_matrix): # finds the location of all the pawns (or actually any piece)
    positions = [0]*8
    for r in range(len(board_matrix)):
        for c in range(len(board_matrix[r])):
            if board_matrix[r][c] == pieceSymbol:
                positions[c]+=8-r
    return positions

def pawn_positions_data(games_dataframe): # runs prior functions to convert raw data into info about the pawns
    all_pawns = []
    for i in range(len(games_dataframe)):
        first_capture = games_dataframe['Moves'][i].find("x")
        game = games_dataframe['Moves'][i][0:first_capture]
        pgn_moves = game.split(" ")
        pgn_moves_stripped = []
        for n in range(len(pgn_moves)):
            if n % 3 != 0:
                pgn_moves_stripped.append(pgn_moves[n])
        try:
            board_matrix = pgn_to_matrix(pgn_moves_stripped)
            all_pawns.append(get_pawn_positions('P',board_matrix))
        except:
            pass
    return all_pawns

def aggregate_pawn_positions_data(pawns_data): # finds mean and standard deviation of pawn positions
    means = [0]*8
    stds = [0]*8
    n = len(pawns_data)
    for r in range(len(pawns_data)): # get sums
        for c in range(len(pawns_data[r])):
            means[c] += float(pawns_data[r][c])
    for i in range(len(means)): # divide by n
        means[i] = means[i]/n

    for r in range(len(pawns_data)): # get sample standard deviation
        for c in range(len(pawns_data[r])):
            stds[c] += (float(pawns_data[r][c])-means[c])**2
    for i in range(len(stds)): #divide by n-1 then take square root
        stds[i] = math.sqrt(stds[i]/(n-1))
    
    return pd.DataFrame(({'Mean':means, 'Standard Deviation':stds}))

# Example usage with a sample PGN move list
pgn_moves = ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6"]
board_matrix = pgn_to_matrix(pgn_moves)
print(board_matrix)
print(get_pawn_positions('P',board_matrix))
