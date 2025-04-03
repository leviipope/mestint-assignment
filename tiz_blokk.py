from keres import *

class TizBlokk_problema(Feladat):
    def __init__(self):
        ke = ('zöld', 'zöld', 'zöld', 'üres', 'üres', 'üres', 'üres', 'piros', 'piros', 'piros')
        c = ('piros', 'piros', 'piros', 'üres', 'üres', 'üres', 'üres', 'zöld', 'zöld', 'zöld')

        super().__init__(ke, c)

        # Szomszédossági fgv
        self.szomszéd = {
            0: [1],
            1: [0, 2, 3],
            2: [1],
            3: [1, 5],
            4: [5],
            5: [3, 4, 6],
            6: [5, 8],
            7: [8],
            8: [6, 7, 9],
            9: [8]
        }

    def célteszt(self, állapot):
        return állapot == self.cél

    def rákövetkező(self, állapot):
        gyerekek = []

        # Színes elemek megkeresése
        for i in range(10):
            if állapot[i] in ['zöld', 'piros']:
                # Szomszédos pozíciók ellenőrzése
                for j in self.szomszéd[i]:
                    # Ha a szomszédos pozíció üres
                    if állapot[j] == 'üres':
                        # Új állapot létrehozása az elem mozgatásával
                        új_állapot = list(állapot)
                        új_állapot[j] = állapot[i]
                        új_állapot[i] = 'üres'
                        gyerekek.append((f"mozgat({i}, {j})", tuple(új_állapot)))

        return gyerekek


if __name__ == "__main__":
    problem = TizBlokk_problema()

    #csúcs = szélességi_gráfkereső(problem)
    csúcs = mélységi_fakereső(problem)

    út = csúcs.út(); út.reverse()
    lépések = csúcs.megoldás()
    print(f"Lépések száma: {len(lépések)}")

    # Az állapotok és a hozzájuk tartozó operátorok együttes kiírása
    # Az első állapot a kezdeti állapot, amihez nincs művelet
    print(f"1. {út[0]} (kezdő állapot)")

    # A többi állapothoz hozzárendeljük a megfelelő műveletet
    for i in range(1, len(út)):
        print(f"{i + 1}. {út[i]} (művelet: {lépések[i - 1]})")
