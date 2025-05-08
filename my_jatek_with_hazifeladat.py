from ast import literal_eval as make_tuple
import random


# KIEGESZITO FUGGVENYEK/OSZTALYOK
def update(x, **entries):
    """Asszociatív tömb, struct értékeinek frissítése."""
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


def cmp(a, b):
    return (a > b) - (a < b)


def if_(test, result, alternative):
    """Háromágú értékadás."""
    if test:
        if callable(result):
            return result()
        return result
    else:
        if callable(alternative):
            return alternative()
        return alternative


class Struct:
    """Pehelykönnyű osztály, metódusok nélkül."""

    def __init__(self, **entries):
        """Megadott attribútumok rögzítese."""
        self.__dict__.update(entries)

    def __repr__(self):
        """Megjeleníti a struktúrát."""
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)


def jatssz(jatek, *jatekosok):
    """n személyes, felváltva lépő játékmenet."""
    allapot = jatek.kezdo
    jatek.kiir(allapot)
    while True:
        for jatekos in jatekosok:
            lepes = jatekos(jatek, allapot)
            allapot = jatek.lep(lepes, allapot)
            jatek.kiir(allapot)
            if jatek.levele(allapot):
                return jatek.hasznossag(allapot, jatekosok[0])


def num_or_str(x):
    """Lehetőség szerint számmá alakít."""
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return str(x).strip()


# KERESESEK
# Minimax keresés
def minimax(allapot, jatek):
    """Legjobb lépés meghatározása teljes kereséssel."""
    jatekos = jatek.kovetkezik(allapot)

    # definiáljuk a keresési fa egyes szintjein használatos címkézést.
    def max_ertek(allapot):
        if jatek.levele(allapot):
            return jatek.hasznossag(allapot, jatekos)
        return max([min_ertek(s) for (_, s) in jatek.rakovetkezo(allapot)])

    def min_ertek(allapot):
        if jatek.levele(allapot):
            return jatek.hasznossag(allapot, jatekos)
        return min([max_ertek(s) for (_, s) in jatek.rakovetkezo(allapot)])

    # minimax lényege
    fiai_ertekei = [(a, min_ertek(s)) for (a, s) in jatek.rakovetkezo(allapot)]
    lepes, ertek = max(fiai_ertekei, key=lambda a_s: a_s[1])
    return lepes


def alfabeta_kereses(allapot, jatek, d=4, levagas_teszt=None, kiertekel=None):
    """A játékfa keresése adott mélységig."""
    jatekos = jatek.kovetkezik(allapot)

    def max_ertek(allapot, alfa, beta, melyseg):
        if levagas_teszt(allapot, melyseg):
            return kiertekel(allapot)
        v = float("-inf")
        for (a, s) in jatek.rakovetkezo(allapot):
            v = max(v, min_ertek(s, alfa, beta, melyseg+1))
            if v >= beta:
                return v
            alfa = max(alfa, v)
        return v

    def min_ertek(allapot, alfa, beta, melyseg):
        if levagas_teszt(allapot, melyseg):
            return kiertekel(allapot)
        v = float("inf")
        for (a, s) in jatek.rakovetkezo(allapot):
            v = min(v, max_ertek(s, alfa, beta, melyseg+1))
            if v <= alfa:
                return v
            beta = min(beta, v)
        return v

    # Alfabéta keresés
    levagas_teszt = levagas_teszt or \
        (lambda allapot, melyseg: melyseg > d or jatek.levele(allapot))
    kiertekel = kiertekel or \
        (lambda allapot: jatek.hasznossag(allapot, jatekos))
    alfa = float("-inf")
    legjobb_lepes = None
    for a, s in jatek.rakovetkezo(allapot):
        v = min_ertek(s, alfa, float("inf"), 0)
        if v > alfa:
            alfa = v
            legjobb_lepes = a
    return legjobb_lepes


# JATEKOSOK
# Játékosok típusai
def kerdez_jatekos(jatek, allapot):
    """Felhasználói input."""
    return num_or_str(input('Mit lép? '))


def random_jatekos(jatek, allapot):
    """Véletlen választ a lehetőségek közül."""
    return random.choice(jatek.legalis_lepesek(allapot))


def alfabeta_jatekos(jatek, allapot):
    """Játékfában keres."""
    return alfabeta_kereses(allapot, jatek)


def minimax_jatekos(jatek, allapot):
    """Játékfában keres."""
    return minimax(allapot, jatek)


# JATEK ALAPOSZTALY
class Jatek:
    """Absztrakt osztály a játékok megadására."""

    def legalis_lepesek(self, allapot):
        """Adott állapotban megtehető lépések listája."""
        raise NotImplementedError()

    def lep(self, lepes, allapot):  # NOQA
        """Aktuális állapotban megtett lépés eredménye."""
        raise NotImplementedError

    def hasznossag(self, allapot, jatekos):
        """A játékos számára ekkora haszna volt (nyereség/veszteség)."""
        raise NotImplementedError()

    def levele(self, allapot):
        """A játékfa terminális csúcsa az állapot."""
        return not self.legalis_lepesek(allapot)

    def kovetkezik(self, allapot):
        """Soron következő játékos meghatározása."""
        return allapot.kovetkezik

    def kiir(self, allapot):
        """Az állás megmutatása."""
        print(allapot)

    def rakovetkezo(self, allapot):
        """Rákövetkező (lépés, állapot) párok listája."""
        return [(lepes, self.lep(lepes, allapot))
                for lepes in self.legalis_lepesek(allapot)]

    def __repr__(self):
        """Játék nevének kiírása."""
        return '<%s>' % self.__class__.__name__

# TIC-TAC TOE OSZTALY
class TicTacToe(Jatek):
    """Általánosított 3x3-as amőba."""

    def __init__(self, h=3, v=3, k=3):
        """Játék alapstrukturájának kialakítása."""
        update(self, h=h, v=v, k=k)
        lepesek = [(x, y) for x in range(1, h+1) for y in range(1, v+1)]
        self.kezdo = Struct(
            kovetkezik='X', eredmeny=0, tabla={}, lepesek=lepesek)

    def legalis_lepesek(self, allapot):
        """Minden üres mező lehetséges lépést jelent."""
        return allapot.lepesek

    def lep(self, lepes, allapot):
        """Lépés hatása."""
        if type(lepes) is str:
            lepes = make_tuple(lepes)
        if lepes not in allapot.lepesek:
            return allapot  # téves lépés volt
        tabla = allapot.tabla.copy()
        tabla[lepes] = allapot.kovetkezik
        lepesek = list(allapot.lepesek)
        lepesek.remove(lepes)
        return Struct(
            kovetkezik=if_(allapot.kovetkezik == 'X', 'O', 'X'),
            eredmeny=self.ertekel(tabla, lepes, allapot.kovetkezik),
            tabla=tabla, lepesek=lepesek)

    def hasznossag(self, allapot, jatekos):
        """X értékelése: 1, ha nyer; -1, ha veszít, 0 döntetlenért."""
        return if_(jatekos == "X", allapot.eredmeny, -allapot.eredmeny)

    def levele(self, allapot):
        """A nyert állás vagy a tele tábla a játék végét jelenti."""
        return allapot.eredmeny != 0 or len(allapot.lepesek) == 0

    def kiir(self, allapot):
        """Lássuk az aktuális állást."""
        tabla = allapot.tabla
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print(tabla.get((x, y), '.'), end=" ")
            print()
        print(allapot.eredmeny)
        print()

    def ertekel(self, tabla, lepes, jatekos):
        """Ha X nyer ezzel a lépéssel, akkor 1, ha O, akkor -1, különben 0."""
        if (self.k_egy_sorban(tabla, lepes, jatekos, (0, 1)) or
                self.k_egy_sorban(tabla, lepes, jatekos, (1, 0)) or
                self.k_egy_sorban(tabla, lepes, jatekos, (1, -1)) or
                self.k_egy_sorban(tabla, lepes, jatekos, (1, 1))):
            return if_(jatekos == 'X', +1, -1)
        else:
            return 0

    def k_egy_sorban(self, tabla, lepes, jatekos, irany):
        """Igaz, ha van a lépéstől adott irányba k azonos figura."""
        delta_x, delta_y = irany
        x, y = lepes
        n = 0
        while tabla.get((x, y)) == jatekos:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = lepes
        while tabla.get((x, y)) == jatekos:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1   # lépés duplán számolva
        return n >= self.k

# Feladat 2.2
class Kavics(Jatek):
    def __init__(self, kezdeti_X, kezdeti_Y):
        self.kezdo = Struct(X=kezdeti_X, Y=kezdeti_Y, kovetkezik='A')

    def legalis_lepesek(self, allapot):
        lepesek = []
        # A lépés formátuma: (melyik kupac, mennyiség)
        #   A: elvétel az X kupacból
        #   B: elvétel az Y kupacból
        #   AB: elvétel mindkét kupacból
        
        if allapot.X > 0:
            for i in range(1, allapot.X + 1):
                lepesek.append(('A', i))
        
        if allapot.Y > 0:
            for i in range(1, allapot.Y + 1):
                lepesek.append(('B', i))
        
        if allapot.X > 0 and allapot.Y > 0:
            for i in range(1, min(allapot.X, allapot.Y) + 1):
                lepesek.append(('AB', i))

        return lepesek

    def lep(self, lepes, allapot):
        uj_X, uj_Y = allapot.X, allapot.Y
        tipus, mennyiseg = lepes # ('A', 3)

        if tipus == 'A':
            uj_X -= mennyiseg
        elif tipus == 'B':
            uj_Y -= mennyiseg
        elif tipus == 'AB':
            uj_X -= mennyiseg
            uj_Y -= mennyiseg

        if allapot.kovetkezik == 'A':
            kovetkezo_jatekos = 'B'
        else:
            kovetkezo_jatekos = 'A'
        
        return Struct(X=uj_X, Y=uj_Y, kovetkezik=kovetkezo_jatekos)

    def hasznossag(self, allapot, jatekos_mark):
        gyoztes = 'B' if allapot.kovetkezik == 'A' else 'A'

        if jatekos_mark == gyoztes:
            return 1
        else:
            return -1

    def kiir(self, allapot):
        print(f"X kupac: {allapot.X}, Y kupac: {allapot.Y}, Következő lép: {allapot.kovetkezik}")
        if self.levele(allapot):
            if allapot.kovetkezik == 'A':
                gyoztes = 'B'
            else:
                gyoztes = 'A'
            print(f"Játék vége! Győztes: {gyoztes}")
        print("*" * 30)

# Feladat 2.3
class Lovas(Jatek):
    def __init__(self, sotet_kezdo_poz=(0,0), vilagos_kezdo_poz=(7,7)):
        self.meret = 8
        self.kezdo_sotet = sotet_kezdo_poz
        self.kezdo_vilagos = vilagos_kezdo_poz
        
        if not (self._ervenyes_mezo(sotet_kezdo_poz) and self._ervenyes_mezo(vilagos_kezdo_poz)):
            raise ValueError("A kezdőpozícióknak a táblán kell lenniük.")
        if sotet_kezdo_poz == vilagos_kezdo_poz:
            raise ValueError("A két huszár nem indulhat ugyanarról a mezőről.")

        self.kezdo = Struct(
            sotet_poz=sotet_kezdo_poz,
            vilagos_poz=vilagos_kezdo_poz,
            kovetkezik='S',
            latogatott_mezok=set([sotet_kezdo_poz, vilagos_kezdo_poz])
        )
        self.knight_moves = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1)
        ]

    def _ervenyes_mezo(self, poz):
        x, y = poz
        return 0 <= x < self.meret and 0 <= y < self.meret

    def legalis_lepesek(self, allapot):
        lepesek = []
        aktualis_jatekos = allapot.kovetkezik
        
        if aktualis_jatekos == 'S':
            aktualis_poz = allapot.sotet_poz
        else:
            aktualis_poz = allapot.vilagos_poz
        
        x, y = aktualis_poz
        for dx, dy in self.knight_moves:
            uj_x, uj_y = x + dx, y + dy
            uj_poz = (uj_x, uj_y)
            if self._ervenyes_mezo(uj_poz) and uj_poz not in allapot.latogatott_mezok:
                lepesek.append(uj_poz)
        return lepesek

    def lep(self, lepes, allapot):
        if lepes not in self.legalis_lepesek(allapot):
            return allapot 

        uj_latogatott_mezok = set(allapot.latogatott_mezok)
        uj_latogatott_mezok.add(lepes)

        if allapot.kovetkezik == 'S':
            return Struct(
                sotet_poz=lepes,
                vilagos_poz=allapot.vilagos_poz,
                kovetkezik='V',
                latogatott_mezok=uj_latogatott_mezok
            )
        else:
            return Struct(
                sotet_poz=allapot.sotet_poz,
                vilagos_poz=lepes,
                kovetkezik='S',
                latogatott_mezok=uj_latogatott_mezok
            )

    def hasznossag(self, allapot, jatekos_mark):
        if self.levele(allapot): 
            if allapot.kovetkezik == 'S':
                gyoztes = 'V'
            else:
                gyoztes = 'S'
            
            if jatekos_mark == gyoztes:
                return 1
            else:
                return -1
        return 0

    def kiir(self, allapot):
        print(f"Következő lép: {'Sötét (S)' if allapot.kovetkezik == 'S' else 'Világos (V)'}")
        print(f"Sötét pozíció: {allapot.sotet_poz}, Világos pozíció: {allapot.vilagos_poz}")
        
        tabla_kep = [["." for _ in range(self.meret)] for _ in range(self.meret)]
        
        for r, c in allapot.latogatott_mezok:
            if (r,c) != allapot.sotet_poz and (r,c) != allapot.vilagos_poz :
                 tabla_kep[r][c] = "x"

        sr, sc = allapot.sotet_poz
        tabla_kep[sr][sc] = "S"
        
        vr, vc = allapot.vilagos_poz
        tabla_kep[vr][vc] = "V"

        print("  " + " ".join(map(str, range(self.meret))))
        for i, sor in enumerate(tabla_kep):
            print(f"{i} " + " ".join(sor))
        
        if self.levele(allapot):
            gyoztes_jatekos = 'Világos (V)' if allapot.kovetkezik == 'S' else 'Sötét (S)'
            print(f"Játék vége! Nincs több legális lépés {allapot.kovetkezik} számára.")
            print(f"Győztes: {gyoztes_jatekos}")
        print("-" * 30)

class BalKiralyno(Jatek):
    """
    A "Bal Királynő" játék.
    Egy N × N mezőből álló táblán játszák. A királynő a (1,N) pozícióból indul
    (1-indexelt, sor=1, oszlop=N, azaz a jobb felső sarok).
    A játékosok felváltva lépnek. Minden lépésben el kell mozdítani a királynőt
    legalább egy mezővel. A figura csak balra, lefelé vagy balra lefelé átlósan léphet.
    Az a játékos nyer, aki a királynővel a tábla bal alsó sarkában lévő (N,1) mezőre lép.

    Megjegyzés: N=1 esetén a játék a kezdőállapotban véget ér (döntetlen).
    Egyes ágensek (pl. minimax_jatekos, random_jatekos) hibát jelezhetnek,
    ha terminális kezdőállapottal hívják meg őket. Javasolt N >= 2 használata.
    """

    def __init__(self, N=8):
        """
        Játék inicializálása N x N méretű táblával.
        Args:
            N (int): A tábla mérete. Alapértelmezett: 8.
                     N >= 1 kell legyen.
        """
        if not isinstance(N, int) or N < 1:
            raise ValueError("A tábla méretének (N) pozitív egész számnak kell lennie.")

        self.N = N
        self.cel_pozicio = (N, 1)  # Bal alsó sarok (sor, oszlop)
        self.start_pozicio = (1, N) # Jobb felső sarok (sor, oszlop)

        self.kezdo = Struct(kovetkezik='X',
                              pozicio=self.start_pozicio,
                              N=self.N,
                              cel=self.cel_pozicio,
                              eredmeny=0)  # eredmeny: 1 ha X nyert, -1 ha O nyert, 0 különben

    def legalis_lepesek(self, allapot):
        """Adott állapotban megtehető lépések listája."""
        lepesek = []
        r, c = allapot.pozicio
        N = allapot.N

        # Ha a királynő már a célpozícióban van, nincs több legális lépés.
        if allapot.pozicio == allapot.cel:
            return []

        # Balra történő lépések (sor azonos, oszlop csökken)
        # Legalább egy mezővel kell elmozdulni.
        for i in range(1, c):  # Az új oszlop c-1, c-2, ..., 1 lehet
            lepesek.append((r, c - i))

        # Lefelé történő lépések (oszlop azonos, sor növekszik)
        # Legalább egy mezővel kell elmozdulni.
        for i in range(1, N - r + 1):  # Az új sor r+1, r+2, ..., N lehet
            lepesek.append((r + i, c))

        # Balra lefelé átlósan történő lépések (sor növekszik, oszlop csökken)
        # Legalább egy mezővel kell elmozdulni (k az elmozdulás mértéke).
        max_atlos_lepes = min(N - r, c - 1) # Max elmozdulás átlósan
        for k in range(1, max_atlos_lepes + 1):
            lepesek.append((r + k, c - k))
        
        return lepesek

    def lep(self, lepes, allapot):
        """Aktuális állapotban megtett lépés eredménye."""
        # A 'lepes' itt az új pozíció (uj_sor, uj_oszlop)
        # A keretrendszer biztosítja, hogy 'lepes' egyike a 'legalis_lepesek' által visszaadottaknak.

        jatekos_aki_lepett = allapot.kovetkezik
        uj_pozicio = lepes
        uj_eredmeny = allapot.eredmeny # Alapértelmezetten marad a régi

        if uj_pozicio == allapot.cel:
            # Az a játékos nyer, aki a célmezőre lép.
            # Ha X lépett a célba, X nyer (eredmény = 1).
            # Ha O lépett a célba, O nyer (eredmény = -1).
            uj_eredmeny = if_(jatekos_aki_lepett == 'X', 1, -1)

        kovetkezo_jatekos = if_(jatekos_aki_lepett == 'X', 'O', 'X')

        return Struct(kovetkezik=kovetkezo_jatekos,
                      pozicio=uj_pozicio,
                      N=allapot.N,
                      cel=allapot.cel,
                      eredmeny=uj_eredmeny)

    def hasznossag(self, allapot, jatekos):
        """A játékos számára ekkora haszna volt (nyereség/veszteség)."""
        # allapot.eredmeny: 1, ha X nyert; -1, ha O nyert; 0, ha döntetlen vagy folyamatban.
        # Ha a 'jatekos' X: hasznosság = allapot.eredmeny
        # Ha a 'jatekos' O: hasznosság = -allapot.eredmeny
        if allapot.eredmeny == 0: # Játék nem ért véget nyeréssel/veszteséggel, vagy N=1
            return 0
        return if_(jatekos == "X", allapot.eredmeny, -allapot.eredmeny)

    # levele(self, allapot)
    # Az alap Jatek osztály levele metódusa megfelelő: return not self.legalis_lepesek(allapot)
    # Ha a királynő a célban van, legalis_lepesek() üres listát ad, így levele() igaz lesz.

    # kovetkezik(self, allapot)
    # Az alap Jatek osztály kovetkezik metódusa megfelelő (allapot.kovetkezik alapján).

    def kiir(self, allapot):
        """Az állás megmutatása a konzolon."""
        N = allapot.N
        print(f"\nKövetkező játékos: {allapot.kovetkezik}")
        print(f"Királynő pozíciója: {allapot.pozicio}")
        # print(f"Cél pozíció: {allapot.cel}")
        # print(f"Tábla mérete: {N}x{N}")
        print("Tábla:")
        for r_idx in range(1, N + 1):
            sor_str = []
            for c_idx in range(1, N + 1):
                aktualis_cella = (r_idx, c_idx)
                if aktualis_cella == allapot.pozicio:
                    sor_str.append('Q')
                elif aktualis_cella == allapot.cel:
                    sor_str.append('C') # Cél megjelölése
                else:
                    sor_str.append('.')
            print(" ".join(sor_str))
        
        if allapot.eredmeny != 0:
            gyoztes = 'X' if allapot.eredmeny == 1 else 'O'
            print(f"Játék vége! Győztes: {gyoztes}")
        elif not self.legalis_lepesek(allapot) and allapot.pozicio != allapot.cel:
             print("Játék vége! Nincs több legális lépés, de a cél nem elérve (döntetlen).")
        elif not self.legalis_lepesek(allapot) and allapot.pozicio == allapot.cel and allapot.eredmeny == 0:
             # Ez az N=1 eset, ahol a start == cel
             print("Játék vége! A királynő a célpozíción indul (döntetlen).")
        print("-" * (2 * N))

def ttt():
    tto = TicTacToe()

    # Ket random jatekos egymas ellen
    # jatssz(tto, random_jatekos, random_jatekos)

    # X -> minimax_jatekos 0 -> random_jatekos
    jatssz(tto, minimax_jatekos, random_jatekos)

    # X -> random_jatekos 0 -> minimax_jatekos
    # jatssz(tto, random_jatekos, minimax_jatekos)

    # X -> minimax_jatekos 0 -> minimax_jatekos
    # jatssz(tto, minimax_jatekos, minimax_jatekos)

    # X -> random_jatekos 0 -> alfabeta_jatekos
    # jatssz(tto, random_jatekos, alfabeta_jatekos)

    # X -> alfabeta_jatekos 0 -> random_jatekos
    # jatssz(tto, alfabeta_jatekos, random_jatekos)

    # X -> alfabeta_jatekos 0 -> alfabeta_jatekos
    # jatssz(tto, alfabeta_jatekos, alfabeta_jatekos)

def kavics():
    kavics = Kavics(19,21)
    jatssz(kavics, alfabeta_jatekos, random_jatekos)

def lovas():
    lovas = Lovas()
    jatssz(lovas, alfabeta_jatekos, random_jatekos)

def bal_kiralyno():
    bal_kiralyno = BalKiralyno(8)
    jatssz(bal_kiralyno, random_jatekos, random_jatekos)

if __name__ == '__main__':
    # ttt()
    kavics()
    lovas()
    bal_kiralyno()
