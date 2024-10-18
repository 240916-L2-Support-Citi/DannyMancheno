import os
import datetime

filename='/home/danny/Revature/Project1/python/alert.txt'
content='"\033[31mThis text is red\033[0m"'

ampm='AM'
if datetime.datetime.now().hour >= 12:
    ampm='PM'

# with open(filename, 'a') as file:
#    file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M {ampm}"))
   
print(f'\033[4m{datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M {ampm}")}\033[0m')
