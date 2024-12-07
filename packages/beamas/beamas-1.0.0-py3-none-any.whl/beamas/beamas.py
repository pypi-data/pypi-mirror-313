##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################
# BEGIN 
##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################


##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################
# IMPORT 
##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################

import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.linalg import eig

##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################
# FONCTIONS PRIMORDIALES 
##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################


##########################################################################################################################################################################################
# MATRICE DE RIGIDITE ISOTROPE
##########################################################################################################################################################################################


def Matrice_de_rigidite_iso(P,f) :
    
    # Constantes 

    E = P.materiau.E
    rho = P.materiau.rho
    L = P.L
    G = P.materiau.G
    J = P.J
    S = P.h * P.b
    I = P.Iz
    m = P.m
    w = 2 * math.pi * f

    # Traction-Compression

    alpha = E * S * w * math.sqrt(rho / E)
    C1 = math.cos(w * L * math.sqrt(rho / E))
    S1 = math.sin(w * L * math.sqrt(rho / E))

    a1 = (-C1 * S1 * S1 * alpha) / (1 - (C1 * C1 * S1))
    b1 = (alpha * S1) / (1 - (C1 * C1 * S1))
    c1 = (alpha * S1) / (1 - (C1 * C1 * S1))
    d1 = (alpha * S1 * C1) / ((C1 * C1 * S1) - 1)

    # Torsion

    alpha2 = G * J * w * math.sqrt((rho * I)/(G * J) )
    C2 = math.cos(w * L * math.sqrt((rho * I)/(G * J) ))
    S2 = math.sin(w * L * math.sqrt((rho * I)/(G * J) ))

    a2 = (-C2 * S2 * S2 * alpha2) / (1 - (C2 * C2 * S2))
    b2 = (alpha2 * S2) / (1 - (C2 * C2 * S2))
    c2 = (alpha2 * S2) / (1 - (C2 * C2 * S2))
    d2 = (alpha2 * S2 * C2) / ((C2 * C2 * S2) - 1)

    # Flexion

    a = math.sqrt(math.sqrt((m * w * w) / (E * I * L)))
    s = math.sin(a * L)
    c = math.cos(a * L)
    S = math.sinh(a * L)
    C = math.cosh(a * L)
    df = 1 - (c * C)
    q = a * L

    alphaf = (((s * C) - (c * S)) * q) / df
    alphafbar = ((S - s) * q) / df
    betaf = (s * S * q * q) / df
    betafbar = ((C - c) * q * q) / df
    gammaf = (((s * C) + (c * S)) * q * q * q) / df
    gammafbar = ((S + s) * q * q * q) / df

    a3 = (E * I * gammaf) / (L * L * L)
    b3 = (-E * I * gammafbar) / (L * L * L)
    c3 = (-E * I * betaf) / (L * L)
    d3 = (-E * I * betafbar) / (L * L)

    i = (-E * I * gammafbar) / (L * L * L)
    j = (E * I * gammaf) / (L * L * L)
    k = (E * I * betafbar) / (L * L)
    l = (E * I * betaf) / (L * L)

    e = -l
    f = k
    g = (alphaf * E * I) / L
    h = (alphafbar * E * I) / L

    m = -f
    n = -e
    o = (alphafbar * E * I) / L
    p = g

    # Matrice

    MRG = np.zeros((12, 12))

    MRG[0, 0] = a1
    MRG[0, 6] = b1
    MRG[1, 1] = a3
    MRG[1, 5] = c3
    MRG[1, 7] = b3
    MRG[1, 11] = d3
    MRG[2, 2] = a3
    MRG[2, 4] = e
    MRG[2, 8] = b3
    MRG[2, 10] = d3
    MRG[3, 3] = a2
    MRG[3, 9] = b2
    MRG[4, 2] = e
    MRG[4, 4] = g
    MRG[4, 8] = f
    MRG[4, 10] = h
    MRG[5, 1] = e
    MRG[5, 5] = g
    MRG[5, 7] = f
    MRG[5, 11] = h
    MRG[6, 0] = c1
    MRG[6, 6] = d1
    MRG[7, 1] = i
    MRG[7, 5] = k
    MRG[7, 7] = j
    MRG[7, 11] = l
    MRG[8, 2] = b3
    MRG[8, 4] = f
    MRG[8, 8] = j
    MRG[8, 10] = n
    MRG[9, 3] = c2
    MRG[9, 9] = d2
    MRG[10, 2] = d3
    MRG[10, 4] = h
    MRG[10, 8] = n
    MRG[10, 10] = p
    MRG[11, 1] = m
    MRG[11, 5] = o
    MRG[11, 7] = n
    MRG[11, 11] = p
    
    
    return MRG
    
    
##########################################################################################################################################################################################
# MATRICE DE RIGIDITE ORTHOTROPE
##########################################################################################################################################################################################    
    
    
def Matrice_de_rigidite_ortho(p,f) :
    
    ## CONSTANTES ##
    
    E1 = p.materiau.E_1
    E2 = p.materiau.E_2
    E3 = p.materiau.E_3
    
    G23 = p.materiau.G_23
    G13 = p.materiau.G_13
    G12 = p.materiau.G_12
    
    nu23 = p.materiau.nu_23
    nu13 = p.materiau.nu_13
    nu12 = p.materiau.nu_12
    
    rho = p.materiau.rho
    
    alpha = p.alpha

    h = p.h
    b = p.b
    L = p.L
    
    Iz = p.Iz
    Iy = p.Iy
    
    I0 = Iy + Iz
    
    S = b * h
    
    ky = p.ky
    kz = p.kz

    s = np.array([
        [1 / E1, -nu12 / E1, -nu13 / E1, 0, 0, 0],
        [-nu12 / E1, 1 / E2, -nu23 / E2, 0, 0, 0],
        [-nu13 / E1, -nu23 / E2, 1 / E3, 0, 0, 0],
        [0, 0, 0, 1 / G23, 0, 0],
        [0, 0, 0, 0, 1 / G13, 0],
        [0, 0, 0, 0, 0, 1 / G12]
    ])

    cos_alpha = np.cos(alpha)
    sin_alpha = np.sin(alpha)
    cos_2alpha = np.cos(2 * alpha)
    sin_2alpha = np.sin(2 * alpha)

    S11p = (s[0, 0] * cos_alpha**4 + s[1, 1] * sin_alpha**4 +
            2 * s[0, 1] * sin_alpha**2 * cos_alpha**2 + s[5, 5] * sin_alpha**2 * cos_alpha**2)
    S16p = (-s[0, 0] * np.sin(2 * alpha) * cos_alpha**2 + s[0, 1] * np.sin(2 * alpha) * cos_2alpha +
            s[1, 1] * np.sin(2 * alpha) * sin_alpha**2 + s[5, 5] * sin_alpha * cos_alpha * cos_2alpha)
    S55p = s[3, 3] * sin_alpha**2 + s[4, 4] * cos_alpha**2
    S66p = (s[0, 0] * np.sin(2 * alpha)**2 + s[1, 1] * np.sin(2 * alpha)**2 -
            2 * s[0, 1] * np.sin(2 * alpha)**2 + s[5, 5] * np.cos(2 * alpha)**2)

    C11p = S66p / (S11p * S66p - S16p**2)
    C55p = 1 / S55p
    C66p = S11p / (S11p * S66p - S16p**2)
    C16p = S16p / (S11p * S66p - S16p**2)
    
    ## MATRICES ##
    
    
    # Système1
    
    A1 = np.array([
        [C11p * S, C16p * S * ky, 0],
        [C16p * S * ky, C66p * S * ky, 0],
        [0, 0, C11p * Iz]
    ])
    B1 = np.array([
        [0, 0, -C16p * S * ky],
        [0, 0, -C66p * S * ky],
        [C16p * S * ky, C66p * S * ky, 0]
    ])


    b_mat1 = np.block([
        [np.eye(3), np.zeros((3, 3))],
        [np.zeros((3, 3)), -A1]
    ])

    
    D1 = np.array([
        [0, 0, C16p * S * ky],
        [0, 0, C66p * S * ky],
        [0, 0, 0]
    ])


   
    w1 = 2 * np.pi * f
    C1 = np.array([
        [rho * w1**2 * S, 0, 0],
        [0, rho * w1**2 * S, 0],
        [0, 0, rho * Iz * w1**2 - C66p * S * ky]
        ])
    a1 = np.block([
            [np.zeros((3, 3)), np.eye(3)],
            [C1, B1]
        ])
    Lb1, V1 = scipy.linalg.eig(a1, b_mat1)

    
    G01 = np.array([
            [V1[0,0],V1[0,1],V1[0,2],V1[0,3],V1[0,4],V1[0,5]],
            [V1[1,0],V1[1,1],V1[1,2],V1[1,3],V1[1,4],V1[1,5]],
            [V1[2,0],V1[2,1],V1[2,2],V1[2,3],V1[2,4],V1[2,5]]
            
            ])
        
    G_exp1 = np.array([
            [V1[0,0]* np.exp(Lb1[0] * L),V1[0,1]* np.exp(Lb1[1] * L),V1[0,2]* np.exp(Lb1[2] * L),V1[0,3]* np.exp(Lb1[3] * L),V1[0,4]* np.exp(Lb1[4] * L),V1[0,5]* np.exp(Lb1[5] * L)],
            [V1[1,0]* np.exp(Lb1[0] * L),V1[1,1]* np.exp(Lb1[1] * L),V1[1,2]* np.exp(Lb1[2] * L),V1[1,3]* np.exp(Lb1[3] * L),V1[1,4]* np.exp(Lb1[4] * L),V1[1,5]* np.exp(Lb1[5] * L)],
            [V1[2,0]* np.exp(Lb1[0] * L),V1[2,1]* np.exp(Lb1[1] * L),V1[2,2]* np.exp(Lb1[2] * L),V1[2,3]* np.exp(Lb1[3] * L),V1[2,4]* np.exp(Lb1[4] * L),V1[2,5]* np.exp(Lb1[5] * L)]
            
            ])
        
        
    di1=np.diag(Lb1)
        
    G1 = np.vstack([G01, G_exp1])
        
        
    H1=np.block([[-A1, np.zeros((3, 3))], [np.zeros((3, 3)), A1]])@ G1 @ di1 + np.block([[D1, np.zeros((3, 3))], [np.zeros((3, 3)), -D1]]) @ G1
       
    K1 = np.block([[-A1, np.zeros((3, 3))], [np.zeros((3, 3)), A1]]) @ G1 @ di1 @ np.linalg.inv(G1) + np.block([[D1, np.zeros((3, 3))], [np.zeros((3, 3)), -D1]])
        
        
    # Système 2
    
    A2 = np.array([
            [C55p * S, 0, 0],
            [0, C66p * Iy + C55p*Iz, -Iy*C16p],
            [0, -Iy*C16p, C11p * Iy]
        ])
    B2 = np.array([
            [0, 0, C55p*S*kz],
            [0, 0, 0],
            [-C55p*S*kz,0, 0]
        ])


    b_mat2 = np.block([
            [np.eye(3), np.zeros((3, 3))],
            [np.zeros((3, 3)), -A2]
        ])

        
    D2 = np.array([
            [0, 0, -C55p * S * kz],
            [0, 0, 0],
            [0, 0, 0]
        ])

       
    w2 = 2 * np.pi * f
    C2 = np.array([
                [rho * w2**2 * S, 0, 0],
                [0, rho * w2**2 * I0, 0],
                [0, 0, (rho * Iy * w2**2) - (C55p * S * kz)]
            ])
    a2 = np.block([
                [np.zeros((3, 3)), np.eye(3)],
                [C2, B2]
            ])
    Lb2, V2 = scipy.linalg.eig(a2, b_mat2)
            
           
    G02 = np.array([
                [V2[0,0],V2[0,1],V2[0,2],V2[0,3],V2[0,4],V2[0,5]],
                [V2[1,0],V2[1,1],V2[1,2],V2[1,3],V2[1,4],V2[1,5]],
                [V2[2,0],V2[2,1],V2[2,2],V2[2,3],V2[2,4],V2[2,5]]
                
                ])
            
            
    G_exp2 = np.array([
                [V2[0,0]* np.exp(Lb2[0] * L),V2[0,1]* np.exp(Lb2[1] * L),V2[0,2]* np.exp(Lb2[2] * L),V2[0,3]* np.exp(Lb2[3] * L),V2[0,4]* np.exp(Lb2[4] * L),V2[0,5]* np.exp(Lb2[5] * L)],
                [V2[1,0]* np.exp(Lb2[0] * L),V2[1,1]* np.exp(Lb2[1] * L),V2[1,2]* np.exp(Lb2[2] * L),V2[1,3]* np.exp(Lb2[3] * L),V2[1,4]* np.exp(Lb2[4] * L),V2[1,5]* np.exp(Lb2[5] * L)],
                [V2[2,0]* np.exp(Lb2[0] * L),V2[2,1]* np.exp(Lb2[1] * L),V2[2,2]* np.exp(Lb2[2] * L),V2[2,3]* np.exp(Lb2[3] * L),V2[2,4]* np.exp(Lb2[4] * L),V2[2,5]* np.exp(Lb2[5] * L)]
                
                ])
            
            
    di2=np.diag(Lb2)
            
    G2 = np.vstack([G02, G_exp2])
            
    H2=np.block([[-A2, np.zeros((3, 3))], [np.zeros((3, 3)), A2]])@ G2 @ di2 + np.block([[D2, np.zeros((3, 3))], [np.zeros((3, 3)), -D2]]) @ G2
            
    K_12 = np.block([[-A2, np.zeros((3, 3))], [np.zeros((3, 3)), A2]]) @ G2 @ di2@ np.linalg.inv(G2) 
    K_22 = np.block([[D2, np.zeros((3, 3))], [np.zeros((3, 3)), -D2]])
            
    K2 = K_12 + K_22
        
        
    # Matrice globale
        
    K_glob = np.zeros((12,12))    
        
    x1 = [0,1,5,6,7,11]
    x2 = [2,3,4,8,9,10]
    
    for i in range(6) :
        
        for j in range(6) :
        
            K_glob[x1[i],x1[j]] = K1[i,j]
            K_glob[x2[i],x2[j]] = K2[i,j]
        
        
    return K_glob
    


##########################################################################################################################################################################################
# MATRICE DE RIGIDITE MULTICOUHE
##########################################################################################################################################################################################


def Matrice_de_rigidite_multi(P,f) :
    
    
    L = P.L
    w = 2 * np.pi * f
    
    # Système1
    
    A1 = P.A1
    
    B1 = P.B1


    b_mat1 = np.block([
        [np.eye(3), np.zeros((3, 3))],
        [np.zeros((3, 3)), -A1]
    ])

    
    D1 = P.D1


    C1 = np.zeros((3,3))
    
    for i in P.Liste :
        
        C1 = C1 + np.array([
              [i.rho * (w**2) * i.b*i.h, 0, 0],
              [0, i.rho * (w**2) * i.b*i.h, 0],
              [0, 0, i.rho * i.Iz * (w**2) - i.C66p * i.b*i.h * i.ky]
              ])
          
      
    
    a1 = np.block([
            [np.zeros((3, 3)), np.eye(3)],
            [C1, B1]
        ])
    Lb1, V1 = scipy.linalg.eig(a1, b_mat1)

    
    G01 = np.array([
            [V1[0,0],V1[0,1],V1[0,2],V1[0,3],V1[0,4],V1[0,5]],
            [V1[1,0],V1[1,1],V1[1,2],V1[1,3],V1[1,4],V1[1,5]],
            [V1[2,0],V1[2,1],V1[2,2],V1[2,3],V1[2,4],V1[2,5]]
            
            ])
        
    G_exp1 = np.array([
            [V1[0,0]* np.exp(Lb1[0] * L),V1[0,1]* np.exp(Lb1[1] * L),V1[0,2]* np.exp(Lb1[2] * L),V1[0,3]* np.exp(Lb1[3] * L),V1[0,4]* np.exp(Lb1[4] * L),V1[0,5]* np.exp(Lb1[5] * L)],
            [V1[1,0]* np.exp(Lb1[0] * L),V1[1,1]* np.exp(Lb1[1] * L),V1[1,2]* np.exp(Lb1[2] * L),V1[1,3]* np.exp(Lb1[3] * L),V1[1,4]* np.exp(Lb1[4] * L),V1[1,5]* np.exp(Lb1[5] * L)],
            [V1[2,0]* np.exp(Lb1[0] * L),V1[2,1]* np.exp(Lb1[1] * L),V1[2,2]* np.exp(Lb1[2] * L),V1[2,3]* np.exp(Lb1[3] * L),V1[2,4]* np.exp(Lb1[4] * L),V1[2,5]* np.exp(Lb1[5] * L)]
            
            ])
        
        
    di1=np.diag(Lb1)
        
    G1 = np.vstack([G01, G_exp1])
        
        
    H1=np.block([[-A1, np.zeros((3, 3))], [np.zeros((3, 3)), A1]])@ G1 @ di1 + np.block([[D1, np.zeros((3, 3))], [np.zeros((3, 3)), -D1]]) @ G1
       
    K1 = np.block([[-A1, np.zeros((3, 3))], [np.zeros((3, 3)), A1]]) @ G1 @ di1 @ np.linalg.inv(G1) + np.block([[D1, np.zeros((3, 3))], [np.zeros((3, 3)), -D1]])
        
        
    # Système 2
    
    A2 = P.A2
    
    B2 = P.B2
    


    b_mat2 = np.block([
            [np.eye(3), np.zeros((3, 3))],
            [np.zeros((3, 3)), -A2]
        ])

        
    D2 = P.D2
    

       
    C2 = np.zeros((3,3))
    
    for i in P.Liste :
        
        C2 = C2 + np.array([
                [i.rho * (w**2) * i.h*i.b, 0, 0],
                [0, i.rho * (w**2) * i.I0, 0],
                [0, 0, (i.rho * i.Iy * (w**2)) - (i.C55p * i.h*i.b * i.kz)]
            ])
    
    
    
    
    a2 = np.block([
                [np.zeros((3, 3)), np.eye(3)],
                [C2, B2]
            ])
    Lb2, V2 = scipy.linalg.eig(a2, b_mat2)
            
           
    G02 = np.array([
                [V2[0,0],V2[0,1],V2[0,2],V2[0,3],V2[0,4],V2[0,5]],
                [V2[1,0],V2[1,1],V2[1,2],V2[1,3],V2[1,4],V2[1,5]],
                [V2[2,0],V2[2,1],V2[2,2],V2[2,3],V2[2,4],V2[2,5]]
                
                ])
            
            
    G_exp2 = np.array([
                [V2[0,0]* np.exp(Lb2[0] * L),V2[0,1]* np.exp(Lb2[1] * L),V2[0,2]* np.exp(Lb2[2] * L),V2[0,3]* np.exp(Lb2[3] * L),V2[0,4]* np.exp(Lb2[4] * L),V2[0,5]* np.exp(Lb2[5] * L)],
                [V2[1,0]* np.exp(Lb2[0] * L),V2[1,1]* np.exp(Lb2[1] * L),V2[1,2]* np.exp(Lb2[2] * L),V2[1,3]* np.exp(Lb2[3] * L),V2[1,4]* np.exp(Lb2[4] * L),V2[1,5]* np.exp(Lb2[5] * L)],
                [V2[2,0]* np.exp(Lb2[0] * L),V2[2,1]* np.exp(Lb2[1] * L),V2[2,2]* np.exp(Lb2[2] * L),V2[2,3]* np.exp(Lb2[3] * L),V2[2,4]* np.exp(Lb2[4] * L),V2[2,5]* np.exp(Lb2[5] * L)]
                
                ])
            
            
    di2=np.diag(Lb2)
            
    G2 = np.vstack([G02, G_exp2])
            
    H2=np.block([[-A2, np.zeros((3, 3))], [np.zeros((3, 3)), A2]])@ G2 @ di2 + np.block([[D2, np.zeros((3, 3))], [np.zeros((3, 3)), -D2]]) @ G2
            
    K_12 = np.block([[-A2, np.zeros((3, 3))], [np.zeros((3, 3)), A2]]) @ G2 @ di2@ np.linalg.inv(G2) 
    K_22 = np.block([[D2, np.zeros((3, 3))], [np.zeros((3, 3)), -D2]])
            
    K2 = K_12 + K_22
        
        
    # Matrice globale
        
    K_glob = np.zeros((12,12))    
        
    x1 = [0,1,5,6,7,11]
    x2 = [2,3,4,8,9,10]
    
    for i in range(6) :
        
        for j in range(6) :
        
            K_glob[x1[i],x1[j]] = K1[i,j]
            K_glob[x2[i],x2[j]] = K2[i,j]
        
        
    return K_glob



##########################################################################################################################################################################################
# LAYERS
##########################################################################################################################################################################################


def Layers(L) :
    
    N = len(L)
    
    longueur_totale = sum(L)
   
    origine = longueur_totale / 2
    

    position_actuelle = 0
   
    abscisses = [position_actuelle - origine]
    
    for reel in L:
 
        position_actuelle += reel
   
        abscisses.append(position_actuelle - origine)
    
    return abscisses





##########################################################################################################################################################################################
##########################################################################################################################################################################################  
##########################################################################################################################################################################################
# CLASSES
##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################


##########################################################################################################################################################################################
# MATERIAU ISOTROPE 
##########################################################################################################################################################################################

class isotropic_material :
    
    def __init__(self,E,G,nu,rho) :
        self.E = E
        self.G = G
        self.nu = nu
        self.rho = rho
        
        
##########################################################################################################################################################################################        
# MATERIAU ORTHOTROPE 
##########################################################################################################################################################################################       


class orthotropic_material :
    
    def __init__(self,E_1,E_2,E_3,G_12,G_13,G_23,nu_12,nu_13,nu_23,rho) :

        self.E_1 = E_1
        self.E_2 = E_2
        self.E_3 = E_3

        self.G_12 = G_12
        self.G_13 = G_13
        self.G_23 = G_23

        self.nu_12 = nu_12
        self.nu_13 = nu_13
        self.nu_23 = nu_23
        
        self.nu_21 = self.E_2 * self.nu_12 / E_1
        self.nu_31 = self.E_3 * self.nu_13 / E_1
        self.nu_32 = self.E_3 * self.nu_23 / E_2

        self.rho = rho
        

##########################################################################################################################################################################################      
# COUCHE 
##########################################################################################################################################################################################        
     

class layer :
    
    def __init__(self,b,h,zi,zj,E_1,E_2,E_3,G_12,G_13,G_23,nu_12,nu_13,nu_23,rho,alpha,ky,kz) :
        
        
        self.b = b
        
        self.zi = zi
        self.zj = zj
        
        self.h = h

        self.E_1 = E_1
        self.E_2 = E_2
        self.E_3 = E_3

        self.G_12 = G_12
        self.G_13 = G_13
        self.G_23 = G_23

        self.nu_12 = nu_12
        self.nu_13 = nu_13
        self.nu_23 = nu_23
        
        self.nu_21 = self.E_2 * self.nu_12 / E_1
        self.nu_31 = self.E_3 * self.nu_13 / E_1
        self.nu_32 = self.E_3 * self.nu_23 / E_2

        self.rho = rho
        self.alpha = alpha
        
        S = b * h
        
        Iz = (b**3)*h/12
        Iy = (b*(h**3)/12) + S*((self.zi + self.zj)**2)/4
        
        I0 = Iy + Iz
        
        self.ky = ky
        self.kz = kz
        
        self.Iz = Iz
        self.Iy = Iy
        self.I0 = I0
        

        
        s = np.array([
            [1 / E_1, -nu_12 / E_1, -nu_13 / E_1, 0, 0, 0],
            [-nu_12 / E_1, 1 / E_2, -nu_23 / E_2, 0, 0, 0],
            [-nu_13 / E_1, -nu_23 / E_2, 1 / E_3, 0, 0, 0],
            [0, 0, 0, 1 / G_23, 0, 0],
            [0, 0, 0, 0, 1 / G_13, 0],
            [0, 0, 0, 0, 0, 1 / G_12]
        ])

        cos_alpha = np.cos(alpha)
        sin_alpha = np.sin(alpha)
        cos_2alpha = np.cos(2 * alpha)
        sin_2alpha = np.sin(2 * alpha)

        S11p = (s[0, 0] * cos_alpha**4 + s[1, 1] * sin_alpha**4 +
                2 * s[0, 1] * sin_alpha**2 * cos_alpha**2 + s[5, 5] * sin_alpha**2 * cos_alpha**2)
        S16p = (-s[0, 0] * np.sin(2 * alpha) * cos_alpha**2 + s[0, 1] * np.sin(2 * alpha) * cos_2alpha +
                s[1, 1] * np.sin(2 * alpha) * sin_alpha**2 + s[5, 5] * sin_alpha * cos_alpha * cos_2alpha)
        S55p = s[3, 3] * sin_alpha**2 + s[4, 4] * cos_alpha**2
        S66p = (s[0, 0] * np.sin(2 * alpha)**2 + s[1, 1] * np.sin(2 * alpha)**2 -
                2 * s[0, 1] * np.sin(2 * alpha)**2 + s[5, 5] * np.cos(2 * alpha)**2)

        C11p = S66p / (S11p * S66p - S16p**2)
        C55p = 1 / S55p
        C66p = S11p / (S11p * S66p - S16p**2)
        C16p = S16p / (S11p * S66p - S16p**2)
        
        self.C11p = C11p
        self.C55p = C55p
        self.C66p = C66p
        self.C16p = C16p
        
  
        
        self.A1 = np.array([
            [C11p * S, C16p * S * ky, 0],
            [C16p * S * ky, C66p * S * ky, 0],
            [0, 0, C11p * Iz]
        ])
        
     
          
        self.B1 = np.array([
            [0, 0, -C16p * S * ky],
            [0, 0, -C66p * S * ky],
            [C16p * S * ky, C66p * S * ky, 0]
        ])
        
        
        
        self.D1 = np.array([
            [0, 0, C16p * S * ky],
            [0, 0, C66p * S * ky],
            [0, 0, 0]
        ])
        
        
        
        self.A2 = np.array([
                [C55p * S, 0, 0],
                [0, C66p * Iy + C55p*Iz, -Iy*C16p],
                [0, -Iy*C16p, C11p * Iy]
            ])
        
    
        
        self.B2 = np.array([
                [0, 0, C55p*S*kz],
                [0, 0, 0],
                [-C55p*S*kz,0, 0]
            ])
            
    
        self.D2 = np.array([
                [0, 0, -C55p * S * kz],
                [0, 0, 0],
                [0, 0, 0]
            ])
            


##########################################################################################################################################################################################      
# POUTRE ISOTROPE 
##########################################################################################################################################################################################


class isotropic_beam :
    
    def __init__(self,L,b,h,alpha,J,materiau) :
        
        self.L = L
        self.b = b
        self.h = h
        
        self.alpha = alpha
        
        self.Iy = self.h * (self.b**3) / 12
        self.Iz = self.b * (self.h**3) / 12
        
        self.J = J
        
        self.materiau = materiau
        
        self.m = self.b * self.h * self.L * self.materiau.rho
                
        
    ## FONCTIONS ##
    
    def bending_response(self,f0,fn) :
        
        frq = np.arange(f0, fn)
        
        response = []
        
        F = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
        
        for i in frq :
              
            U = np.linalg.solve(Matrice_de_rigidite_iso(self,i), F)
            
            response.append(U[1])
            
        plt.plot(frq, 20 * np.log10(np.abs(response)),label='bending')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Response')
        plt.title('bending_response')
        plt.grid(True)
        plt.legend()
        plt.show()
        
    def torsion_response(self,f0,fn) :
        
        frq = np.arange(f0, fn)
        
        response = []
        
        F = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
        
        for i in frq :
              
            U = np.linalg.solve(Matrice_de_rigidite_iso(self,i), F)
            
            response.append(U[4])
            
        plt.plot(frq, 20 * np.log10(np.abs(response)),label='torsion')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Response')
        plt.title('torsion_response')
        plt.grid(True)
        plt.legend()
        plt.show()
    
    def tension_response(self,f0,fn) :
        
        frq = np.arange(f0, fn)
        
        response = []
        
        F = np.array([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
        
        for i in frq :
              
            U = np.linalg.solve(Matrice_de_rigidite_iso(self,i), F)
            
            response.append(U[0])
            
        plt.plot(frq, 20 * np.log10(np.abs(response)),label='tension')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Response')
        plt.title('tension_response')
        plt.grid(True)
        plt.legend()
        plt.show()
        
    def compression_response(self,f0,fn) :
        
        frq = np.arange(f0, fn)
        
        response = []
        
        F = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
        
        for i in frq :
              
            U = np.linalg.solve(Matrice_de_rigidite_iso(self,i), F)
            
            response.append(U[0])
            
        plt.plot(frq, 20 * np.log10(np.abs(response)),label='compression')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Response')
        plt.title('compression_response')
        plt.grid(True)
        plt.legend()
        plt.show()
        
    def loading_response(self,f0,fn,F,N) :
        
        frq = np.arange(f0, fn)
        
        response = []
        
        for i in frq :
            
            U = np.linalg.solve(Matrice_de_rigidite_iso(self,i), F)
            
            response.append(U[N])
            
        plt.plot(frq, 20 * np.log10(np.abs(response)),label='response')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Response')
        plt.title('loading_response')
        plt.grid(True)
        plt.legend()
        plt.show()
        

        
##########################################################################################################################################################################################
# POUTRE ORTHOTROPE 
##########################################################################################################################################################################################


class orthotropic_beam :
    
    def __init__(self,L,b,h,alpha,ky,kz,materiau) :
        
        self.L = L
        self.b = b
        self.h = h
        
        self.alpha = alpha
        
        self.Iy = self.h * (self.b**3) / 12
        self.Iz = self.b * (self.h**3) / 12
        
        
        self.ky = ky
        self.kz = kz
        
        self.materiau = materiau
        
        
    ## FONCTIONS ##
     
    def bending_response(self,f0,fn) :
         
         frq = np.arange(f0, fn)
         
         response = []
         
         F = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
         
         for i in frq :
               
             U = np.linalg.solve(Matrice_de_rigidite_ortho(self,i), F)
             
             response.append(U[1])
             
         plt.plot(frq, 20 * np.log10(np.abs(response)),label='bending')
         plt.xlabel('Frequency (Hz)')
         plt.ylabel('Response')
         plt.title('bending_response')
         plt.grid(True)
         plt.legend()
         plt.show()
             
             
         
    def torsion_response(self,f0,fn) :
         
         frq = np.arange(f0, fn)
         
         response = []
         
         F = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
         
         for i in frq :
             
             U = np.linalg.solve(Matrice_de_rigidite_ortho(self,i), F)
             
             response.append(U[3])
             
         plt.plot(frq, 20 * np.log10(np.abs(response)),label='torsion')
         plt.xlabel('Frequency (Hz)')
         plt.ylabel('Response')
         plt.title('torsion_response')
         plt.grid(True)
         plt.legend()
         plt.show()
     
    def tension_response(self,f0,fn) :
         
         frq = np.arange(f0, fn)
         
         response = []
         
         F = np.array([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
         
         for i in frq :
             
             U = np.linalg.solve(Matrice_de_rigidite_ortho(self,i), F)
             
             response.append(U[0])
             
         plt.plot(frq, 20 * np.log10(np.abs(response)),label='tension')
         plt.xlabel('Frequency (Hz)')
         plt.ylabel('Response')
         plt.title('tension_response')
         plt.grid(True)
         plt.legend()
         plt.show()
         
    def compression_response(self,f0,fn) :
         
         frq = np.arange(f0, fn)
         
         response = []
         
         F = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
         
         for i in frq :
             
             U = np.linalg.solve(Matrice_de_rigidite_ortho(self,i), F)
             
             response.append(U[0])
             
         plt.plot(frq, 20 * np.log10(np.abs(response)),label='compression')
         plt.xlabel('Frequency (Hz)')
         plt.ylabel('Response')
         plt.title('compression_response')
         plt.grid(True)
         plt.legend()
         plt.show()
         
    def loading_response(self,f0,fn,F,N) :
         
         frq = np.arange(f0, fn)
         
         response = []
         
         for i in frq :
             
             U = np.linalg.solve(Matrice_de_rigidite_ortho(self,i), F)
             
             response.append(U[N])
             
         plt.plot(frq, 20 * np.log10(np.abs(response)),label='response')
         plt.xlabel('Frequency (Hz)')
         plt.ylabel('Response')
         plt.title('loading_response')
         plt.grid(True)
         plt.legend()
         plt.show()
         
 
##########################################################################################################################################################################################      
# POUTRE MULTICOUCHE
##########################################################################################################################################################################################         
         
       
         
class multilayer_beam :
     
     def __init__(self,L,Liste) :
         
         self.L = L
         self.Liste = Liste
         
         self.A1 = np.zeros((3,3))
         
         self.A2 = np.zeros((3,3))
         
         
         self.B1 = np.zeros((3,3))
         
         self.B2 = np.zeros((3,3))
         
         
         self.C1 = np.zeros((3,3))
         
         self.C2 = np.zeros((3,3))
         
         
         self.D1 = np.zeros((3,3))
         
         self.D2 = np.zeros((3,3))
         
         
         
         
         for a in Liste :
             
         
             self.A1 = self.A1 + a.A1
             
             self.A2 = self.A2 + a.A2
             
             
             self.B1 = self.B1 + a.B1
             
             self.B2 = self.B2 + a.B2
             
             
             self.D1 = self.D1 + a.D1
             
             self.D2 = self.D2 + a.D2
                  
         
     ## FONCTIONS ##
      
     def bending_response(self,f0,fn) :
          
          frq = np.arange(f0, fn)
          
          response = []
          
          F = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
          
          for i in frq :
                
              U = np.linalg.solve(Matrice_de_rigidite_multi(self,i), F)
              
              response.append(U[1])
              
          plt.plot(frq, 20 * np.log10(np.abs(response)),label='bending')
          plt.xlabel('Frequency (Hz)')
          plt.ylabel('Response')
          plt.title('bending_response')
          plt.grid(True)
          plt.legend()
          plt.show()
              
              
          
     def torsion_response(self,f0,fn) :
          
          frq = np.arange(f0, fn)
          
          response = []
          
          F = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
          
          for i in frq :
              
              U = np.linalg.solve(Matrice_de_rigidite_multi(self,i), F)
              
              response.append(U[3])
              
          plt.plot(frq, 20 * np.log10(np.abs(response)),label='torsion')
          plt.xlabel('Frequency (Hz)')
          plt.ylabel('Response')
          plt.title('torsion_response')
          plt.grid(True)
          plt.legend()
          plt.show()
      
     def tension_response(self,f0,fn) :
          
          frq = np.arange(f0, fn)
          
          response = []
          
          F = np.array([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
          
          for i in frq :
              
              U = np.linalg.solve(Matrice_de_rigidite_multi(self,i), F)
              
              response.append(U[0])
              
          plt.plot(frq, 20 * np.log10(np.abs(response)),label='tension')
          plt.xlabel('Frequency (Hz)')
          plt.ylabel('Response')
          plt.title('tension_response')
          plt.grid(True)
          plt.legend()
          plt.show()
          
     def compression_response(self,f0,fn) :
          
          frq = np.arange(f0, fn)
          
          response = []
          
          F = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1)
          
          for i in frq :
              
              U = np.linalg.solve(Matrice_de_rigidite_multi(self,i), F)
              
              response.append(U[0])
              
          plt.plot(frq, 20 * np.log10(np.abs(response)),label='compression')
          plt.xlabel('Frequency (Hz)')
          plt.ylabel('Response')
          plt.title('compression_response')
          plt.grid(True)
          plt.legend()
          plt.show()
          
     def loading_response(self,f0,fn,F,N) :
          
          frq = np.arange(f0, fn)
          
          response = []
          
          for i in frq :
              
              U = np.linalg.solve(Matrice_de_rigidite_multi(self,i), F)
              
              response.append(U[N])
              
          plt.plot(frq, 20 * np.log10(np.abs(response)),label='response')
          plt.xlabel('Frequency (Hz)')
          plt.ylabel('Response')
          plt.title('loading_response')
          plt.grid(True)
          plt.legend()
          plt.show()      
        
       
##########################################################################################################################################################################################
##########################################################################################################################################################################################  
##########################################################################################################################################################################################
# END
##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################


