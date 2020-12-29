import datetime
import requests
import calendar
import time
from bs4 import BeautifulSoup
from datetime import date


def ord(n):  # returns st, nd, rd and th
    return str(n) + (
        "th" if 4 <= n % 100 <= 20 else {
            1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    )


# Scrapes rubbish collection dates ** USE roadID=2767 TO POST **
URL = "https://apps.castlepoint.gov.uk/cpapps/index.cfm?roadID=2757&fa=wastecalendar.displayDetails"
raw_html = requests.get(URL)
data = BeautifulSoup(raw_html.text, "html.parser")

pink = data.find_all('td', class_='pink', limit=4)
black = data.find_all('td', class_='normal', limit=4)
month = data.find('div', class_='calMonthCurrent')
todays_date = datetime.date.today()

# creats sack lists
pink_sack = []
for div in pink:
    n = div.text
    pink_sack.append(n)
pink_sack = list(map(int, pink_sack))

black_sack = []
for div in black:
    n = div.text
    black_sack.append(n)
black_sack = list(map(int, black_sack))

# creats pink/black list in date order
color_sack = []
color_sack = [None]*(len(pink_sack)+len(black_sack))
if pink_sack[0] < black_sack[0]:
    color_sack[::2] = pink_sack
    color_sack[1::2] = black_sack
else:
    color_sack[::2] = black_sack
    color_sack[1::2] = pink_sack

# sorts months
second_month_start = [i for i in range(len(color_sack)-1) if (color_sack[i] > color_sack[i+1])]
second_month_start = int("".join(map(str, second_month_start))) + 1 # converts list to integer

current_month_list = (color_sack[:(second_month_start)])

next_month_list = (color_sack[(second_month_start):])

# checks today for rubbish
if todays_date.day in current_month_list:
    print(f"Today {(ord(todays_date.day))}", end=" ")
    if todays_date.day in pink_sack:
        print("is pink")
    elif todays_date.day in black_sack:
        print("is black")

# Looks for the next rubbish day
try:
    next_rubbish_day = next(
        x for x in current_month_list if x > todays_date.day)
except StopIteration:
    next_rubbish_day = next_month_list[0]
    if todays_date.month == 12 and next_rubbish_day == next_month_list[0]:
        todaysmonth=todays_date.month%12+1
        todaysyear=todays_date.year+1
    else:
        todaysmonth=todays_date.month
        todaysyear=todays_date.year
    day = calendar.weekday(
        (todaysyear), (todaysmonth), (next_rubbish_day))
else:
    next_rubbish_day = next(
        x for x in current_month_list if x > todays_date.day)
    day = calendar.weekday(
        (todays_date.year), (todays_date.month), (next_rubbish_day))

# print(next_rubbish_day)
print(f"Next rubbish day is {(calendar.day_name[day])} the {(ord(next_rubbish_day))}" +
      (" and is Pink" if next_rubbish_day in pink_sack else " and is Black"))
