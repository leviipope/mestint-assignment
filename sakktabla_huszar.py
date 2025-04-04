from keres import *


class Sakktábla_Huszár(Feladat):
    def __init__(self):
        self.N = 8  # 8x8 sakktábla

        # Initialize the starting matrix
        kezdő_M = [[0 for _ in range(self.N)] for _ in range(self.N)]

        # Mark corners as visited/removed
        kezdő_M[0][0] = 1  # (1,1) sarok
        kezdő_M[0][self.N - 1] = 1  # (1,N) sarok
        kezdő_M[self.N - 1][0] = 1  # (N,1) sarok
        kezdő_M[self.N - 1][self.N - 1] = 1  # (N,N) sarok

        # Mark starting position as visited (első sor, második oszlop)
        kezdő_M[0][1] = 1

        # Convert to tuple of tuples for immutability
        kezdő_M = tuple(tuple(row) for row in kezdő_M)

        # Initial state: (Matrix, move number, knight position)
        self.kezdő = (kezdő_M, 1, (0, 1))

    def célteszt(self, állapot):
        M, p, pozíció = állapot
        i, j = pozíció

        # Check if we've visited all non-corner squares
        if p == self.N * self.N - 4:
            # Check if the starting position (1,2) is reachable with one more knight move
            return self._huszárlépés(i, j, 0, 1)

        return False

    def _huszárlépés(self, i, j, i_új, j_új):
        """Ellenőrzi, hogy a huszár tud-e lépni (i,j)-ből (i_új,j_új)-be"""
        return ((abs(i_új - i) == 2 and abs(j_új - j) == 1) or
                (abs(i_új - i) == 1 and abs(j_új - j) == 2))

    def _érvényes_pozíció(self, i, j):
        """Ellenőrzi, hogy a (i,j) pozíció érvényes-e (a táblán belül és nem sarok)"""
        if not (0 <= i < self.N and 0 <= j < self.N):
            return False

        # Ellenőrzi, hogy nem sarok-e
        sarkok = [(0, 0), (0, self.N - 1), (self.N - 1, 0), (self.N - 1, self.N - 1)]
        if (i, j) in sarkok:
            return False

        return True

    def rákövetkező(self, állapot):
        M, p, pozíció = állapot
        i, j = pozíció

        gyerekek = []

        # Lehetséges huszárlépések
        lépések = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

        for di, dj in lépések:
            i_új, j_új = i + di, j + dj

            # Ellenőrzi, hogy az új pozíció érvényes és még nem látogatott
            if self._érvényes_pozíció(i_új, j_új) and M[i_új][j_új] == 0:
                # Létrehoz egy új mátrixot, ahol az új pozíció meg van jelölve
                M_új = [list(row) for row in M]
                M_új[i_új][j_új] = 1
                M_új = tuple(tuple(row) for row in M_új)

                új_állapot = (M_új, p + 1, (i_új, j_új))
                művelet = f"({i + 1},{j + 1}) -> ({i_új + 1},{j_új + 1})"

                gyerekek.append((művelet, új_állapot))

        return gyerekek


def tábla_kirajzolás(pozíciók=None):
    """
    Kirajzolja a sakktáblát a huszár útvonalával.
    pozíciók: a huszár pozícióinak listája sorrendben.
    """
    N = 8  # 8x8 sakktábla

    # Létrehoz egy reprezentációt az útvonal megjelenítéséhez
    tábla = [[0 for _ in range(N)] for _ in range(N)]

    # Megjelöli a sarkokat (X-szel jelölve)
    sarkok = [(0, 0), (0, N - 1), (N - 1, 0), (N - 1, N - 1)]
    for i, j in sarkok:
        tábla[i][j] = -1

    # Számokkal jelöli a lépéseket
    for lépés, (i, j) in enumerate(pozíciók, 1):
        tábla[i][j] = lépés

    # Kirajzolja a táblát oszlop és sor feliratokkal
    print("  " + " ".join([f"{j + 1:2d}" for j in range(N)]))
    for i in range(N):
        sor = f"{i + 1} "
        for j in range(N):
            if tábla[i][j] == -1:
                sor += " X "  # Sarok
            elif tábla[i][j] == 0:
                sor += " . "  # Nem látogatott mező
            else:
                sor += f"{tábla[i][j]:2d} "  # Lépés száma
        print(sor)


if __name__ == "__main__":
    h = Sakktábla_Huszár()

    print("A huszár útkeresése megkezdődött...")

    # Mélységi gráfkeresést használunk a hatékonyság érdekében
    csúcs = mélységi_gráfkereső(h)

    if csúcs:
        print("Megoldás találva!")

        # Kinyeri a huszár útvonalát a megoldásból
        út = csúcs.út()
        út.reverse()

        # Kigyűjti a huszár pozícióit az útvonal mentén
        pozíciók = []
        for csúcs_az_úton in út:
            _, _, poz = csúcs_az_úton.állapot
            pozíciók.append(poz)

        # Megjeleníti a megoldást
        print("\nA huszár útja:")
        tábla_kirajzolás(pozíciók)

    else:
        print("Nincs megoldás!")
