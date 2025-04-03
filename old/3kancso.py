from keres import Feladat, szélességi_fakereső, mélységi_fakereső


class kancso_problema (Feladat):
    # nem a kansot modellezem hanem a problemat
    def __init__(self, ke, c):
        self.kezdő = ke
        self.cél = c
        self.MAX1 = 3
        self.MAX2 = 5
        self.MAX3 = 8

    def célteszt(self, a): # a -> állapot
        return a[0] == self.cél or a[1] == self.cél or a[2] == self.cél

    def rákövetkező(self, a):
        a1,a2,a3 = a
        gyerekek = []

        if a1 != 0 and a2 != self.MAX2:
            T = min(a1,self.MAX2-a2)
            uj_allapot = (a1-T, a2+T, a3)
            gyerekek.append(("1-ből 2-be", uj_allapot))

        if a1 != 0 and a3 != self.MAX3:
            T = min(a1,self.MAX3-a3)
            uj_allapot = (a1-T, a2, a3+T)
            gyerekek.append(("1-ből 3-ba", uj_allapot))

        if a2 != 0 and a1 != self.MAX1:
            T = min(a2,self.MAX1-a1)
            uj_allapot = (a1+T, a2-T, a3)
            gyerekek.append(("2-ből 1-be", uj_allapot))

            ## hfbefejezni

        if a2 != 0 and a3 != self.MAX3:
            T = min(a2,self.MAX3-a3)
            uj_allapot = (a1, a2-T, a3+T)
            gyerekek.append(("2-ből 3-be", uj_allapot))

        if a3 != 0 and a1 != self.MAX1:
            T = min(a3,self.MAX1-a1)
            uj_allapot = (a1+T, a2, a3-T)
            gyerekek.append(("3-ból 1-be", uj_allapot))

        if a3 != 0 and a2 != self.MAX2:
            T = min(a3,self.MAX2-a2)
            uj_allapot = (a1, a2+T, a3-T)
            gyerekek.append(("3-ból 2-be", uj_allapot))

        return gyerekek

    def rakovetkezo_for(self, a):
        a1, a2, a3 = a
        gyerekek = []
        korsok = [a1, a2, a3]
        max_korsok = [self.MAX1, self.MAX2, self.MAX3]

        for i in range(3):
            for j in range(3):
                if i != j and korsok[i] != 0 and korsok[j] != max_korsok[j]:
                    T = min(korsok[i], max_korsok[j] - korsok[j])
                    uj_allapot = list(korsok)
                    uj_allapot[i] -= T
                    uj_allapot[j] += T
                    gyerekek.append((f"{i + 1}-ből {j + 1}-be", tuple(uj_allapot)))
        return gyerekek

if __name__ == "__main__":
    kancso = kancso_problema((0, 0, 8), 4)

    # current_state = (2, 5, 1)
    # print(current_state)
    #
    # next_states = kancso.rakovetkezo_for(current_state)
    # for action, state in next_states:
    #     print(action,state)

    # 3/26
    # csúcs = szélességi_fakereső(kancso)
    csúcs = mélységi_fakereső(kancso)
    út = csúcs.út()
    út.reverse()
    print(út)
    print(csúcs.megoldás())