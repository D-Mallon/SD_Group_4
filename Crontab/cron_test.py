import datetime

# Get the current date and time
now = datetime.datetime.now()

# Open the file and append the date
with open('/home/ubuntu/dates.txt', 'a') as f:
    f.write(str(now) + '\n')

