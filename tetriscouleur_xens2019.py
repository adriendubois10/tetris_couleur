import random as rd
import matplotlib.pyplot as plt

largeur, hauteur = 6, 12

VIDE = []
#R, V, B, N , J = 1, 2, 3, 4, 5

R = [240, 10, 10]
V = [5, 240, 5]
B = [5, 5, 240]
J = [240, 240, 10]
N = [240, 10, 240]

def creergrille(l=largeur,h=hauteur):
    return [[(VIDE) for _ in range(h)] for _ in range(l)]

grille = [ [J, R, R, N, V, R, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
           [R, R, B, J, VIDE, R, N, V, VIDE, VIDE, VIDE, VIDE],
           [J, N, N, R, VIDE, J, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
           [J, J, VIDE, R, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
           [N, VIDE, R, VIDE, VIDE, R, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
           [VIDE, V, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, J, R, N]
         ]

lcolor = [R, V, B, N, J]

#affichage rudimentaire

def couleur(c):
    if c==[]:
        return ' '
    if c==[240, 10, 10]:
        return 'R'
    if c==[5, 240, 5]:
        return 'V'
    if c==[5, 5, 240]:
        return 'B'
    if c==[240, 240, 10]:
        return 'N'
    if c==[240, 10, 240]:
        return 'J'
    
def affichergrille(grille):
    l = len(grille)
    h = len(grille[0])
    for j in range(h-1,-1,-1):
        print('|',('{}'*l).format(*tuple([couleur(grille[i][j]) for i in range(l)])), '|' )
        
#Partie 2 - Barreau
        
def grillelibre(grille,k):
    l, h = len(grille), len(grille[0])
    test = False
    for i in range(l):
        test = test or grille[i][-k:]==[VIDE]*k
    return test
        
def descente(grille,x,y,k): # on suppose les hypothèses vérifiées
    for i in range(k):
        grille[x][y+i-1] = grille[x][y+i]
    grille[x][y+k-1] = VIDE
    
def deplacerbarreau(grille,x,y,k,direction):
    if (0<=x+direction<len(grille) and grille[x+direction][y:y+k] == k*[VIDE]):
        for j in range(y,y+k):
            grille[x+direction][j] = grille[x][j]
            grille[x][j] = VIDE
        
def permuterbarreau(grille,x,y,k):
    temp = grille[x][y+k-1]
    for j in range(y+k-1,y,-1):
        grille[x][j] = grille[x][j-1]
    grille[x][y] = temp
    
def descenterapide(grille,x,y,k):
    k0 = y
    while (k0-1)>=0 and grille[x][k0-1]==VIDE: #dernier indice non vide
        k0 += -1
    for j in range(k0,k0+k):
            grille[x][j] = grille[x][y-k0+j]
    for j in range(k0+k,y+k):
        grille[x][j] = VIDE
        
#Partie 3 - Detection des alignements et calcul du score
        
rt = [B,R,R,R,R,J,J,J,VIDE,VIDE,VIDE]
        
def detectalignement(rangee):
    
    changement, n, m = [], len(rangee), 1
    for i in range(n):
        if i==(n-1) or rangee[i]!=rangee[i+1]:
        #si i=n-1, la condtion est fausee et le 'ou' non exclusif permet de ne pas calculer rangee[n] qui n'existe pas 
            changement.append((rangee[i],m,i-(m-1)))
            m = 1
        else:
            m += 1
            
    score, marking = 0, [False]*n
    for k in changement:
        elem, m, i0 = k
        if elem != VIDE and m>=3:
            score += m-2
            marking[i0:i0+m] = [True]*m
    return (marking, score)
        
def scorerangee(grille,g,i,j,dx,dy):
    l, h = len(grille), len(grille[0])
    rangee, n = [], 0
    while 0<=i+n*dx<l and 0<=j+n*dy<h:
        rangee.append(grille[i+n*dx][j+n*dy])
        n += 1
    marking, score = detectalignement(rangee)
    for k in range(n):
        if marking[k]:
            g[i+k*dx][j+k*dy] = VIDE
    return score

def effacealignement(grille):
    l, h = len(grille), len(grille[0])
    g = grille.copy()
    score = 0
    for x in range(l): #horinzontal
        score += scorerangee(grille,g,x,0,0,1)
    for y in range(h): #vertical
        score += scorerangee(grille,g,0,y,1,0)
    for x in range(l-2): #diag vers haut droit depuis bas
        score += scorerangee(grille,g,x,0,1,1)
    for y in range(h-2): #diag vers haut droit depuis côté gauche
        score += scorerangee(grille,g,0,y,1,1)
    for x in range(l-2): #diag vers bas droit depuis haut
        score += scorerangee(grille,g,x,h-1,-1,-1)
    for y in range(2,h): #diag vers bas droit depuis côté gauche
        score += scorerangee(grille,g,0,y,1,-1)
    return (g, score)

def tassementcolonne(grille,x,hauteur):
    tasse, n = [], 0
    for c in grille[x]:
        if c!=VIDE:
            tasse.append(c)
            n += 1
    grille[x][:n] = tasse
    grille[x][n:] = [VIDE]*(hauteur-n)
    
def tassementgrille(grille):
    h = len(grille[0])
    for x in range(len(grille)):
        tassementcolonne(grille,x,h)
        
def calculscore(grille,t):
    score = 1
    new_score = -1
    g = grille.copy()
    while new_score != 0:
        plt.pause(2)
        score += new_score
        tassementgrille(grille)
        grille, new_score = effacealignement(grille)
        if t:
            refresh()
    return score

#Partie 5 - régions unicolores

def regionmax(grille):
    l, h = len(grille), len(grille[0])
    fait = [[False]*h]*l
    g = [[[couleur,0] for couleur in ligne] for ligne in grille]
    def prochevoisin(x,y,couleur):
        for dx in [-1,1]:
            if 0<=x+dx<l and (not fait[x+dx][y]) and g[x+dx][y][0]==couleur:
                g[x+dx][y][1] = g[x][y][1] + 1
                fait[x+dx][y] = True
            if 0<=x+dx<l and fait[x+dx][y] and g[x+dx][y][1]>g[x][y][1] and g[x+dx][y][0]==couleur:
                g[x][y][1] = g[x+dx][y][1]
            prochevoisin(x+dx,y,couleur)
        for dy in [-1,1]:
            if 0<=y+dy<l and (not fait[x][y+dy]) and g[x][y+dy][0]==couleur:
                g[x][y+dy][1] = g[x][y+dy][1] + 1
                fait[x][y+dy] = True
            if 0<=y+dy<l and fait[x][y+dy] and g[x][y+dy][1]>g[x][y][1]:
                g[x][y][1] = g[x][y+dy][1]
            prochevoisin(x,y+dy,couleur)
    for i in range(l):
        for j in range(h):
            if not fait[i][j] and g[i][j][0]!=VIDE:
                prochevoisin(i,j,g[i][j][0])
    return max([g[i][j][1] for i in range(l) for j in range(h)])

#Jeu

def genbarreau(grille,k):
    if not grillelibre(grille,k):
        return -1
    else:
        l, xi = len(grille), []
        for i in range(l):
            if grille[i][-k:]==[VIDE]*k:
                xi.append(i)
        n = len(lcolor)
        l, h = len(grille), len(grille[0])
        x = xi[rd.randint(0,len(xi)-1)]
        I = [rd.randint(0,n-1) for _ in range(k)]
        for i in range(h-k,h):
            grille[x][i] = lcolor[I[i-(h-k)]]
        return x
        
def derniere_case_nonvide(grille,x):
    h = len(grille[x])
    for k in range(h-1,-1,-1):
        if grille[x][k]!=VIDE:
            return k
    return 0          
        
    


        
        
    
    
    