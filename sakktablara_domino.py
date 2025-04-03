from keres import *

class Sakktabla_domino(Feladat):
    def __init__(self, ke=None, c=None):
        """Initialize the problem with an empty chessboard."""
        # If no start state is provided, create a default one
        if ke is None:
            tabla = tuple(tuple(0 for _ in range(8)) for _ in range(8))
            self.kezdő = (tabla, 0)
        else:
            self.kezdő = ke

        self.cél = c

    def célteszt(self, allapot):
        """Check if the state is a goal state."""
        B, d = allapot

        # Check if 21 dominoes are placed (covering 63 squares)
        return d == 21 and sum(sum(row) for row in B) == 63

    def rákövetkező(self, allapot):
        """Generate successor states."""
        B, d = allapot
        gyerekek = []

        # If we've already placed 21 dominoes, no more moves
        if d >= 21:
            return gyerekek

        # Convert tuple of tuples to list of lists for modification
        B_list = [list(row) for row in B]

        # Try placing horizontal dominoes
        for i in range(8):
            for j in range(6):  # Only up to j=5 since a 3x1 domino needs 3 squares
                # Check if the three consecutive squares are free
                if B[i][j] == 0 and B[i][j + 1] == 0 and B[i][j + 2] == 0:
                    # Create a new state with the domino placed
                    uj_B_list = [row.copy() for row in B_list]
                    uj_B_list[i][j] = uj_B_list[i][j + 1] = uj_B_list[i][j + 2] = 1
                    uj_B = tuple(tuple(row) for row in uj_B_list)
                    uj_d = d + 1
                    gyerekek.append((f"lerak_vizszintes({i + 1}, {j + 1})", (uj_B, uj_d)))

        # Try placing vertical dominoes
        for i in range(6):  # Only up to i=5 since a 3x1 domino needs 3 squares
            for j in range(8):
                # Check if the three consecutive squares are free
                if B[i][j] == 0 and B[i + 1][j] == 0 and B[i + 2][j] == 0:
                    # Create a new state with the domino placed
                    uj_B_list = [row.copy() for row in B_list]
                    uj_B_list[i][j] = uj_B_list[i + 1][j] = uj_B_list[i + 2][j] = 1
                    uj_B = tuple(tuple(row) for row in uj_B_list)
                    uj_d = d + 1
                    gyerekek.append((f"lerak_fuggoleges({i + 1}, {j + 1})", (uj_B, uj_d)))

        return gyerekek


if __name__ == "__main__":
    # Create the problem instance
    problem = Sakktabla_domino()
    csúcs = mélységi_fakereső(problem)

    út = csúcs.út()
    út.reverse()
    print(csúcs.megoldás())

    final_state = csúcs.állapot
    B, d = final_state
    print("\nFinal board state (1 = covered, 0 = free):")
    for row in B:
        print(row)
    print(f"Number of dominoes placed: {d}")

    for i in range(8):
        for j in range(8):
            if B[i][j] == 0:
                print(f"Az ures mezo: ({i + 1}, {j + 1})")