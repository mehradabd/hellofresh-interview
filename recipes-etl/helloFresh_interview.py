"""importing necessary packages:
'pandas' for modifying data,
'json' for reading json file,
and 're' for using regular expression
"""
import pandas as pd
import json
import re

# loading json file and converting it into a list
recipes_data = [json.loads(line) for line in open('recipes.json', 'r')]

# selecting recipes with only 'Chilies as one the ingredients. "\bCh(i|e)l(l|i|e)?" is the regular expression used
# for misspelling and singular form of Chilies
chilies_recipes = list(filter(lambda x: re.search(r'\bCh(i|e)l(l|i|e)?',
                                                  x['ingredients'], flags=re.IGNORECASE), recipes_data))


def time_translation(time_string):
    """
    This function translates values of 'cookTime' and 'prepTime' ,which are in the string format, into integers
     so then we can calculate the difficulty. The function outputs the sum of hours and minutes in the string.

    Parameter:
        time_string (str): cookTime or prepTime in string format

    Returns:
        time (int): the integer time it takes to cook or prep a recipe
     """
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
    """
    This function outputs the difficulty level of a recipe with respect to the cook time and prep time of it.

    Parameters:
        cook_time (str): cookTime in string format
        prep_time (str): prepTime in string format

    Returns:
        difficulty level (str): difficulty level of recipe which could be "Hard", "Medium", "Easy",
         or "Unknown" if both cookTime and prepTime are None.
    """
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


# Converting the list to a data frame
chilies_df = pd.DataFrame(chilies_recipes)

# Adding the difficulty column using the "difficulty_assigner" function to each record.
chilies_df['difficulty'] = [difficulty_assigner(chilies_df["cookTime"][i],
                                                chilies_df["prepTime"][i]) for i in range(len(chilies_df))]

# saving the results to a csv file
chilies_df.to_csv("recipes.csv")
