#!/usr/bin/python

import datetime
import flipdot
import random
import time

def main():
    panel = flipdot.flipdot()

    try:
        input("Press enter to start")
    except SyntaxError as err:
        pass

    panel.clear_panel()

    # Random dots
#    for i in range(10):
#        for col in range(0, 55):
#            for row in range(0, 16):
#                panel.set_pixel(col, row, random.choice([0, 1]))

    # Date, time
#    date = datetime.datetime.now().strftime("%c")
#    date = datetime.datetime.now().strftime("%A")
    date = datetime.datetime.now().strftime("%H:%M %A")
    panel.write_string(date)
    time.sleep(3)

    panel.write_string("Hello!")

    print "spinning until interrupt"
    panel.set_addr(0, 0)

    while True:
        pass

if __name__ == "__main__":
    main()
