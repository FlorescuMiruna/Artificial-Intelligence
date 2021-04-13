import copy
import time
"""Am modelat problema sub forma de graf astfel:

Nodurile reprezinta starile incuietorilor.
Nodul de start este de fiecare data de forma [inc(i,1), inc(i,1), inc(i,1)] ,difera doar lungimea listei, in functie de input,
adica de lungimea listei de chei, starea de start reprezinta faptul ca toate incuietorile sunt inchise o singura data.

Avem un singur nod scop, de fiecare data este de forma: [inc(d,0), inc(d,0), inc(d,0)], reprezentand faptul ca toate incuietorile sunt deschise

Muchiile reprezinta trecerea dintr-o stare a incuietorii in alta prin aplicarea unei chei din lista de chei.
 
Costul este de fiecare data 1, acesta reprezentand faptul ca am aplicat o data cheia si am trecut intr-o alta stare a lacatului.
"""
class NodParcurgere:

    def __init__(self, info, key,parinte, cost = 0, h = 0):
        self.info = info # Informatia din nod
        self.key = key  # Cheia cu care incuietoarea a ajuns in aceasta stare (muchia din graful de parcurgere)
        self.parinte = parinte # Parintele nodului din arborele de parcurgere
        self.g = cost # Costul
        self.h = h # Euristica
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:# Obtinem drumul pana la nodul nostru, mergand din parinte in parinte
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
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
        while nodDrum is not None:
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

        sir += "(" + str(incuietori[len(incuietori)-1][0]) + ","+  str(incuietori[len(incuietori)-1][1]) + ")]"

        #sir += str(self.info)
        return sir

class Graph: # graful problemei



    def __init__(self, nume_fisier_intrare):

        """Parsam fisierul de input si memoram informatia sub forma de stari in graf"""

        global sir_afisare
        f = open(nume_fisier_intrare,"r")

        continut_fisier = f.read()
        self.lista_chei = []
        for linie in continut_fisier.split('\n'):
            cheie = list(linie)
            self.lista_chei.append(cheie)

        sir_afisare += "Lista chei:" + str(self.lista_chei) + '\n'
        incuietoriStart = []

        nrIncuietori = len(cheie)

        for i in range(nrIncuietori):
            incuietoriStart.append(['i', 1])

        self.start = incuietoriStart
        self.scopuri = []

        incuietoriScop = []
        for i in range(nrIncuietori):  # Mereu starea scop va fi reprezentata de o lista de incuietori, toate deschise
            incuietoriScop.append(['d', 0])

        self.scopuri.append (incuietoriScop)

        NodStart = NodParcurgere(self.start, None, None, 0, 0) # Mereu starea scop va fi reprezentata de o lista de incuietori, toate deschise
        sir_afisare += "Initial: " + str(NodStart) +'\n'
      #  print("Stari finale: ", str(self.scopuri))

    def testeaza_scop(self, nodCurent): # Functia care testeaza daca suntem intr-o starea scop
        return nodCurent.info in self.scopuri

    def genereazaSuccesori(self, nodCurent,tip_euristica): # Functia care genereaza succesori in nodul de parcurgere
        listaSuccesori = []


        for i in range(len(self.lista_chei)): # Folosim deepcopy ca sa nu afectam informatia nodului curent

            incuietoariNoi = copy.deepcopy(nodCurent.info)
            #print("incuietoariNoi: ", incuietoariNoi)
            cheie = copy.deepcopy(self.lista_chei[i])
            #print(cheie)

            for indice in range(len(cheie)):
                #print("cheie[indice]",cheie[indice])
                if cheie[indice] == 'i': # Avem cheie de inchidere
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


            if not nodCurent.contineInDrum(incuietoariNoi):

                nodNou = NodParcurgere(
                    incuietoariNoi,# Informatia din nod, retinuta sub forma de lista de incuietori
                    cheie,# Cheia (muchia) cu care am ajuns in aceasta stare
                    nodCurent, # parinte
                    nodCurent.g + 1, # Am mai facut o mutare, deci costului i se va adauga 1
                    h=self.calculeaza_h(incuietoariNoi, tip_euristica)
                )
                # print(nodCurent.info)
                # print(cheie)
                # print("incuietoriNoi dupa aplicarea cheii: ", incuietoariNoi)
                listaSuccesori.append(nodNou)


        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica):
        if tip_euristica == "euristica_banala":
            return self.euristica_banala(infoNod, tip_euristica)
        elif tip_euristica == "euristica_admisibila_1":
            return self.euristica_admisibila_1(infoNod, tip_euristica)
        elif tip_euristica == "euristica_admisibila_2":
            return self.euristica_admisibila_2(infoNod, tip_euristica)
        else:
            raise Exception("Aceasta euristica nu este definita")

    def euristica_banala(self, infoNod, tip_euristica):
        return 0 if infoNod in self.scopuri else 1

    def euristica_admisibila_1(self, infoNod, tip_euristica):
        """ Pentru fiecare nod, numar indicele maxim de inchidere, daca de exemplu avem o incuietoare cu (i,4), stim ca va trebui sa o deschidem de 4 ori pentru a ajunge
        sa fie deschisa, adica (d,0), deci cu siguranta va trebui sa mai facem cel putin 4 pasi pana sa ajungem intr-o stare finala. Euristica este admisibila pentru ca
        de fiecare data este mai mica decat distanta reala pana la starea-scop."""
        maximInchis = 0
        for incuietoare in infoNod:
            if incuietoare[0] == 'i':
                if incuietoare[1] > maximInchis:
                    maximInchis = incuietoare[1]

        return maximInchis

def a_star(gr, tip_euristica):
    c = [NodParcurgere(gr.start, None,None, 0, gr.calculeaza_h(gr.start, tip_euristica))] # Initial in coada OPEN punem nodul de start
    closed = [] # Coada CLOSED e inital goala

    while len(c) > 0:  # Cat timp coada OPEN nu e vida
        nodCurent = c.pop(0)  # Iau elementul din varful cozii si il elimin din coada
        closed.append(nodCurent)  # Mut nodul in coada CLOSED

        if gr.testeaza_scop(nodCurent):# Daca am ajuns intr-un nod scop (in cazul nostru nodul scop e unic), situatia in care toate lacatele sunt deschise

            global sir_afisare
            sir_afisare += "Solutie:\n "
            nodCurent.afisDrum(afisLung=True, afisCost=True)
            end = time.time()
            sir_afisare += "Runtime of the program is: " + str(end - start) + "\n"
            sir_afisare += "--------------------------------------------------\n"

            return

        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)  # Generam succesorii din arborele de parcurhere
        lSuccesoriCopy = lSuccesori.copy()
        for s in lSuccesoriCopy:
            gasitOpen = False
            for elem in c:     # Cautam nodul in coada OPEN
                if s.info == elem.info:
                    gasitOpen = True
                    if s.f < elem.f:
                        c.remove(elem)
                    else:
                        lSuccesori.remove(s)
                    break
            if not gasitOpen:  # Daca nu l-am gasit in coada OPEN il cautam in coada CLOSED
                for elem in closed:
                    if s.info == elem.info:
                        if s.f < elem.f:
                            closed.remove(elem)
                        else:
                            lSuccesori.remove(s)
                        break

        for s in lSuccesori:  # Ii cautam locul in coada in asa fel incat nodurile sa ramane ordonate dupa f
            i = 0
            while i < len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i, s)

        myTime = time.time() - start;
        if myTime > Timeout:
            print("Time is out!")
            sir_afisare += "Time is out!"
            break



sir_afisare = ""

nume_fisier_intrare = input("Numele fisierului de intrare: ")
Timeout = int(input("Introduceti timeout-ul la care doriti sa se opreasca algoritmul: "))

gr = Graph(nume_fisier_intrare)

start = time.time()


#
# a_star(gr, "euristica_admisibila_1")
# nume_fisier_iesire = "output_a_star_optim_e1.txt"
# g = open(nume_fisier_iesire,"w")
# g.write(sir_afisare)

a_star(gr,"euristica_banala")
nume_fisier_iesire = "output_a_star_optim_banala.txt"
g = open(nume_fisier_iesire,"w")
g.write(sir_afisare)