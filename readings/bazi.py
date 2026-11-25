from datetime import date

# Chinese New Year dates - extend 1924-2044
CNY = {
    1987: date(1987, 1, 29),
    1988: date(1988, 2, 17),
    1990: date(1990, 1, 27),
    2000: date(2000, 2, 5),
    # Add the rest from your existing table / lunar calendar
}

ANIMALS = ['Rat','Ox','Tiger','Rabbit','Dragon','Snake',
           'Horse','Goat','Monkey','Rooster','Dog','Pig']

def year_animal(d):
    y = d.year
    cny = CNY.get(y)
    if cny and d < cny:
        y -= 1
    return ANIMALS[(y - 4) % 12]

# Test cases - must pass before launch:
# 1990-06-15 -> Horse
# 1988-01-01 -> Rabbit (1987 year, CNY 1988-02-17)
# 2000-02-05 -> Dragon (CNY day)
# 2000-02-04 -> Rabbit
