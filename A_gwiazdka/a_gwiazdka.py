import math
import numpy as np
import datetime
from PIL import Image, ImageOps

__author__ = "Patryk Szczygielski"
__version__ = "alpha 2.23"
__email__ = "patryk8199@gmail.com"
__desc__ = "Algorytm a-gwiazdka stworzony na podstawie wykładu z Elementów Robotyki Inteligentnej,oraz filmu na yt: " \
           "https://www.youtube.com/watch?v=eSOJ3ARN5FM dla lepszego zrozumienia działania algorytmu "


def heurastyka(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return math.sqrt(x ** 2 + y ** 2)


# funckja sprawdzająca dzieci aktualnego punktu
def dzieci(pozycja, mapa):
    tablica = []
    for x in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dx = pozycja[0] + x[0]
        dy = pozycja[1] + x[1]
        if dx < 0 or dx > mapa.shape[0] - 1 or dy < 0 or dy > mapa.shape[1] - 1:
            continue
        if mapa[dx][dy] != 0:
            continue
        tablica.append((dx, dy))
    return tablica


# wyjątek w przypadku braku droga
class BrakDrogi(Exception):
    pass


def a_gwiazdka(start, koniec, mapa):
    g = {}
    f = {}
    pass
    g[start] = 0
    f[start] = heurastyka(start, koniec)
    if mapa[koniec[0]][koniec[1]] != 0:
        print("Punkt końcowy jest przeszkodą")
        return None
    if start == koniec:
        print("Punkt początkowy jest też punktem końcowym")
        return [start]
    zamkniete = set()
    otwarte = {start}
    rodzic = {}
    while otwarte:
        aktualny = None
        aktualnyf = None
        for p in otwarte:
            if aktualny is None or f[p] < aktualnyf:
                aktualny = p
                aktualnyf = f[p]
        # odtwarzanie drogi po tablicy(słowniku)rodziców
        if aktualny == koniec:
            droga = set()
            droga.add(aktualny)
            while aktualny in rodzic:
                aktualny = rodzic[aktualny]
                droga.add(aktualny)
            return droga

        otwarte.remove(aktualny)
        zamkniete.add(aktualny)

        for sasiad in dzieci(aktualny, mapa):
            if sasiad in zamkniete:
                continue
            if sasiad not in otwarte:
                otwarte.add(sasiad)
            elif g[aktualny]+1 >= g[sasiad]:
                continue
            rodzic[sasiad] = aktualny
            g[sasiad] = g[aktualny]+1
            h = heurastyka(sasiad, koniec)
            f[sasiad] = g[sasiad] + h
    raise BrakDrogi


def rysuj_mape(mapka, start, stop, trasa):
    mapa = np.zeros((mapka.shape[0], mapka.shape[1], 3), dtype=np.uint8)
    for x in range(mapka.shape[0]):
        for y in range(mapka.shape[1]):
            mapa[x][y] = [255, 255, 255]
            if mapka[x][y] == 5:
                mapa[x][y] = [0, 0, 0]
    for x in trasa:
        mapa[x[0]][x[1]] = [0, 225, 225]
    mapa[start[0]][start[1]] = [150, 225, 0]
    mapa[stop[0]][stop[1]] = [225, 0, 0]
    img = Image.fromarray(mapa, 'RGB')
    img = img.resize((512, 512), resample=0)
    img = ImageOps.expand(img, 10, 'black')
    img.show()


def main():
    start = (0, 0)
    stop = (13, 5)
    mapa = np.loadtxt("grid.txt")
    try:
        czas = datetime.datetime.now()
        droga = a_gwiazdka(start, stop, mapa)
        czask = datetime.datetime.now() - czas
        mapa2 = mapa
        for x in droga:
            mapa2[x[0]][x[1]] = 1
        mapa2[start[0]][start[1]] = 2
        mapa2[stop[0]][stop[1]] = 3
        print(mapa2)
        print(czask)
        rysuj_mape(mapa, start, stop, droga)
    except BrakDrogi:
        print("Nie znaleziono drogi")


if __name__ == "__main__":
    main()
