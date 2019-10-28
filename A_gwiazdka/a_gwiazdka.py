import math
import numpy as np
import datetime
def heurastyka(p1,p2):
    X=p1[0]-p2[0]
    Y=p1[1]-p2[1]
    return math.sqrt(X**2+Y**2)
def dzieci(pozycja,mapa):
    tablica=[]
    for x,y in [(1,0),(-1,0),(0,1),(0,-1)]:
        dx=pozycja[0]+x
        dy=pozycja[1]+y
        if(dx<0 or dx>mapa.shape[0]-1 or dy<0 or dy>mapa.shape[1]-1):
            continue
        if(mapa[dx][dy]!=0):
            continue
        tablica.append((dx,dy))
    return tablica
def A_Star(start,koniec,mapa):
    G={}
    F={}
    G[start]=0
    F[start]=heurastyka(start,koniec)
    zamkniete=set()
    otwarte= {start}
    rodzic={}
    while len(otwarte)>0:
        aktualny=None
        aktualnyf=None
        for p in otwarte:
            if aktualny is None or F[p]<aktualnyf:
                aktualny=p
                aktualnyf=F[p]


        if aktualny==koniec:
            droga=[aktualny]
            while aktualny in rodzic:
                aktualny=rodzic[aktualny]
                droga.append(aktualny)
            droga.reverse()
            return droga
        otwarte.remove(aktualny)
        zamkniete.add(aktualny)
        for sasiad in dzieci(aktualny,mapa):
            if sasiad in zamkniete:
                continue
            dzieckoG=G[aktualny]+1
            if sasiad not in otwarte:
                otwarte.add(sasiad)
            elif dzieckoG>=G[sasiad]:
                continue
            rodzic[sasiad]=aktualny
            G[sasiad]=dzieckoG
            H=heurastyka(sasiad,koniec)
            F[sasiad]=G[sasiad]+H
    return ValueError("Nie można znaleźć drogi")

def main():
    start=(0,19 )
    stop=(19,0)
    mapa=np.loadtxt("grid.txt")
    czas=datetime.datetime.now()
    droga=A_Star(start,stop,mapa)
    czask=datetime.datetime.now()-czas
    mapa2=mapa
    for x in droga:
        mapa2[x[0]][x[1]]=2
    mapa2[start[0]][start[1]]=1
    mapa2[stop[0]][stop[1]]=3
    print(mapa2)
    print(czask)

if __name__=="__main__":
    main()