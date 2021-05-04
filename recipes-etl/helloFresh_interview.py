import pandas as pd
import json
import re

recipes_data = [json.loads(line) for line in open('recipes.json', 'r')]
chilies_recipes = list(filter(lambda x: re.search(r'\bCh(i|e)l(l|i|e)?', x['ingredients'], flags=re.IGNORECASE),
                              recipes_data))

chilies_df = pd.DataFrame(chilies_recipes)


def time_translation(time_string):
    hours = 0
    minutes = 0
    hour_index = 0
    hour_seen = False
    for index, letter in enumerate(time_string):
        if letter == "H":
            hours = int(time_string[2: index]) * 60
            hour_seen = True
            hour_index = index
        if letter == "M" and hour_seen:
            minutes = int(time_string[hour_index + 1: index])
        elif letter == "M" and not hour_seen:
            minutes = int(time_string[2: index])
    if hours == 0 and minutes == 0:
        return None
    else:
        return hours + minutes


def difficulty_assigner(cook_time, prep_time):
    cook_time = time_translation(cook_time)
    prep_time = time_translation(prep_time)

    if not cook_time and not prep_time:
        return "Unknown"
    elif not cook_time:
        total_time = prep_time
    elif not prep_time:
        total_time = cook_time
    else:
        total_time = cook_time + prep_time

    if total_time > 60:
        return 'Hard'
    elif 30 <= total_time <= 60:
        return "Medium"
    elif total_time < 30:
        return "Easy"
    else:
        return "Unknown"


chilies_df['difficulty'] = [difficulty_assigner(chilies_df["cookTime"][i], chilies_df["prepTime"][i]) for i in
                            range(len(chilies_df))]
chilies_df.to_csv("hello.csv")
