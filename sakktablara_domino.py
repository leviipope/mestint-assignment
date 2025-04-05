from keres import *

class Sakktabla_domino(Feladat):
    def __init__(self):
        tabla = tuple(tuple(0 for _ in range(8)) for _ in range(8))
        self.kezdő = (tabla, 0)
        self.cél = None  # inkabb felbontjuk a céltesztben

    def célteszt(self, allapot):
        B, d = allapot

        return d == 21 and sum(sum(row) for row in B) == 63 # 21 domino lefed 63 kockat

    def rákövetkező(self, allapot):
        B, d = allapot
        gyerekek = []

        # tuple-k tuple-je -> list-k list-je
        B_list = [list(row) for row in B]

        # horizontalis lerakás
        for i in range(8):
            for j in range(6):  #  csak j = 5 -ig tud menni
                # 3 egymas melletti mező szabad e
                if B[i][j] == 0 and B[i][j + 1] == 0 and B[i][j + 2] == 0:
                    uj_B_list = [row.copy() for row in B_list]
                    uj_B_list[i][j] = uj_B_list[i][j + 1] = uj_B_list[i][j + 2] = 1 # lerakás
                    uj_B = tuple(tuple(row) for row in uj_B_list)
                    uj_d = d + 1
                    gyerekek.append((f"lerak_vizszintes({i + 1}, {j + 1})", (uj_B, uj_d)))

        # vertikalis lerakás
        for i in range(6):  # csak i=5-ig
            for j in range(8):
                # 3 egymas alatt lévő mező szabad e
                if B[i][j] == 0 and B[i + 1][j] == 0 and B[i + 2][j] == 0:
                    uj_B_list = [row.copy() for row in B_list]
                    uj_B_list[i][j] = uj_B_list[i + 1][j] = uj_B_list[i + 2][j] = 1 # lerakás
                    uj_B = tuple(tuple(row) for row in uj_B_list)
                    uj_d = d + 1
                    gyerekek.append((f"lerak_fuggoleges({i + 1}, {j + 1})", (uj_B, uj_d)))

        return gyerekek


if __name__ == "__main__":
    problem = Sakktabla_domino()
    csúcs = mélységi_fakereső(problem)

    út = csúcs.út(); út.reverse()
    print(csúcs.megoldás())

    final_state = csúcs.állapot
    B, d = final_state
    for row in B:
        print(row)
    print(f"Osszesen lerakott domino: {d}")

    for i in range(8):
        for j in range(8):
            if B[i][j] == 0:
                print(f"Az ures mezo: ({i + 1}, {j + 1})")