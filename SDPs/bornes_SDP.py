cardX,cardY,cardA,cardB = 2,2,2,2
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import math as math
import time as time
def Alphabet(cardX,cardY,cardA,cardB): #return l'alphabet 
    alphabetx=[]
    alphabety=[]
    for x in range(1, cardX+1):
        for a in range(1, cardA+1):
            alphabetx.append(("x",x,a))
    for y in range(1, cardY+1):
        for b in range(1, cardB+1):
            alphabety.append(("y",y,b))
    return alphabetx,alphabety

AlphaX,AlphaY=Alphabet(cardX,cardY,cardA,cardB)

def afficher_matrice_graphique(matrice):
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=matrice, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(matrice[0]))))  # Ajuste largeur
    plt.show()

def afficher_matrice_jolie_simple(matrice):
    for row in matrice:
        print(" ".join([f"{x:4}" for x in row]))

def afficher_matrice_jolie_floats(matrice, decimals=3):
    for row in matrice:
        print(" | ".join([f"{x:.{decimals}f}" for x in row]))
              
def tuple_(mot):
    (lx,ly)=mot
    return (tuple(lx),tuple(ly))


def RepresentantEquivalence(mot): #return le représentant de la classe d'équivalence avec les x à gauche et les y à droite
    lx,ly= mot
    #on supprime les égalités :)
    i = 1
    lx2=[]
    ly2=[]
    if len(lx)>0 :
        lx2.append(lx[0])
    if len(ly)>0:
        ly2.append(ly[0])
    while i<len(lx) : 
        if lx[i-1]!=lx[i] :
            lx2.append(lx[i])
        i+=1
    i=1
    while i<len(ly):
        if ly[i-1]!=ly[i]:
            ly2.append(ly[i])
        i+=1
    return (lx2,ly2)

def EstEquivalent(mot1,mot2):
    return RepresentantEquivalence(mot1)==RepresentantEquivalence(mot2)

def GénèreMotsdim_sup(Mots_dim_inf):
    nouveaux_mots=[]
    n=len(Mots_dim_inf[0][0]+Mots_dim_inf[0][1])
    for mot in Mots_dim_inf :
        n_mot=len(mot[0])
        if n_mot==n:
            for lettre in AlphaX:
                if n_mot==0 or lettre!=mot[0][-1]:
                    nouveaux_mots.append((mot[0].copy()+[lettre],mot[1].copy()))
        for lettre in AlphaY:
            if n-n_mot==0 or lettre!=mot[1][-1]:
                nouveaux_mots.append((mot[0].copy(),mot[1].copy()+[lettre]))
    return nouveaux_mots

def GénèreMots(k): 
    L_tous_les_mots=[]
    L_mots=[([],[])]
    L_tous_les_mots+=L_mots
    for i in range(k):
        L_mots=GénèreMotsdim_sup(L_mots)
        L_tous_les_mots+=L_mots
    return L_tous_les_mots

def Sous_mot_nul(sous_mot):
    i=1
    while i < len(sous_mot):
        if sous_mot[i][1]==sous_mot[i-1][1] and sous_mot[i][2]!=sous_mot[i-1][2]:
            return True
        i+=1
    return False

def Reverse(mot):
    (lx,ly)=mot
    lx=lx[::-1]
    ly=ly[::-1]
    return (lx,ly)

def Concaténer(mot1,mot2):
    mot1=Reverse(mot1)
    (lx1,ly1),(lx2,ly2)=mot1,mot2
    return (lx1+lx2,ly1+ly2)

def Contrainte1(liste_k): #retourne un couple avec la contrainte 1 sous forme matrice et coef
    dimension=len(liste_k)
    matrice=np.zeros((dimension,dimension))
    matrice[0,0]=1
    return [(matrice,1)]


def Contrainte2(liste_k,k):
    dimension=len(liste_k)
    contraintes=[]
    liste_représentants=[]
    dico={} # :)
    for i in range(dimension):
        mot1=liste_k[i]
        for j in range(dimension):
            mot2=liste_k[j]
            mot_concatene=Concaténer(mot1,mot2)
            représentant=RepresentantEquivalence(mot_concatene)
            liste_représentants.append([représentant,(i,j)])
    liste_représentants.sort()
    i=1
    new_liste_représentants=[liste_représentants[0][0]]
    dico[tuple_(liste_représentants[0][0])]=liste_représentants[0][1]
    while i<len(liste_représentants):
        if liste_représentants[i][0]!=liste_représentants[i-1][0]:
            dico[tuple_(liste_représentants[i][0])]=liste_représentants[i][1]
            if len(liste_représentants[i][0][0])+len(liste_représentants[i][0][1])<2*k:
                new_liste_représentants.append(liste_représentants[i][0])
        i=i+1
    
    for mot in new_liste_représentants :
        (lx,ly)=mot
        i=0
        nx=len(lx)
        ny=len(ly)
        for i in range(0,nx+1):
            s=lx[:i]
            t=lx[i:]+ly
            
            for x in range(1,cardX+1):
                M=np.zeros((dimension,dimension))
                (i0,j0)=dico[tuple_(mot)]
                M[i0,j0]+=-1/2
                M[j0,i0]+=-1/2
                for a in range(1,cardA+1):
                    (i1,j1)=dico[tuple_(RepresentantEquivalence((s+[("x",x,a)]+lx[i:],ly)))]
                    M[i1,j1]+=1/2
                    M[j1,i1]+=1/2
                contraintes.append((M,0))
        for j in range(0,ny+1):
            s=lx + ly[:j]
            t=ly[j:]
            
            for y in range(1,cardY+1):
                M=np.zeros((dimension,dimension))
                (i0,j0)=dico[tuple_(mot)]
                M[i0,j0]-=1
                M[j0,i0]-=1
                for b in range(1,cardB+1):
                    (i1,j1)=dico[ tuple_(RepresentantEquivalence((lx,ly[:j]+[("y",y,b)]+t))) ]
                    M[i1,j1]+=1
                    M[j1,i1]+=1
                contraintes.append((M,0))
    return contraintes
    
              

def Contrainte3(liste_k): #réduire complexité 
    dimension=len(liste_k)
    contraintes=[]
    for i in range(dimension):
        mot1=liste_k[i]
        for j in range(i,dimension) :
            mot2=liste_k[j]
            mot_concatene=Concaténer(mot1,mot2)
            if Sous_mot_nul(mot_concatene[0]) or Sous_mot_nul(mot_concatene[1]):
                matrice=np.zeros((dimension,dimension))
                matrice[i,j]=1
                matrice[j,i]=1
                contraintes.append((matrice,0))
    return contraintes

    
def Contrainte4(liste_k):
    dimension=len(liste_k)
    contraintes=[]
    liste_représentants=[]
    for i in range(len(liste_k)):
        mot1=liste_k[i]
        for j in range(len(liste_k)) :
            mot2=liste_k[j]
            mot_concatene=Concaténer(mot1,mot2)
            représentant=RepresentantEquivalence(mot_concatene)
            liste_représentants.append([représentant,(i,j)])
    liste_représentants.sort()
    l=len(liste_représentants)
    i=1
    while i<len(liste_représentants):
        if liste_représentants[i][0]==liste_représentants[i-1][0]:
            (i0,j0)=liste_représentants[i][1]
            (i1,j1)=liste_représentants[i-1][1]
            matrice=np.zeros((dimension,dimension))
            matrice[i0,j0]+=1
            matrice[j0,i0]+=1
            matrice[i1,j1]-=1
            matrice[j1,i1]-=1
            if (i0,j0) != (i1,j1) and (i0,j0) != (j1,i1):
                contraintes.append((matrice,0))
        i=i+1
    return contraintes


def GoalSDP(Bell_Matrix,dimension):
    matrice=np.zeros((dimension,dimension))
    for i in range(1,cardA*cardX+1):
        for j in range(1,cardB*cardY+1):
            matrice[cardA*cardX + i, j ] = Bell_Matrix[j-1,i-1]/2 #wesh
            matrice[j,cardA*cardX+i] = Bell_Matrix[j-1,i-1]/2
    return matrice

def SDP(k,bell_matrix):
    t0=time.time()
    liste_k=GénèreMots(k)
    print("On a fini la liste_k")
    print(time.time()-t0)
    dimension=len(liste_k)
    contraintes=[]
    contraintes+=Contrainte1(liste_k)
    print("Contrainte1", time.time()-t0)
    contraintes+=Contrainte2(liste_k,k)
    print("Contrainte2", time.time()-t0)
    contraintes+=Contrainte3(liste_k)
    print("Contrainte3", time.time()-t0)
    contraintes+=Contrainte4(liste_k)
    print("Contrainte4", time.time()-t0)
    
    matrice_SDP=GoalSDP(bell_matrix,dimension)
    R=cp.Variable((dimension,dimension),symmetric=True)
    
    objective=cp.Maximize(cp.trace(matrice_SDP @ R))
    
    constraints=[]
    
    for (matrice,borne) in contraintes :
        constraints.append(cp.trace(matrice @ R) == borne)
    constraints.append(R>>0)
    print("On commence le problème")
    print("On commence", time.time()-t0)
    problem=cp.Problem(objective,constraints)
    problem.solve()
    print("Fini", time.time()-t0)
    print(problem.value)


bell_matrix=np.zeros((4,4))


bell_matrix[0,0]=1
bell_matrix[0,1]=-1
bell_matrix[1,0]=-1
bell_matrix[1,1]=1

bell_matrix[0,2]=1
bell_matrix[0,3]=-1
bell_matrix[1,2]=-1
bell_matrix[1,3]=1

bell_matrix[2,0]=1
bell_matrix[2,1]=-1
bell_matrix[3,0]=-1
bell_matrix[3,1]=1

bell_matrix[2,2]=-1
bell_matrix[2,3]=1
bell_matrix[3,2]=1
bell_matrix[3,3]=-1



SDP(2,bell_matrix)
