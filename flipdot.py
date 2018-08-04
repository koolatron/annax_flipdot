#!/usr/bin/python

# This could be more general

import gpiozero
import time
from PIL import Image, ImageDraw, ImageFont
import pprint
import random

DEFAULT_ROW_PINS = [21, 20, 16, 12]
DEFAULT_COL_PINS = [26, 19, 13, 6, 5, 11, 9]
DEFAULT_STROBE_PIN = 7
DEFAULT_DATA_PIN = 8

COL_ADDR_BITS = 7
ROW_ADDR_BITS = 4

COLS = 110
ROWS = 16

class flipdot:

    def __init__(self, row_pins=DEFAULT_ROW_PINS, col_pins=DEFAULT_COL_PINS, strobe_pin=DEFAULT_STROBE_PIN, data_pin=DEFAULT_DATA_PIN, rows=ROWS, cols=COLS):
        self.strobe_pin = gpiozero.OutputDevice(strobe_pin, active_high=False)
        self.data_pin = gpiozero.OutputDevice(data_pin)
        self.row_pins = []
        self.col_pins = []

        self.rows = rows
        self.cols = cols

        for pin in row_pins:
            self.row_pins.append(gpiozero.OutputDevice(pin))

        for pin in col_pins:
            self.col_pins.append(gpiozero.OutputDevice(pin))

        self.all_pins = self.row_pins + self.col_pins + [self.strobe_pin] + [self.data_pin]
        self.panel_state = [[0] * self.rows for i in range(self.cols)]

        for pin in self.all_pins:
            pin.off()


    def cleanup(self):
        for pin in self.all_pins:
            pin.off()
            pin.close()


    def _set_addr(self, x, y):
        # avoid unmapped addresses between panels
        if (x > 29):
            if (x > 54):
                if (x > 84):
                    x += 2
                x += 7
            x += 2
    
        x = [int(digit) for digit in bin(x)[2:]]
        y = [int(digit) for digit in bin(y)[2:]]
    
        x.reverse()
        y.reverse()
    
        # expand col addr to 7 bits
        for i in range(len(x), 7):
            x.append(0)
    
        # expand row addr to 4 bits
        for i in range(len(y), 4):
            y.append(0)
    
        # TODO: Consider caching the address line states and only changing if necessary
        for pos in range(len(x)):
            if (x[pos] == self.col_pins[pos].value):
                continue
    
            if (x[pos] == 0):
                self.col_pins[pos].off()
            else:
                self.col_pins[pos].on()
    
        for pos in range(len(y)):
            if (y[pos] == self.row_pins[pos].value):
                continue
    
            if (y[pos] == 0):
                self.row_pins[pos].off()
            else:
                self.row_pins[pos].on()


    def _set_pixel(self, x, y, state):
        # TODO: raise ValueError and/or IndexError on state/bounds respectively

        if (self.panel_state[x][y] == state):
            return

        self._set_addr(x, y)

        # TODO: Consider caching the data pin state and only changing if necessary
        if (state == 0):
            self.data_pin.off()
        else:
            self.data_pin.on()

        self.strobe_pin.on()
        time.sleep(0.001)

        self.strobe_pin.off()

        self.panel_state[x][y] = state


    def _get_pixel(self, x, y):
        return self.panel_state[x][y]


    def set_panel(self, buffer, transitionType=None):
        addrs = [(x, y) for x in range(110) for y in range(16)];

        if transitionType == "dissolve":
            random.shuffle(addrs)

        if transitionType == "dual-wipe":
            addrs = []
            for x in range(0, 110):
                for y in range(0, 16, 2):
                    addrs.append((x,y))
                    addrs.append((109-x,y+1))

        for (x, y) in addrs:
            self._set_pixel(x, y, buffer[x][y])


    def clear_panel(self):
        for x in range(COLS):
            for y in range(ROWS):
                self._set_pixel(x, y, 1)

        for x in range(COLS):
            for y in range(ROWS):
                self._set_pixel(x, y, 0)


    def write_string(self, string, transitionType=None, justification=None, font=None):
        img = Image.new('1', (110, 16))
        d = ImageDraw.Draw(img)
        f = ImageFont.truetype("fonts/Arial Black.ttf", 14)
        w, h = d.textsize(string, font=f)

        xpos = 2
        ypos = (16-h)/2

        if justification == "center":
            xpos = (110-w)/2

        d.text((xpos, ypos), string, fill=(1), font=f)
    
        raw_data = list(img.getdata())
    
        arr = []
        for i in range(16):
            a = i * 110
            b = (i + 1) * 110
            arr.append(raw_data[a:b])

        # Transpose array
        arr2 = map(list, zip(*arr))
 
        self.set_panel(arr2, transitionType=transitionType)
