import numpy as np
import copy
import time

#TROIS PETITES FONCTIONS DE TEST UTILISEES PLUS BAS#
def test(mess,eval,res):
    print(mess,(eval==res)*'OK'+(eval!=res)*'Try again')
def test_determine_valuations(mess,list_var,res):
    test=mess+'Ok'
    list_testee=determine_valuations(list_var)
    for el in list_testee :
        if el not in res:
            test=mess+'Try again'
            return test
    for el in res:
        if el not in list_testee :
            test=mess+'Try again'
            return test
    for i in range(len(list_testee)-1):
        if list_testee[i] in list_testee[i+1:]:
            test=mess+'wowowow y a du doublon là-dedans'
            return test
    return test  
    for el in res:
        if el not in list_testee :
            test=mess+'Try again'
            return test
    for i in range(len(list_testee)-1):
        if list_testee[i] in list_testee[i+1:]:
            test=mess+'wowowow y a du doublon là-dedans'
            return test
    return test  

def test_for(mess,formu,res_for):
    res=True
    if (formu==[] and res_for!=[]) or (formu!=[] and res_for==[]):
        res=False
    for el1 in formu:
        for el2 in res_for:
            res=(set(el1)==set(el2))
            if res :
                break
        if not res :
            print(mess+'Try again !')
            return
    for el2 in res_for:
        for el1 in formu:
            res=(set(el2)==set(el1))
            if res :
                break
        if not res :
            print(mess+'Try again !')
            return
    res=False
    for i in range(len(formu)-1):
        for el in formu[i+1:]:
            if set(formu[i])==set(el):
                print(mess+'wowowow y a du doublon là-dedans')
                return 
    print(mess+'Ok')
    
#A VOUS DE JOUER#

########### Partie 1 ###########

def get(v:int, l:list):
    assert(v>0)
    return l[v-1]

def evaluer_clause(clause, list_var):
    '''
    Arguments : une liste d'entiers non nuls traduisant une clause, une liste de booléens 
    informant de valeurs logiques connues (ou None dans le cas contraire) pour un ensemble 
    de variables
    Renvoie : None ou booléen
    '''
    result = False
    unknown = False

    if len(clause)<1 :
        return result
    
    for i in clause:
        var = get(abs(i), list_var) # sélection la variable correspondant à la clause (absolue)
        if var == None :            # si var inconnue (None) -> pas calculable -> pass
            unknown = True          # True si présance d'une var inconnue
        else :
            if i<0 : 
                var = not(var) # si clause negative -> inverse la valeur
            result = result or var  # calcul de la clause
        if result : 
            return result   # si un résultat True alors clause True
    
    if not(result) and unknown :  # si résultat False et présence d'une var inconnue donc potentiellement True alors result = None
        result = None
        return result

    return result
    
clause1=[1,-2,3,-4]
list_var1=[True,True,False,None]
test("essai cas 1 evaluer_clause : ",evaluer_clause(clause1,list_var1),True)
clause2=[1,-2,3,-4]
list_var2=[False,True,False,None]
test("essai cas 2 evaluer_clause : ",evaluer_clause(clause2,list_var2),None)
clause3=[1,-2,3,-4]
list_var3=[None,True,False,True]
test("essai cas 3 evaluer_clause : ",evaluer_clause(clause3,list_var3),None)
clause4=[1,-3]
list_var4=[False,False,True]
test("essai cas 4 evaluer_clause : ",evaluer_clause(clause4,list_var4),False)
clause5=[]
list_var5=[False,False,True]
test("essai cas 5 evaluer_clause : ",evaluer_clause(clause5,list_var5),False)
clause6=[1,2,3]
list_var6=[False,False,True]
test("essai cas 6 evaluer_clause : ",evaluer_clause(clause6,list_var6),True)

def evaluer_cnf(formule, list_var):
    '''
    Arguments : une liste de listes d'entiers non nuls traduisant une formule,une liste de booléens 
    informant de valeurs logiques connues (ou None dans le cas contraire) pour un ensemble de variables
    Renvoie : None ou booléen
    '''
    list_result = []                # stock résultat des clauses
    for i in formule:               # calculs des clauses
        list_result.append(evaluer_clause(i, list_var))
    
    result = True
    for i in list_result :
        if i != None : 
            result = result and i   # calcule de la formule
        else :
            result = None           # si clause inconnue alors incalculable
            return result

    return result 

for1=[[1,2],[2,-3,4],[-1,-2],[-1,-2,-3],[1]]
list_var_for1_test1=[True,False,False,None]
test('test1 evaluer_cnf : ',evaluer_cnf(for1,list_var_for1_test1),True)
list_var_for1_test2=[None,False,False,None]
test('test2 evaluer_cnf : ',evaluer_cnf(for1,list_var_for1_test2),None)
list_var_for1_test3=[True,False,True,False]
test('test3 evaluer_cnf : ',evaluer_cnf(for1,list_var_for1_test3),False)

def determine_valuations(list_var):
    '''Arguments : une liste de booléens informant de valeurs logiques connues 
    (ou None dans le cas contraire) pour un ensemble de variables
    Renvoie : La liste de toutes les valuations (sans doublon) envisageables pour les 
    variables de list_var
    '''
    # détermination des indices où l'on trouve None
    unknown = []
    for i in range(len(list_var)):
        if list_var[i] is None:
            unknown.append(i)

    # création des listes pour remplacer le None par True/False
    valuations = []
    boolen = [True, False]
    for j in range(2**len(unknown)):
        valuation = list_var.copy()
        for k in range(len(unknown)):
            valuation[unknown[k]] = boolen[(j >> k) & 1]
        valuations.append(valuation)

    return valuations

list_var1=[True,None,False,None]
print(test_determine_valuations('res_test_determine_valuations cas 1 : ',list_var1,[[True, True, False, True], [True, False, False, True], [True, True, False, False], [True, False, False, False]]))
list_var2=[None,False,True,None,True,False]
print(test_determine_valuations('res_test_determine_valuations cas 2 : ',list_var2,[[True, False, True, True, True, False], [False, False, True, True, True, False], [True, False, True, False, True, False], [False, False, True, False, True, False]]))
list_var3=[False,True,True,False]
print(test_determine_valuations('res_test_determine_valuations cas 3 : ',list_var3,[[False, True, True, False]]))
list_var4=[None,None,None]
print(test_determine_valuations('res_test_determine_valuations cas 4 : ',list_var4,[[True, True, True], [False, True, True], [True, False, True], [False, False, True], [True, True, False], [False, True, False], [True, False, False], [False, False, False]]))

def resol_sat_force_brute(formule, list_var):
    '''Arguments : une liste de listes d'entiers non nuls traduisant une formule,
                   une liste de booléens informant de valeurs logiques connues 
                   (ou None dans le cas contraire) pour un ensemble de variables
       Renvoie : SAT, l1
                 avec SAT : booléen indiquant la satisfiabilité de la formule
                       l1 : une liste de valuations rendant la formule vraie ou une liste vide
    '''
    valuations = determine_valuations(list_var)

    for val in valuations:
        is_satisfiable = evaluer_cnf(formule, val)
        if is_satisfiable:
            return True, val

    return False, []

for1=[[1,2],[2,-3,4],[-1,-2],[-1,-2,-3],[1],[-1,2,3]]
list_var_for1=[None,None,None,None]
test('test1 resol_sat_force_brute : ',resol_sat_force_brute(for1,list_var_for1),(True,[True, False, True, True]))

for2=[[1,4,-5],[-1,-5],[2,-3,5],[2,-4],[2,4,5],[-1,-2],[-1,2,-3],[-2,4,-5],[1,-2]]
list_var_for2=[None,None,None,None,None]
test('test2 resol_sat_force_brute : ',resol_sat_force_brute(for2,list_var_for2),(False,[]))

def enlever_litt_for(formule,litteral):
    '''Arguments :
    formule : comme précédemment
    litteral : un entier non nul traduisant la valeur logique prise par une variable
        Renvoie : la formule simplifiée
    '''
    simplified_formule = []

    for clause in formule:
        if litteral in clause:
            continue
        simplified_clause = [l for l in clause if -l != litteral]
        simplified_formule.append(simplified_clause)

    return simplified_formule
    
for1=[[1,2,4,-5],[-1,2,3,-4],[-1,-2,-5],[-3,4,5],[-2,3,4,5],[-4]]
litt1=4
test('essai cas 1 enlever_litt_for : ',enlever_litt_for(for1,litt1),[[-1, 2, 3], [-1, -2, -5], []])

def init_formule_simpl_for(formule_init,list_var):
    '''
    Renvoie : La formule simplifiée en tenant compte des valeurs logiques renseignées dans list_var
    '''
    formule_simpl = formule_init.copy()

    for i, lit in enumerate(list_var):
        if lit is not None:
            formule_simpl = enlever_litt_for(formule_simpl, i + 1 if lit else -(i + 1))

    return formule_simpl

list_var_for1=[False, None, None, False, None]
for1=[[-5, -3, 4, -1], [3], [5, -2], [-2, 1, -4], [1, -3]]
cor_for1=[[3], [5, -2], [-3]]
test_for('test1_init_formule_simpl_for : ',init_formule_simpl_for(for1,list_var_for1),cor_for1)

list_var_for2= [False, True, False, True, False]
for2= [[3, 2, 1], [-1, -2, 5]]
cor_for2=[]
test_for('test2_init_formule_simpl_for : ',init_formule_simpl_for(for2,list_var_for2),cor_for2)

list_var_for3= [None, None, None, True, None]
for3= [[-5, -1], [-1, -3], [4], [-4, 1], [-2, -1, 3]]
cor_for3=[[-5, -1], [-1, -3], [1], [-2, -1, 3]]
test_for('test3_init_formule_simpl_for : ',init_formule_simpl_for(for3,list_var_for3),cor_for3)

def retablir_for(formule_init,list_chgmts):
    '''Arguments : une formule initiale et une liste de changements à apporter sur un ensemble de variables (chaque changement étant une liste [i,bool] avec i l'index qu'occupe la variable dans list_var et bool la valeur logique qui doit lui être assignée) 
    Renvoie : la formule simplifiée en tenant compte de l'ensemble des changements
    '''
    formule_simpl = formule_init.copy()

    for chgmt in list_chgmts:
        index, valeur = chgmt
        formule_simpl = init_formule_simpl_for(formule_simpl, [None] * index + [valeur] + [None] * (len(formule_simpl[0]) - index - 1))

    return formule_simpl

formule_init=[[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]]
list_chgmts1=[[0, True], [1, True], [2, False]]
form1=[[-5], [4, 5], [-4, 5]]

list_chgmts2=[[0, True], [1, True], [2, False], [3, True], [4, False]]
form2=[[]]

list_chgmts3=[[0, True], [1, True], [2, False], [3, False]]
form3=[[-5], [5]]
test('essai cas 1 retablir_for : ',retablir_for(formule_init,list_chgmts1),form1)
test('essai cas 2 retablir_for : ',retablir_for(formule_init,list_chgmts2),form2)
test('essai cas 3 retablir_for : ',retablir_for(formule_init,list_chgmts3),form3)

########### Partie 2 ###########

