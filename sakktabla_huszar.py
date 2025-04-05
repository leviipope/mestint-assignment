from keres import *


class Sakktábla_Huszár(Feladat):
    def __init__(self):
        M = [[0 for i in range(8)] for i in range(8)]

        # sarkok eltavolitasa
        M[0][0] = 1  # (1,1) sarok
        M[0][7] = 1  # (1,8) sarok
        M[7][0] = 1  # (8,1) sarok
        M[7][7] = 1  # (8,8) sarok

        # a kiindulo pozicio mar lefedve
        M[0][1] = 1

        M = tuple(tuple(row) for row in M)

        self.kezdő = (M, 1, (0, 1))

    def célteszt(self, állapot):
        _, p, pos = állapot
        i, j = pos

        if p == 60:
            # kezdopozicio elerheto e
            return (abs(0 - i) == 2 and abs(1-j) == 1) or (abs(0 - i) == 1 and abs(1 - j) == 2)
        return False

    def rákövetkező(self, állapot):
        M, p, pos = állapot
        i, j = pos

        gyerekek = []

        lepesek = [(2, 1), (1,2), (-1, 2), (-2, 1), (-2, -1),(-1, -2), (1, -2), (2, -1)]

        for lepesek_i, lepesek_j in lepesek:
            i_uj, j_uj = i + lepesek_i, j + lepesek_j

            # benne van e a sakktablaba
            if not (0 <= i_uj < 8 and 0 <= j_uj <8):
                continue

            # ha sarok, akkor skip
            sarkok = [(0, 0), (0,7), (7, 0), (7, 7)]
            if (i_uj, j_uj) in sarkok:
                continue

            if M[i_uj][j_uj] == 0: # ha nem volt meg rajta
                M_uj = [list(row) for row in M]
                M_uj[i_uj][j_uj] = 1
                M_uj = tuple(tuple(row) for row in M_uj)

                uj_allapot = (M_uj, p + 1, (i_uj, j_uj))
                gyerekek.append((f"({i +1},{j + 1}) -> ({i_uj+1},{j_uj + 1})",uj_allapot))

        return gyerekek

if __name__ == "__main__":
    h = Sakktábla_Huszár()
    csúcs = mélységi_gráfkereső(h)

    #út = csúcs.út(); út.reverse()
    #print(út)
    print(csúcs.megoldás())
    final_state = csúcs.állapot
    _, p, _ = final_state
    print(f"lefedett mezok szama: {p}")
