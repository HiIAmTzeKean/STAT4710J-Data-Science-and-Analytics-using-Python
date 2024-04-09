# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False
        
    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True
    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    if (n%2 == 0):
        median = (sorted_nums[int(n/2 - 1)] + sorted_nums[int(n/2)]) / 2
    else:
        median = sorted_nums[int(n/2)]
    
    mean = sum(sorted_nums)/n
    
    if(median>=mean):
        return False
    else:
        return True


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def same_diff_ints(ints):
    # n = len(ints)
    # if n == 0:
    #     return False
    # for i in range(n):
    #     for j in range(n):
    #         if ints[i] != ints[j] and (i - j) == abs(ints[i] - ints[j]):
    #             return True
    # return False
####If the loop is written as above, you get half of the credit because 
####it is not "**running quicker in cases where the pairs are close together than in cases where the pairs are further apart**"
    n = len(ints)
    if n == 0:
        return False
    for d in range(1,n):
        for j in range(0,n-1):
            if j+d<n and ints[j] != ints[j+d] and d == abs(ints[j+d] - ints[j]):
                return True
    return False

    

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    if n <= 0:
        return ""
    result = ""
    for i in range(n + 1):
        result += s[:n - i]
    return result


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------

def get_max_num_digits(ints, n):
    digits = np.array([])
    num_digits = np.array([])
    for num in ints:
        digits = np.append(digits, num - 2)
        digits = np.append(digits, num + 2)
    for num in digits:
        length = len(str(int(num)))
        num_digits = np.append(num_digits, length)
    return int(max(num_digits))

def exploded_numbers(ints, n):
    output = np.array([])
    max_num_digits = get_max_num_digits(ints, n)

    for num in ints:
        left = num - n
        right = num + n
        s = ""
        for i in range(left, right + 1):
            s += str(i).zfill(max_num_digits)
            if (i != right):
                s += " "
        output = np.append(output, s)
    return output.tolist()

# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    return  A + np.sqrt(np.arange(len(A)))

def where_square(A):
    return ((A ** 0.5) % 1 == 0)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def growth_rates(A):
    return np.round(np.diff(A)/A[:-1],2)

def with_leftover(A):
    leftover = np.cumsum(20%A)
    can_buy = (A <= leftover)
    if True not in can_buy:
        return -1
    else:
        return can_buy.tolist().index(True)


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def salary_stats(salary):
    # The number of players
    try:
        num_players = len(salary["Player"].unique())
    except:
        num_players = None
    # The number of teams
    try:
        num_teams = salary.groupby("Team").count().shape[0]
    except:
        num_teams = None
    # The total salary amount over the season
    try:
        total_salary = salary["Salary"].sum()
    except:
        total_salary = None
    # The name of the player with the highest salary
    try:
        highest_salary = salary.sort_values("Salary").iloc[-1].get("Player")
    except:
        highest_salary = None
    # The average salary of the Boston Celtics ('BOS'), rounded to the nearest hundredth
    try:
       avg_bos = round(salary.groupby("Team").mean().loc["BOS"].get("Salary"), 2)
   
    except:
       avg_bos = None
       #The name of player and the name of the team whose salary is the third-lowest, separated by a comma and a space (e.g. John Doe, MIA)
    try:
       # if there are ties, return the first based on alphabetical order
       # sort "Salary" then "Player", if there are ties, the data are sorted according to alphabetical order of names
       third_lowest_row = salary.sort_values(by = ["Salary", "Player"]).iloc[2]
       third_lowest_name = third_lowest_row.get("Player")
       third_lowest_team = third_lowest_row.get("Team")
       third_lowest = third_lowest_name + ", " + third_lowest_team
    
    except:
       third_lowest = None
   # Whether there are any duplicate last names (True: yes, False: no), as a boolean
    try:
       last_names = salary["Player"].str.split().str[1]
       num_last_names = len(last_names.unique())
       duplicates = (num_last_names < num_players)
    except:
       duplicates = None
   # The total salary of the team that has the highest paid player
    try:
       highest_paid_player_team = salary[salary["Player"] == highest_salary]["Team"].iloc[0]
       total_highest = salary.groupby("Team").sum().loc[highest_paid_player_team].get("Salary")
    except:
       total_highest = None
    values = [num_players, num_teams, total_salary, highest_salary, avg_bos, third_lowest, duplicates, total_highest]
    indcies = ["num_players", "num_teams", "total_salary", "highest_salary", "avg_bos", "third_lowest", "duplicates", "total_highest"]
    return pd.Series(values, index = indcies)
    



