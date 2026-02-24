# dates

# Python Dates
import datetime

x = datetime.datetime.now()
print(x)

# output
x = datetime.datetime.now()
print(x.year)
print(x.strftime("%A"))

# create object
x = datetime.datetime(2020, 5, 17)
print(x)

# The strftime() Method
x = datetime.datetime(2018, 6, 1)
print(x.strftime("%B"))


'''
# ДАТА
%d - День месяца (01-31)
%m - Номер месяца (01-12)
%y - Год короткий (22)
%Y - Год полный (2022)
%j - День года (001-366)

# ДЕНЬ НЕДЕЛИ
%a - День недели сокращенно (Sun)
%A - День недели полностью (Sunday)
%w - Номер дня недели (0-6, 0 = Воскресенье)
%u - Номер дня недели по ISO (1-7, 1 = Понедельник)

# МЕСЯЦ
%b - Название месяца сокращенно (Jan)
%B - Название месяца полностью (January)

# ВРЕМЯ
%H - Час 24-часовой формат (00-23)
%I - Час 12-часовой формат (01-12)
%p - AM или PM
%M - Минуты (00-59)
%S - Секунды (00-59)
%f - Микросекунды (000000-999999)

# НЕДЕЛИ
%W - Номер недели (Пн - первый день)
%U - Номер недели (Вс - первый день)
%V - Номер недели по ISO (01-53)

# ЛОКАЛИЗАЦИЯ И ЗОНЫ
%z - UTC смещение (+0300)
%Z - Название часового пояса (MSK)
%c - Дата и время полностью (Mon Dec 31 17:41:00 2018)
%x - Дата (12/31/18)
%X - Время (17:41:00)
%% - Символ процента
'''

# Write a Python program to subtract five days from current date.
from datetime import date, timedelta
today = date.today()
five_days_ago = today - timedelta(days=5)
print("Current date:", today)
print("5 days ago:", five_days_ago)

# Write a Python program to print yesterday, today, tomorrow.
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

# Write a Python program to drop microseconds from datetime.
from datetime import datetime
current_datetime = datetime.now()
clean_datetime = current_datetime.replace(microsecond=0)
print("Original:", current_datetime)
print("Without microseconds:", clean_datetime)

# Write a Python program to calculate two date difference in seconds.
# Creating two arbitrary dates
date1 = datetime(2023, 1, 1, 12, 0, 0)
date2 = datetime(2023, 1, 2, 14, 30, 0)

difference = date2 - date1
seconds_diff = difference.total_seconds()

print(f"Difference in seconds: {seconds_diff}")