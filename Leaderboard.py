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


def high_score():
    highest_score = 0
    with open(filename, encoding="utf8") as file:
        csv_read = csv.DictReader(file)
        for line in csv_read:
            highest_score += int(line['score'])

    print(highest_score)
