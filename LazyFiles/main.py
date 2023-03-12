import app

key = input('Please provide valid API key:\n')
number_of_days = input('How many days would you like to log?\n')
links = input('Please provide the links with one comma in between:\n')
links = links.split(',')
day = 1
while day <= int(number_of_days):
    app.run_logger(key,links[day],day)
    day = day + 1