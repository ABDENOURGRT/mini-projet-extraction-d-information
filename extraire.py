

import http.client
import re,os

os.system("cls")

port = 80 # Port Par Defaut de PROTOCOLE HTTP 

print("[?][+]===================================================[+]\n\n\
      {+} Donner L\'interrvalle des Pages a Aspirer ? {+} \n\n\
                + Format de Intervallle :  [A-Z]-[A-Z] \n\
                    [!] Exemple : A-I , D-X \n\n\
     {+} Donner Un Port de Protocole  HTTP {+} \n \n\
                + Port Par defaut est 80\n\
                + Intervalle des Port Auttorise : [0-1023]\n\t\t    [!] Exemple : 800,1000\
                \n\n[+]===================================================[?][+]\
                \n\n\n")

accepte = False            # Boolean Pour Le Bien Saiser   
while accepte is False :   # Revien Si L'Intervalle Saiser Erroe 
    ch = input("> Intervalle des Pages  :").upper()  # lire l'intervalle 
    if re.search('^[A-Z]-[A-Z]$', ch):
        if (ord(ch[0]) <= ord(ch[2])):
            accepte = True      # L'ordre est vari  Exp : [A < B] = [65 < 66]
        else:                   # Pas Bon Ordre [B < A] = [66 < 65] qui faux 
            print('\t\t [!] INTERVAL ERREUR [!] \n\n')
    else:                       # dans le cas 1 - 9 ou $ - X
        print('\t\t  [!] FORMAT ERREUR [!]\n\n')

os.system("pause")
os.system("cls")
# Saisier le port le Selon le choix de user (port par defaut est 80)

print("[?][+]===================================================[+]\n\n\
      {+} Vous voulez entrer votre port de protocole HTTP ? {+} \n\n\
                + Port Par defaut 80\n\
                + Intervalle des Port Auttorise : [80-1000]\n \
                +La Reponse : 1 ==> OUI | 0 ==> NON   \n \
                \n\n[+]===================================================[?][+]\
                \n\n\n ")

## Lire le Numero de Port Si Le Utilisateur Voules le Saiser 

if (int(input(" > Je Decide de  : ")) == 1):
    os.system("pause")
    os.system("cls")

    try : 
        port = int(input("\n\t > Saisir le Port :  \t\n"))
    except ValueError :
        port=80
    finally:
        print("\n\t[!][!] Le serveur écoute à présent sur le port {} [!][!]".format(port) + "\n\t")
os.system("pause")
os.system("cls")


fich1 = open("subst.dic", "w", encoding='utf-16-le') # OUVERTEUR De fichier avec encodage UTF-16 LITTLE ENDIEN 
fich1.write('\ufeff') # Ecriteur de le BOM de LITTLE ENDIENE [FE FF] 2octet 

fich2 = open("info.txt", "w",encoding='utf-8')  # ouverteur de ficheir en mode ecriteur 

debut,fin,nb1 = ord(ch[0]),ord(ch[2]),0

print(f"\n\n\t\t[+]====================[    L'intervalle: [{chr(debut)} - {chr(fin)}]    ]====================[+]\t\t\n\n")
while (debut <= fin):
    
    link = f"/vidal/vidal-Sommaires-Substances-{chr(debut)}.htm"
    try :
        connection =  http.client.HTTPConnection(f"localhost:{port}")
        connection.request('GET',link)
        data = connection.getresponse().readlines()
    except ConnectionRefusedError as e : 
        data=""
        print("[+]====================[   Error de connection au local server   ]====================[+]\n\t[+] Verife le Port Entre esq disponible\n\t[+] Verifie le server local esq elle en mode run\n\n")
        exit(1)

    except ConnectionError as e:
          data=""
          print("[+]====================[   Error de connection au local server   ]====================[+]\n\t[+] ReEssaye Un Autre fois et verife que le server local est lancer")
        
   
    nb2 = 0
    for y in data:  # les subtances
        sub = re.search("Substance/(\w[\s\d]?)+-\d+\.htm\">((\w[')(\s\d-]{0,2})+)<", y.decode('utf-8')) # decodage parcque elle est crybte sur net
        if sub != None:
            fich1.write(f"{sub.group(2)},.N+subst\n")
            nb2 = nb2 + 1
    fich2.write(
        f"\nLe nombre des médicament par substance active commençant par {chr(debut)} : {nb2}")
    nb1 = nb1 + nb2
    debut = debut + 1

print("\n\t\t[+]===================={      Aspiration terminée    }====================[+]")
fich2.write(f"\nLe nombre totale de médicament par substance active : {nb1}")
fich1.close()
fich2.close()
