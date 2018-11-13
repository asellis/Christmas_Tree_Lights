# Stores the Red/Green/Blue values for a single LED

class LED:
    def __init__(self, red=0, green=0, blue=0):
        self.r = red if red>=0 and red<=255 else 0
        self.g = green if green>=0 and green<=255 else 0
        self.b = blue if blue>=0 and blue<=255 else 0

    def set(self, red, green, blue):
        self.r = red if red>=0 and red<=255 else 0
        self.g = green if green>=0 and green<=255 else 0
        self.b = blue if blue>=0 and blue<=255 else 0

    def values(self):
        return [self.r, self.g, self.b]

    def __str__(self):
        return "LED red={} green={} blue={}".format(self.r, self.g, self.b)
