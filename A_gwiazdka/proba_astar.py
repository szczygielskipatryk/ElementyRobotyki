import numpy as np
import math

class punkt:
    def __init__(self, rodzic, pozycja):
        self.rodzic = rodzic
        self.pozycja = pozycja
        self.f = self.h = self.g = 0

    def heur(self, koniec):
        return math.sqrt((self.pozycja[0] - koniec.pozycja[0]) ** 2 + (self.pozycja[1] - koniec.pozycja[1]) ** 2)

    def __eq__(self, other):
        return self.pozycja == other.pozycja

    def __hash__(self):
        return id(self)


def A_star(grid, start, stop):
    otwarte = set()
    zamkniete = set()
    otwarte.add(start)
    if(grid[stop.pozycja[0]][stop.pozycja[1]]!=0):
        print("Punkt końcowy jest przeszkodą")
        return None
    if(start==stop):
        print("Punkt startowy jest też punktem końcowym")
        return None

    while otwarte:
        aktualne=min(otwarte,key=lambda p:p.f)
        if aktualne==stop:
            akt=aktualne
            droga=[]
            while akt is not None:
                droga.append(akt.pozycja)
                akt=akt.rodzic
            return droga[::-1]
        dzieci=set()
        for wsp in [(1,0),(0,-1),(-1,0),(0,1)]:
            wsp_kid=(aktualne.pozycja[0]+wsp[0],aktualne.pozycja[1]+wsp[1])
            if(wsp_kid[0]>grid.shape[0]or wsp_kid[0]<0 or wsp_kid[1]>grid.shape[1]or wsp_kid[1]<0):
                continue
            if(grid[wsp_kid[0]][wsp_kid[1]]!=0):
                continue
            kid=punkt(aktualne,wsp_kid)
            dzieci.add(kid)
        for pot in dzieci:
            if pot in zamkniete:
                continue
            if pot in otwarte:
                nowe_g=aktualne.g+1##1 to koszt ruchu
                if nowe_g<pot.g:
                    pot.g=nowe_g
                    pot.rodzic=aktualne

            else:
                pot.g=aktualne.g+1
                pot.h=pot.heur(stop)
                pot.f=pot.g+pot.h
                pot.rodzic=aktualne
                otwarte.add(pot)
    raise ValueError("Nie znaleziono ścieżki")

def main():
    start=punkt(None,(0,0))
    stop=punkt(None,(2,3))
    mapa=np.loadtxt("grid.txt")
    droga=A_star(mapa,start,stop)
    print(droga)

if __name__==("__main__"):
    main()