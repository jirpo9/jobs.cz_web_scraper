class Kniha:
    def __init__(self, nazev, autor, rok_vydani):
        self.nazev = nazev
        self.autor = autor
        self.rok_vydani = rok_vydani

    def __str__(self):
        return f"{self.nazev}, {self.autor}, {self.rok_vydani}"
    
class Knihovna:

    def __init__(self):
        self.knihy = []


    def pridej_knihu(self, kniha):
        self.knihy.append(kniha)
                
    def vypis_knihy(self):
        for kniha in self.knihy:
            print(f"{kniha.nazev}, {kniha.autor}, {kniha.rok_vydani}")
                
    def vyhledej_knihu(self, nazev):
        if not self.knihy:
            print("Knihovna je prázdná.")
            return
        for kniha in self.knihy:
            if kniha.nazev == nazev:
                print(f"Našli jsme: {kniha.nazev}, {kniha.autor}, {kniha.rok_vydani}") 
                return
        print("Kniha nenalezena.")
                                             

babicka = Kniha("Babička", "Božena Němcová", "1855")
kytice = Kniha("Kytice", "Karel Jaromír Erben", "1853")
dasenka = Kniha("Dášeňka čili život štěněte", "Karel Čapek", "1933")

Knihovna_ = Knihovna()
Knihovna_.pridej_knihu(babicka)
Knihovna_.pridej_knihu(kytice)
Knihovna_.pridej_knihu(dasenka)

Knihovna_.vypis_knihy()
Knihovna_.vyhledej_knihu("Dášeňka čili život štěněte")