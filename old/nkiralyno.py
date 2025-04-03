from keres import Feladat


class nyolckiralyno_problema (Feladat):
    def __init__(self, k ,c):
        self.kezdő = k
        self.cél = c
        self.N = len(k)-1

    def célteszt(self, a):
        return a[self.N] == self.cel

    def rákövetkező(self, a):
        gyerekek = []
        s = a[-1]

        for j in range(0,self.N):
            alkalmazhato = False
            for i in range(0,s):
                if a[i] != j and abs(i-s) != abs(a[i]-j):
                    pass
                else:
                    alkalmazhato = False
                    break

        if alkalmazhato:
            tmp = list(a)
            tmp[s] = j
            tmp[-1] = s + 1
            uj_allapot = tuple(tmp)
            gyerekek.append((s+"->"+j, uj_allapot))

        return gyerekek

if __name__ == "__main__":
    kir = nyolckiralyno_problema((0,0,0,0,0,0,0,0,1),9)
