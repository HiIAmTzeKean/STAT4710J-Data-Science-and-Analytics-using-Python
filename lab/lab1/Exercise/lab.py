# lab.py


from itertools import tee
from pathlib import Path
import io
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if ints == []:
        return False
    for i in range(len(ints)-1):
        if ints[i]==ints[i+1]+1:
            return True
    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    if nums ==[]: return False
    if nums[len(nums)//2] <= sum(nums)/len(nums):
        return True
    return False


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def same_diff_ints(ints):
    if ints == []: return False
    for iteration in range(1, len(ints)):
        for i in range(len(ints)-iteration):
            if abs(ints[i]-ints[i+iteration])==iteration:
                return True
    return False


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    text = ""
    for i in range(n):
        text = s[:i+1] + text
    return text


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    # exploding a number to the right is the only way to cause the number of digits
    # needed to increase
    max_num=max(ints)
    number_of_digits = len(str(max_num+n))
    exploded = []
    for i in ints:
        text = f"{str.zfill(str(i))}"
        for j in range(n):
            text = text + f" {str.zfill(str(i+j+1))}"
            text = f"{str.zfill(str(i-j-1))} " + text
        exploded.append(text)
    return exploded


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------

def add_root(A: np.ndarray):
    return A + np.sqrt(np.arange(0,len(A)))

def where_square(A):
    return np.sqrt(A)%1==0


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def growth_rates(A):
    B = np.roll(A,-1)
    B[-1] = A[-1]
    return np.around((B-A)/A,2)
    

def with_leftover(A):
    try:
        return np.where(np.cumsum(20%A)>A)[0][0]
    except:
        False


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def salary_stats(salary:pd.DataFrame):
    stats = {
        'num_players': len(salary),
        'num_teams': len(pd.unique(salary['Team'])),
        'total_salary': salary['Salary'].sum(),
        'highest_salary': salary.nlargest(1,'Salary')['Player'].iloc[0],
        'avg_los': round(salary[salary['Team']=='Los Angeles Lakers']['Salary'].mean(),2),
        'fifth_lowest': ', '.join(salary.sort_values('Salary',ascending=True).iloc[4].get(['Player','Team']).tolist()),
        'duplicates': salary['Player'].replace({'Jr.':'','lll':''}).str.split(' ').str[1].value_counts().sum()!=0,
        'total_highest': salary[salary['Team']==salary.nlargest(1,'Salary')['Team'].iloc[0]]['Salary'].sum()
    }
    return pd.Series(stats)



