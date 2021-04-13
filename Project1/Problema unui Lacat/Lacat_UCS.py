

import copy;
import time;

class NodParcurgere:
    def __init__(self,info,key,parinte,cost):
        self.info = info   # Informatia din nod
        self.key = key   # Cheia reprezentand ultima cheie aplicata pe incuietoare (muchia din arborele de parcurgere cu care s-a ajuns in acest nod)
        self.parinte = parinte # Parintele nodului din arborele de parcurgere
        self.g = cost # Costul

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None: # Obtinem drumul pana la nodul nostru, mergand din parinte in parinte
            l.insert(0,nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self,afisLung = False, afisCost = False):

        global sir_afisare
        l = self.obtineDrum()
        i = 1
        for nod in l:
            if nod.key is not None:
                sir_afisare +=  str(i) + ") Incuietori: " + str(nod.parinte) + '\n'
                sir_afisare += "Folosim cheia: " + str(nod.key) + " pentru a ajunge la " + str(nod) + '\n'
                i += 1


        sir_afisare += "Incuietori(stare scop): " + str(nod) + '\n'
        if afisCost:
            sir_afisare += "S-au realizat : " + str( self.g ) + " operatii." + '\n'
        if afisLung:
            sir_afisare += "Lungimea drumului: " + str(len(l)) + '\n'
        return len(l)

    def contineInDrum(self, infoNodNou):
        """Verificam daca nodul pe care vrem sa il adaugam in arbore se gaseste pe drumul pana la nodul curent.
           Folosim aceasta functie ca sa ne asiguram ca nu se creeaza cicluri"""
        nodDrum = self
        while nodDrum is not None:  # Reconstruim drumul mergand din parinte in parinte
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte
        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        """Ne ajuta sa afisam nodul nostru in formatul pe care ni-l cere problema (si pentru a fi mai usor de inteles)"""
        sir = "[ "
        incuietori = self.info
        for i in range (len(incuietori)-1):
            sir += "inc(" + str(incuietori[i][0]) + "," + str(incuietori[i][1]) + "), "

        sir += "(" + str(incuietori[len(incuietori)-1][0]) + ","+  str(incuietori[len(incuietori)-1][1]) + ") ]"
        return sir


class Graph: # graful problemei

    def __init__(self, nume_fisier):
        """Parsam fisierul de input si memoram informatia sub forma de stari in graf"""

        global sir_afisare

        f = open(nume_fisier,"r")
        continut_fisier = f.read()
        self.lista_chei = []
        for linie in continut_fisier.split('\n'):
            cheie = list(linie)
            self.lista_chei.append(cheie)

        sir_afisare += "Lista chei:"+ str( self.lista_chei) +'\n'
        incuietoriStart = []

        nrIncuietori = len(cheie)

        for i in range(nrIncuietori):  # Mereu informatia de start va fi reprezentata de o lista de incuitori, toate inchide o data
            incuietoriStart.append(['i', 1])

        self.start = incuietoriStart

        self.scopuri = []
        incuietoriScop = []

        for i in range(nrIncuietori):  # Mereu starea scop va fi reprezentata de o lista de incuietori, toate deschise
            incuietoriScop.append(['d', 0])

        self.scopuri.append (incuietoriScop)

        NodStart = NodParcurgere(self.start, None, None,  0)  # Pentru nodul Start, cheia va fi None, parintele None si setam costul la 0

        sir_afisare += "Initial: "+ str(NodStart) + '\n'

    def testeaza_scop(self, nodCurent):  # Functia care testeaza daca suntem intr-o starea scop
        return nodCurent.info in self.scopuri

    def genereazaSuccesori(self, nodCurent):  # Functia care genereaza succesori in nodul de parcurgere

        listaSuccesori = []

        for i in range(len(self.lista_chei)):
            incuietoariNoi = copy.deepcopy(nodCurent.info) # Folosim deepcopy ca sa nu afectam informatia nodului curent

            #print("incuietoariNoi: ", incuietoariNoi)
            cheie = copy.deepcopy(self.lista_chei[i])
            #print(cheie)

            for indice in range(len(cheie)):
                #print("cheie[indice]",cheie[indice])
                if cheie[indice] == 'i': # Avem incuietoare de inchidere
                    if incuietoariNoi[indice][0] == 'd': # Daca incuietaorea e deschisa o inchidem
                        incuietoariNoi[indice][0] = 'i'
                    incuietoariNoi[indice][1] += 1 # O mai inchidem o data sau o inchidem pentru prima oara daca era deschisa

                elif cheie[indice] == 'd': # Avem o cheie de deschidere
                   # if incuietoariNoi[indice][0] == 'd': # daca e deja deschisa o lasam asa
                    #    continue
                    if incuietoariNoi[indice][0] == 'i':

                        if incuietoariNoi[indice][1] == 1: # daca e inchisa o singura data, o deschidem
                            incuietoariNoi[indice] = ['d',0]

                        elif incuietoariNoi[indice][1] > 1 : # daca e inchisa de mai multe ori scadem din indicele de inchidere
                            incuietoariNoi[indice][1] -= 1

                elif cheie[indice] == 'g':
                    continue


            if not nodCurent.contineInDrum(incuietoariNoi): # Daca nodul nu a mai fost pe acest drum, il adaugam

                nodNou = NodParcurgere(
                    incuietoariNoi,  # Informatia din nod, retinuta sub forma de lista de incuietori
                    cheie, # Cheia (muchia) cu care am ajuns in aceasta stare
                    nodCurent,  # parinte
                    nodCurent.g + 1  # Am mai facut o mutare, deci costului i se va adauga 1

                )
                # print(nodCurent.info)
                # print(cheie)
                # print("incuietoriNoi dupa aplicarea cheii: ", incuietoariNoi)
                listaSuccesori.append(nodNou)


        return listaSuccesori


def uniform_cost(gr, nrSolutiiCautate ):

    global sir_afisare
    # In coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None,None,0)]  # Initial avem nodul de START
    #print("c", c)

    while len(c) > 0:  # Cat timp coada nu e vida
        nodCurent = c.pop(0)  # Luam primul element si il eliminam din coada

        if gr.testeaza_scop(nodCurent): # Daca am ajuns intr-un nod de scop inseamna ca avem solutie
            sir_afisare += "Solutie: \n"
            nodCurent.afisDrum(afisLung=True, afisCost=True)
            sir_afisare += "\n------------------------------------------------\n"

            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return

        lSuccesori = gr.genereazaSuccesori(nodCurent)  # Generam succesorii din arborele de parcurhere

        for s in lSuccesori:
            i = 0
            while i < len(c): # Ii caul locul nodului in coada astfel incat sa ramana ordonate dupa cost
                if c[i].g > s.g:
                    break
                i += 1
            c.insert(i,s)

        myTime = time.time() - start;
        if myTime > 5:
            print("Time is out!")
            sir_afisare += "Time is out!"
            break






sir_afisare = ""
nume_fisier_intrare = input("Numele fisierului de intrare: ")
Timeout = int(input("Introduceti timeout-ul la care doriti sa se opreasca algoritmul: "))
nrSolutiiCautate = int(input("Numarul de solutii cautate: "))

gr = Graph(nume_fisier_intrare)

start = time.time()




uniform_cost(gr,nrSolutiiCautate)
nume_fisier_iesire = "output_ucs.txt"
g = open(nume_fisier_iesire,"w")
g.write(sir_afisare)






