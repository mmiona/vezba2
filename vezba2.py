#DINAMICKO PLANIRANJE KONEKCIJA KOLA U RANZIRNIM STANICAMA 
from pulp import *

#Broj dolaznih vozova
n = ["1111", "1112", "1113"]
#Broj odlaznih vozova
m =["1000", "1002", "1003"]
#vreme prispeca dolaznog voza, diskretizovano u minutama
ai = {"1111": 10, "1112": 50, "1113": 150}
#vreme pregleda dolaznog voza
ti = {"1111": 30, "1112": 30, "1113": 30} 
#vreme otpreme odlaznog voza j
dj = {"1000": 100, "1002":160, "1003": 250} 

#vreme potrebno za naguravanje dolaznog voza 
hi = {"1111": 5, "1112": 5, "1113": 5}
#skup odsecaka koji pripadaju dolaznom vozu i
ui = {"1111": ["A", "B", "C"], "1112": ["D", "E"], "1113": ["F", "G"]}
#skup odsecaka koji mogu da budu dodeljeni odlaznom vozu
uj = {"1000": ["C", "D"], "1002": ["A", "B"], "1003": ["E", "F", "G"]}


#skup svih odsecaka
U = ["A", "B", "C", "D", "E", "F", "G"]

#skup odlaznih vozova koji mogu da prevoze odsecak u
ju = {"1000": "A", "1002": "A", "1002": "B", "1003": "B", "1003": "C", "1000": "D", "1002": "D", "1003": "D",
"1000": "E", "1002": "E", "1003": "E", "1000": "F", "1002": "F", "1003": "F", "1000": "G", "1002": "G", "1003": "G"}

#osobine odsecaka
F= ["r", "w","l"]
efu= {
    ("r", "A"): 10, ("w", "A"): 1250, ("l", "A"): 15,
    ("r", "B"): 20, ("w", "B"): 2350, ("l", "B"): 15, 
    ("r", "C"):15, ("w","C"):1750, ("l","C"):15, 
    ("r", "D"): 10, ("w", "D"):1250, ("l","D"):15, 
    ("r", "E"):20, ("w", "E"): 3350, ("l","E"):15, 
    ("r", "F"):20, ("w","F"):2250, ("l","F"):15, 
    ("r", "G"):20, ("w","G"):2550, ("l","G"):15
} 
#r - broj kola; #w - tezina; #l - duzina; 
#(r,w, l) = splitDict (f)

#minimalno vreme za odsecak da bude preusmeren na odlazni voz nakon sto je ranziran 
t = {"A": [30], "B": [30], "C":[30], "D": [30], "E": [30], "F":[30], "G":[30]} 

#vreme pregleda i formiranja odlaznog voza j
bvj ={"1000": [20, 20], "1002": [20,20], "1003": [20,20]} 
(bj,vj) = splitDict(bvj)

#maximalne vrednosti osobine f odlaznog voza j
gjf = {
    ("1000", "r"): 2000, ("1000", "w"): 2000, ("1000","l"): 2000, 
    ("1002", "r"): 2000, ("1002", "w"): 2000, ("1002", "l"): 2000, 
    ("1003", "r"): 2000, ("1003", "w"): 2000, ("1003", "l"): 2000
}

#minimalne vrednosti osobine f odlaznog voza j
pjf = {
    ("1000", "r"): 20, ("1000", "w"): 20, ("1000","l"): 20,
    ("1002", "r"): 20, ("1002", "w"): 20, ("1002", "l"): 20,
    ("1003", "r"): 20, ("1003", "w"):20, ("1003", "l"): 20
}

#trosak dodeljivanja odsecka odlaznom vozuj
#cju ("A": [10, 10, 10], "B":[20, 20, 20], "c":[10, 15, 20], "D":[30, 30, 30], "E":[30, 30, 30], "F":[20, 20, 20], "G":[20, 10, 20]} cju ("1000", "A"): 100, ("1000", "B"): 100,
cju = {
    ("1000", "A"): 100, ("1000", "B"): 100, ("1000", "C"): 100, ("1000", "D"): 100, ("1000", "E"): 200, ("1000", "F"): 250, ("1000", "G"): 290, 
    ("1002", "A"): 300, ("1002", "B"): 300, ("1002", "C"): 300, ("1002", "D"): 300, ("1002", "E"): 300, ("1002", "F"): 300, ("1002", "G"): 300, 
    ("1003", "A"): 300, ("1003", "B"): 300, ("1003", "C"): 300, ("1003", "D"): 300, ("1003", "E"): 300, ("1003", "F"): 300, ("1003", "G"): 300,
}
#trosak otkazivanja odlaznog voza j
oj = {"1000": 10, "1002": 20, "1003": 30}


K= [1,2,3]
#L redosled formiranja odlaznog voza
L= [1,2,3]
M=1000
T=25


# ================================
#PROMENLJIVE ODLUCIVANJA
# Promenljiva koja označava pozicije dolaznih vozova u nizu za formiranje.
DolazniRanziranje = LpVariable.dicts ("DolazniRanziranje", [(i, k) for i in n for k in K], 0, 1, LpBinary)
# Promenljiva koja označava pozicije odlaznih vozova u nizu za formiranje.
OdlazniRanziranje = LpVariable.dicts ("OdlazniRanziranje", [(j,l) for j in m for l in L], 0,1, LpBinary)
# Promenljiva koja označava prisustvo vagona na određenim pozicijama.
PrisustvoNaPozicijama = LpVariable.dicts("PrisustvoNaPozicijama", [(j,u) for j in m for u in U], 0, 1, LpBinary)
# Promenljiva koja označava aktivnost odlaznih vozova
AktivnostOdlaznihVagona = LpVariable.dicts("AktivnostOdlaznihVagona", [(j) for j in m], 0,1, LpBinary)
# Promenljiva koja označava formirane odlazne vagone.
FormiraniOdlazniVagoni = LpVariable.dicts ("FormiraniOdlazniVagoni", [(l,k) for l in L for k in K], 0,1, LpBinary)
# Promenljiva koja označava osobine odlaznih vagona
OsobineOdlaznihVagona = LpVariable.dicts("OsobineOdlaznihVagona", [(j,f) for j in m for f in F], 0,1, LpBinary)
# Promenljiva koja označava vremena tehničkog pregleda
VremenaTehnickogPregleda = LpVariable.dicts ("VremenaTehnickogPregleda", [(i) for i in n], 0, None, LpContinuous)
# Promenljiva koja označava vremena otpreme
VremenaOtpreme = LpVariable.dicts("VremenaOtpreme", [(j) for j in m], 0, None, LpContinuous)

#FUNKCIJA CILJA (1)
load = LpProblem ("Railcar_yards", LpMinimize)
load += (
    lpSum (cju [(j, u)]*PrisustvoNaPozicijama[(j, u)] for j in m for u in U) - lpSum (oj [(j)]*AktivnostOdlaznihVagona [(j)] for j in m)
)


#OGRANICENJA
#Ogranicenje 2: hump engine can only start to push an inbound train over the hump after 
#the engine finishes the previous train
for k in range (len (n)-1):
    load += (
        VremenaTehnickogPregleda[n[k+1]] - VremenaTehnickogPregleda[n[k]] - lpSum (hi [(i)]*DolazniRanziranje[(i,k+1)] for i in n) >= 0 
        #mora k+1 jer za indeks 0 nema vrednosti za DolazniRanziranje
    )


#Ogranicenje 3: Dolazni vozovi ne mogu biti ranzirani pre nego je odradjen tehnicki pregled 
for k in range (len (n)):
    load += (
        VremenaTehnickogPregleda[n[k]] - lpSum((ai [(i)] + ti[(i)]) *DolazniRanziranje[(i,k+1)] for i in n) >= 0 
        #mora k+1 jer za indeks 0 nema vrednosti za DolazniRanziranje
    )


#Ogranicenje 4 i 5: Dodeljuju svakom dolaznom vozu tacno jednu poziciju u ranzirnom nizu 
for k in range (len (n)): 
    load += (
        lpSum (DolazniRanziranje[(i,k+1)] for i in n) == 1
        #mora k+1 jer za indeks 0 nema vrednosti za DolazniRanziranje
    )
for i in n: 
    load += (
        lpSum (DolazniRanziranje[(i,k+1)] for k in range(len(n))) == 1
        #mora k+1 jer za indeks 0 nema vrednosti za DolazniRanziranje
    )


# #Ogranicenje 6: ranzirna lokomotiva formira bilo koji odlazni voz
# samo kada svi odsecci dodeljeni
# #odlaznom vozu su ranzirani sa operativnom vrem rezervom koja se zasniva na delta (lk)... 
for k in range(len(n)):
    for l in range(len(m)):
        load += (
                VremenaOtpreme[m[l]] - VremenaTehnickogPregleda[n[k]] - lpSum(hi[i]*DolazniRanziranje[(i,k+1)] for i in n) - T >= M*(FormiraniOdlazniVagoni[(l+1,k+1)]-1)
                #mora k+1 jer za indeks 0 nema vrednosti za DolazniRanziranje
                #T je skalar, nije definisano posebno za svaki odsecak
            )

# #Ogranicenje 7: if any cuts from the k-th classified inbound train are assigned to the 1-th assembled outbound train
for k in range(len(n)) :
    for i in n:
        for j in m:
            for l in range (len (m) ) :
                load += (
                    #ovde odradi presek da nije prazan skup izmedju dolaznih i odlaznih vozova
                    M* (FormiraniOdlazniVagoni[(1+1,k+1)]+2 - DolazniRanziranje[(i,k+1)] - OdlazniRanziranje[(j,1+1)]) >= lpSum(PrisustvoNaPozicijama[(j,u)] for u in U if u in ui[i] and u in uj[j])
                )
# #Ogranicenje 8:
for l in range(len (m)-1):
    load+=(
        VremenaOtpreme[m[l+1]]- VremenaOtpreme[m[1]] - lpSum(vj[j]*OdlazniRanziranje[(j, 1+1) ] for j in m)>= 0
    )

#Ogranicenje 9: svaki formirani odlazni voz zadovoljava planirano vreme otpreme
for l in range (len (m) ) :
    load += (
        VremenaOtpreme[m[1]] <= lpSum((dj[(j)] - vj[j] - bj[j])*OdlazniRanziranje[ (j, 1+1) ] for j in m) + M* (1-lpSum (OdlazniRanziranje[ (j, 1+1) ] for j in m) )
)

# #Ogranicenje 10 i 11: Svaki odlazni voz je dedeljen samo jednoj poziciji u nizu za formiranje,
# #pod uslovom da nije otkazan
for j in m:
    load += (
        lpSum(OdlazniRanziranje[(j, 1+1) ] for l in range(len(m)-1) ) == AktivnostOdlaznihVagona[j]
    )
for l in range(len(m)-1) :
    load += (
        lpSum(OdlazniRanziranje[(j,1+1)] for j in m) <= 1
    )

#Ogranicenje 12 svaki odsecak dodeljen najvise jednom odlaznom vozu
for u in U:
    load += (
        lpSum(PrisustvoNaPozicijama[(j,u)] for j in ju) <= 1
    )

#Ogranicenje 13 Maksimalne i minimalne gran vrednosti svakog odlaznog voza
for j in m:
    for f in F:
        load += (
            lpSum(efu[(f,u)]*PrisustvoNaPozicijama[(j,u)] for u in U) <= gjf[(j, f)]*AktivnostOdlaznihVagona[(j)]
        )

#Ogranicenje 14: Minimalne gran vrednosti ...
for j in m:
    for f in F:
        load += (
            lpSum(efu[(f,u)] * PrisustvoNaPozicijama[(j,u)] for u in U) >= pjf[(j, f)] * OsobineOdlaznihVagona[(j,f)]
        )

#Ogranicenje 15:
for j in m:
    load += (
        lpSum(OsobineOdlaznihVagona[(j,f)] for f in F) >= AktivnostOdlaznihVagona [(j)]
    )

# #problem solve
load.solve()

#Print the results
print("Status: ", LpStatus [load. status])

for v in load. variables () :
    print(v.name, "=", v.varValue)
print("The optimal value of the objective function is =", value (load. objective))

# # #print (allyards [0:5])
load.writeLP('RailCarYards.txt')
