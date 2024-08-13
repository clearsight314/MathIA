This repository contains all the code used to preprocess the data for my IB Mathematics: Applications and Interpretations HL IA, which analyzes chess playing at different levels.

If you want to recreate the processed data I obtained, you must download the raw csv files from these places:

Masters data: https://database.nikonoel.fr/
General data: https://www.kaggle.com/datasets/arevel/chess-games

Both are sourced from Lichess originally, but I preferred to get the data from these secondary sources because it did not involve downloading 20+gb files.

The "general data" contains computer evaluations in the move list, so it must be cleaned with clean_csv.py.

I am not a software engineer by any means, so this code is not very well optimized or generalized. It may take several minutes to run the code on large files, and filenames must be changed in the code to match the downloaded csv names. All outputs are displayed in the terminal.

If the code does not work, ensure that all the imported libraries and python3 are installed.
