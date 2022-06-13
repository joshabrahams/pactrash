import csv
import os.path

filename = "assets/leaderboard.csv"


def add_score(player_name, player_score):
    column_names = ['player_name', 'score']
    rows = [
        {'player_name': player_name, 'score': player_score}
    ]

    if not os.path.exists(filename):
        with open(filename, "w", encoding='UTF8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(rows)
            file.close()
    else:
        if player_name != "" and player_score != "":
            with open(filename, "a+") as file:
                writer = csv.DictWriter(file, fieldnames=column_names)
                writer.writerows(rows)
                file.close()



class Leaderboard:
    def __init__(self):
        self.highest_score = 0
        self.leaderboard_sorted = []

    def high_score(self):
        if os.path.exists(filename):
            with open(filename, encoding="utf8") as file:
                csv_read = csv.DictReader(file)
                for line in csv_read:
                    if int(line['score']) > self.highest_score:
                        self.highest_score = int(line['score'])
