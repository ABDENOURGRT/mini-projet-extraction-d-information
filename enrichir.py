


import re,sys,os
def Extract(File1, File3):
    var = File1.readlines()
    tab = []
    for i in var:
        x = re.findall("^[-Ø]? ?(\w+) :? ?(((\d+|,|\.)+ ?(mg|ml|cp|sachet))|\d/?\d? ?/j)", i, re.I)
        for j in x:
            if tab != []:
                File3.write("\n")
            File3.write(str(j[0].lower()) + ",.N+subst")
            tab.append(str(j[0].lower()) + ",.N+subst")
    return tab
#############################################################################
def add_elt_queue(element, List):
    # Ajouter un saut de ligne a la fin du fichier de subst.dic
    List.append(List.pop() + '\n')
    List.append(elmt)
############################################################################
def add_elt(element, List, pos):
    tab = []
    x = len(List) - pos
    # Parcoure de la liste jusqu'à la postion d'insertion
    while x != 0:
        tab.append(List.pop())
        x = x - 1
    element = element + '\n'
    tab.append(element)
    x = len(tab)
    # Rendre les élements List a leur postion adequat
    while x != 0:
        List.append(tab.pop())
        x = x - 1
############################################################################
def Dispaly(elmt, counter):
    print( str(counter) + ')-  ' + elmt[:-9])
############################################################################
def Remplir(List,File,String):
    cpt_tot=0
    alph =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                          'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    F =open(File,'w', encoding='utf-16-le')
    
    for let in alph:
	    cpt_let = 0
	    for item in List:
		    strs = item.strip('\n')
		    if strs[0]==let.lower()  or strs[0]== 'é' and let.lower() == 'e':
			    cpt_let=cpt_let+1
	    cpt_tot=cpt_tot+cpt_let
	    F.write(f"\nLe nombre de medicaments par substance active {String} commencant par: {let}= {str(cpt_let)}\n")
    F.write(f"\n[+] Le nombre totale de medicaments par substance active {String} = {str(cpt_tot)}  [+]\n")  
    F.close()
#######################################################################
def Enrichment(File1, File2, File3):
    # initialisation des structures de données
    List1 = Extract(File1, File3)#la trace
    List2 = File2.readlines()#a enrichir
    n1,n2 = len(List1),len(List2)
    x1,x2,cpt = 0,0,0
    Remplir(List1,"info2.txt","issus de corpus")
    t=[]
    while x2 < n2:
        t.append(List2.pop().replace('é','e'))
        x2 += 1
    x2=0
    while x2 < n2:
        List2.append(t.pop())
        x2 += 1
    x2 =0    

    # Trie par insertion et supprission des doublons
    while x1 < n1:#boucler la trace
        # Affichage des médicaments issus decorpus et issus de l’enrichissement
        cpt = cpt + 1
        #Dispaly(List1[x1], cpt)
        List1[x1].replace('é','e')
        # Chercher la position d'insertion si c'est pas un doublon
        while x2 < n2 and List1[x1].rstrip() > List2[x2].rstrip():
            x2 +=1
        # Ajout a la fin de la liste List2
        if x2 == n2:
            add_elt_queue(List1[x1], List2)
        # Sinon l'ajout nest pas a la fin
        else:
            # Ne pas ajouter les médicaments doublons dans subst.dic
            if List1[x1].rstrip() < List2[x2].rstrip():
                add_elt(List1[x1], List2, x2)
        x2,n2= 0,len(List2)
        x1 +=1
    Remplir(List2,"info3.txt","issus de l'enrichissement")
    return List2
##################################################################################
def main():
    # ouverture des fichiers
    try:
        File1 = open(sys.argv[1], "r",encoding="utf-8")
        try:
            File2 = open("subst.dic", "r", encoding='utf-16-le')
           
            try:
                File3 = open("subst_enri.dic", "w", encoding='utf-16-le')
                File3.write('\ufeff')
                res = Enrichment(File1, File2, File3)
                File4 = open("subst.dic", "w", encoding='utf-16-le')
                File4.write('\ufeff')
                for x in res:
                    File4.write(x)
                File1.close()
                File2.close()
                File3.close()
                File4.close()
            except IOError:
                print("\n\t\t [!] Erreur espace mémoire inufusant [!] \t\t\n")
                exit()
        except FileNotFoundError:
            print("\n\t\t [!] Erreur: Le fichier subst.dic n'existe pas [!]\t\t\n")
            exit()
    except FileNotFoundError:
        print("\n\t\t [!] Erreur: Le fichier corpus-medical.txt n'existe pas [!]\n\t\t[+] passe Le fichier corpus-medical.txt 1er argument [+]\n")
        exit()
    except IndexError:
        print("\n\t\t [!] Erreur: Le fichier corpus-medical.txt n'existe pas [!]\n\t\t[+] passe Le fichier corpus-medical.txt 1er argument [+]\n")
        exit()
###########################################################################
if __name__ == '__main__':
    main()
