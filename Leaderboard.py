import csv
import os.path

filename = "assets/leaderboard.csv"


def leaderboard(player_name, player_score):
    column_names = ['player_name', 'score']
    rows = [
        {'player_name': player_name, 'score': player_score}
    ]

    if not os.path.exists(filename):
        with open(filename, 'w', encoding='UTF8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(rows)
    else:
        with open(filename, 'a', encoding='UTF8') as file:
            writer = csv.DictWriter(file, fieldnames=column_names)
            writer.writerows(rows)
