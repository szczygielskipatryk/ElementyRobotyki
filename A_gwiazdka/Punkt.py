import math
class Punkt:
    def __init__(self,pozycja,rodzic):
        self.pozycja=pozycja
        self.rodzic=rodzic
        self.h=self.g=self.f=0
    def __eq__(self, other):
        return self.pozycja==other.pozycja
    def wyliczH(self,other):
        X=self.pozycja[0]-other.pozycja[0]
        Y=self.pozycja[1]-other.pozycja[1]
        return math.sqrt(X**2+Y**2)
    