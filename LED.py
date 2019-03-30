# Stores the Red/Green/Blue values for a single LED

class LED:
    def __init__(self, red=0, green=0, blue=0):
        # Stores the given LED colors
        # If the values go out of range, the specified color
        # is set to 0
        self.r = red if red>=0 and red<=255 else 0
        self.g = green if green>=0 and green<=255 else 0
        self.b = blue if blue>=0 and blue<=255 else 0

    def set(self, red, green, blue):
        self.r = red if red>=0 and red<=255 else 0
        self.g = green if green>=0 and green<=255 else 0
        self.b = blue if blue>=0 and blue<=255 else 0

    def values(self):
        # Returns the LED values as a list
        return [self.r, self.g, self.b]

    def __str__(self):
        # Returns a string indicating the LED colors
        # Used for printing LED data
        return "LED red={} green={} blue={}".format(self.r, self.g, self.b)

    def __getitem__(self,key):
        # Returns the color based on the index given
        if key==0:
            return self.r
        elif key==1:
            return self.g
        elif key==2:
            return self.b
        else:
            return
