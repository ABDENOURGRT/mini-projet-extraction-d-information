

""" 
Creation d'un base de donnes en extron des POSOLOGIE d'apre la page web 
"""
import re,os
import sqlite3
f = open("corpus-medical_snt/concord.html", 'r', encoding='utf-8')
data = f.readlines()
expreg = "(&nbsp;)?<a href=\"[\d| ]+\">(.+)</a>(&nbsp;)?"

# extrai les token sans apres supprime les dubliqate et enumer la liste des token
idf_tokens = [(idf, token) for idf, token in enumerate(list(set([(re.search(expreg, i.rstrip())).group(2)
                                                                 for i in data if re.search(expreg, i.rstrip()) != None])))]
f.close()   # Ferme le fichier

try :
	os.remove("extraction.db")
except FileNotFoundError :
	pass	# sa pas pose des problem dans la creation de nouvelle fichier .db 

db = sqlite3.connect("extraction.db")  # connection a la BD
connection = db.cursor()
# Creation de Table
connection.execute(
    '''Create Table if not exists EXTRACTION(ID INTEGER PRIMARY KEY,POSOLOGIE VARCHAR2(100))''')

# Table des tokens extries est idf_tokens
# L'Ajoute des Tokens extrae d'apre page web a la table EXTRACTION
try:
    connection.executemany(
        'INSERT INTO EXTRACTION (ID,POSOLOGIE) values(?,?)', idf_tokens)
except sqlite3.Error as sqle:
    print(sqle)  # Here we solve the error of Integrite
finally:
    db.commit()  # Enregistre les donnes change au nivau de la BD
    db.close()  # arrite la connextion a BD
