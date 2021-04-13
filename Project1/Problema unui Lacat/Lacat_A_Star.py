import copy
import time

class NodParcurgere:
    def __init__(self, info, key,parinte, cost = 0, h = 0):
        self.info = info
        self.key = key  # Cheia cu care incuietoarea a ajuns in aceasta stare (muchia din graful de parcurgere)
        self.parinte = parinte
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        global sir_afisare
        l = self.obtineDrum()
        i = 1
        for nod in l:
            if nod.key is not None:
                sir_afisare += str(i) + ") Incuietori: " + str(nod.parinte) + '\n'
                sir_afisare += "Folosim cheia: " + str(nod.key) + " pentru a ajunge la " + str(nod) + '\n'
                i += 1

        sir_afisare += "Incuietori(stare scop): " + str(nod) + '\n'
        if afisCost:
            sir_afisare += "S-au realizat : " + str( self.g ) + " operatii." + '\n'
        if afisLung:
            sir_afisare += "Lungimea drumului: " + str(len(l)) + '\n'
        return len(l)

    def contineInDrum(self, infoNodNou):
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

        sir = "[ "
        incuietori = self.info
        for i in range (len(incuietori)-1):
            sir += "inc(" + str(incuietori[i][0]) + "," + str(incuietori[i][1]) + "), "

        sir += "(" + str(incuietori[len(incuietori)-1][0]) + ","+  str(incuietori[len(incuietori)-1][1]) + ")]"

        #sir += str(self.info)
        return sir

class Graph: # graful problemei

    def __init__(self, nume_fisier):

        global sir_afisare
        f = open(nume_fisier,"r")
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
        for i in range(nrIncuietori):
            incuietoriScop.append(['d', 0])

        self.scopuri.append (incuietoriScop)

        NodStart = NodParcurgere(self.start, None, None, 0, 0)
        sir_afisare += "Initial: " +  str(NodStart) + '\n'
      #  print("Stari finale: ", str(self.scopuri))

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    def genereazaSuccesori(self, nodCurent,tip_euristica):
        listaSuccesori = []
        #print("Genereaza succesori")



        for i in range(len(self.lista_chei)):

            incuietoariNoi = copy.deepcopy(nodCurent.info)
            #print("incuietoariNoi: ", incuietoariNoi)
            cheie = copy.deepcopy(self.lista_chei[i])
            #print(cheie)

            for indice in range(len(cheie)):


                #print("cheie[indice]",cheie[indice])
                if cheie[indice] == 'i':
                    if incuietoariNoi[indice][0] == 'd': # Daca incuietaorea e deschisa o inchidem
                        incuietoariNoi[indice][0] = 'i'
                    incuietoariNoi[indice][1] += 1 # O mai inchidem o data sau o inchidem pentru prima oara daca era deschisa
                elif cheie[indice] == 'd': # Daca avem o cheie de deschidere

                   # if incuietoariNoi[indice][0] == 'd': # daca e deja deschisa o lasam asa
                    #    continue
                    if incuietoariNoi[indice][0] == 'i':

                        if incuietoariNoi[indice][1] == 1: # daca e inchisa o singura data, o deschidem
                            incuietoariNoi[indice] = ['d',0]

                        elif incuietoariNoi[indice][1] > 1 :
                            incuietoariNoi[indice][1] -= 1 # o deschidem o data
                elif cheie[indice] == 'g':
                    continue


            if not nodCurent.contineInDrum(incuietoariNoi):

                nodNou = NodParcurgere(
                    incuietoariNoi,
                    cheie,
                    nodCurent, # parinte
                    nodCurent.g + 1, # cost 1
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
        maximInchis = 0
        for incuietoare in infoNod:
            if incuietoare[0] == 'i':
                if incuietoare[1] > maximInchis:
                    maximInchis = incuietoare[1]
        return maximInchis


def a_star(gr, tip_euristica,nrSolutiiCautate=4):
    global nrSolutie
    global sir_afisare
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, None, 0, gr.calculeaza_h(gr.start, tip_euristica))]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            sir_afisare += "Solutie: " + str(nrSolutie) + "\n"
            nrSolutie += 1
            nodCurent.afisDrum(afisLung=True, afisCost=True)
            end = time.time()
            sir_afisare += "Runtime of the program is: " + str(end - start) +"\n"
            sir_afisare += "-------------------------------------------------------\n"

           # input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        for s in lSuccesori:
            i = 0
            while i < len(c):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i, s)


        myTime = time.time() - start;
        if myTime > Timeout:
            print("Time is out!")
            sir_afisare += "Time is out!"
            break

       # print("My time:", myTime)



sir_afisare = ""
nrSolutie = 1 # Variabila care ne ajuta sa numaram solutiile

nume_fisier_intrare = input("Numele fisierului de intrare: ")
Timeout = int(input("Introduceti timeout-ul la care doriti sa se opreasca algoritmul: "))
nrSolutiiCautate = int(input("Numarul de solutii cautate: "))

gr = Graph(nume_fisier_intrare)

start = time.time()



a_star(gr, "euristica_admisibila_1",nrSolutiiCautate)
nume_fisier_iesire = "output_a_star_e1.txt"
g = open(nume_fisier_iesire,"w")
g.write(sir_afisare)

# a_star(gr,"euristica_banala",nrSolutiiCautate)
# nume_fisier_iesire = "output_a_star_banala.txt"
# g = open(nume_fisier_iesire,"w")
# g.write(sir_afisare)