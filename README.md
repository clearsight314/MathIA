This repository contains all the code used to preprocess the data for my IB Mathematics: Applications and Interpretations HL IA, which analyzes chess playing at different levels.

If you want to recreate the processed data I obtained, you must download the raw csv files from these places:

Masters data: https://database.nikonoel.fr/
General data: https://www.kaggle.com/datasets/arevel/chess-games

Both are sourced from Lichess originally, but I preferred to get the data from these secondary sources because it did not involve downloading 20+gb files.

The "general data" contains computer evaluations in the move list, so it must be cleaned with clean_csv.py.
