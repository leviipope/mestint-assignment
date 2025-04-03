def leap_year(ev):
    if ev % 4 == 0 and ev % 100 !=0 or ev % 400 == 0:
        return True
    else:
        return False

def leap_year_between(ev1, ev2):
    my_list = []
    for i in range(ev1, ev2+1):
        if leap_year(i):
            my_list.append(i)
    return my_list

def leap_year_between2(ev1, ev2):
    return [i for i in range(ev1, ev2+1) if leap_year(i)]

def even_or_odd():
    while True:
        x = int(input("Kérem a következő"))
        if x == 0:
            break
        print("Paros" if x % 2 == 0 else "Paratlan")

class Hallgato:
    def __init__(self,n,nk):
        self.nev = n
        self.neptun_kod = nk
        self.jegyek = []

    def add_jegy(self, jegy):
        if 1<= jegy <= 5:
            self.jegyek.append(jegy)
        else:
            print("ervenytelen jegy")

    @property
    def atlag(self):
        return sum(self.jegyek)/len(self.jegyek) if self.jegyek else 0

    def __str__(self):
        return f"{self.nev} ({self.atlag})"

if __name__=="__main__":
    #print(f"Szökő év-e: {leap_year(2024)}")
    #print(f"szoko evek {leap_year_between(1888,1912)}")
    #even_or_odd()
    h = Hallgato("Deb Ella", "RT45WE")
    h.add_jegy(2)
    h.add_jegy(1)
    h.add_jegy(1)
    print(h)