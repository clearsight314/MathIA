import pandas as pd
"""
This entire file is dedicated to cleaning up the messy pgn data from Kaggle.
Computer analyses were in many of the move lists which caused issues in the other code.
I did use ChatGPT to help me fix my code here.
"""
def clean_chess_moves(csv_file_path, output_file_path=None):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    def clean_moves(move_str):
        cleaned_moves = []
        move_parts = move_str.split()  # Split the moves by whitespace
        
        for part in move_parts:
            # Check if the part is a move, move number, or includes a check/checkmate
            if any(char in part for char in "abcdefgh12345678") or part in ["O-O", "O-O-O"]:
                cleaned_moves.append(part)
            elif part.endswith(('+', '#')):  # Check and checkmate
                cleaned_moves.append(part)
            elif part.endswith('.'):
                cleaned_moves.append(part)  # Include move numbers like '1.'
        
        return ' '.join(cleaned_moves)

    # Apply the cleaning function to the 'AN' column and rename it to 'Moves'
    df['Moves'] = df['AN'].apply(clean_moves)
    
    # Drop the original 'AN' column
    df.drop(columns=['AN'], inplace=True)

    # Optionally, save the cleaned data to a new CSV file
    if output_file_path:
        df.to_csv(output_file_path, index=False)

    return df


print("beginning file cleanup...")
cleaned_df = clean_chess_moves('chess_games.csv', 'gen_games.csv') # cleans file chess_games.csv and puts output into gen_games.csv
print(cleaned_df.head())
print("done!")
