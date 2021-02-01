import parking
from time import sleep
from datetime import datetime


def parking_loop():
    counter = 0
    while True:
        parking.check_page_change()
        counter += 1
        print(str(counter) + " times looped. Time: ", datetime.now())
        counter += 1
        sleep(1800) #Loops every 30 minutes