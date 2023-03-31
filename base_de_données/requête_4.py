#!usr/bin/env python3
#-*- coding: utf-8 -*-

# bdd bar a 4 tables : Employes , Etablissement, Carte, Ventes

"""Le script affiche 5 boissons les moins vendues dans l’établissement ce mois-ci
et les employés ayant vendu le moins de boissons. On compose la date à partir du mois saisi par l'utilisateur.
On affiche une erreur en cas de données non-disponibles ou si le mois a été saisi au mauvais format.
"""

import csv
import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()
bdd.text_factory = str # pour éviter les erreurs d'encodage

# On définit l'année, puisque la BDD ne contient les données que pour 2022
year = '2022'
list_least_profit = []

# On vérifie le format de la saisie du mois dans le terminal
def get_mois(mois):
    if mois.isdigit(): 
        if int(mois)>= 1 and int(mois) <= 12:
            if len(mois) < 2:
                mois = '0' + mois
            return mois
    else:
        print("Veuillez saisir le mois au bon format: (entre 1 et 12).")
        return False

# création d'une liste des matricules des managers pour ne donner l'accès qu'aux managers
managers_request = cursor.execute("SELECT manager_id FROM Etablissement").fetchall()
managers_list = [i[0] for i in managers_request]

# pour tester le programme, sinon donne accès à tout le monde
print(managers_list)

# On récupère le matricule de l'employé
user = input("Bonjour, saisissez votre matricule, s'il vous plaît: ")


# On récupère le nom du bar du manager
bar = cursor.execute('SELECT name FROM Etablissement WHERE manager_id == ?', (user,)).fetchone()


# Boissons qui rapportent le moins
if user in managers_list:
    mois = input("Bonjour, saisissez un mois (entre 1 et 12) pour lequel vous souhaitez des informations, s'il vous plaît.\n")
    month = get_mois(mois)
    if month != False:
        date = '__/' + month + '/' + year
        least_profit = cursor.execute("""SELECT COUNT(boisson_id) AS sum_sales, id_boisson, Carte.nom
                                    FROM Employes, Ventes, Carte
                                    WHERE matricule = employe_id AND nom_bar = ? AND id_boisson = boisson_id
                                    GROUP BY nom_bar, id_boisson HAVING date LIKE ? 
                                    ORDER BY sum_sales LIMIT 5;""", (bar[0], date))
        for line in least_profit:
            list_least_profit.append(line)                          
        # affichage les 5 boissons les moins vendues    
        if len(list_least_profit) == 0 :  
            print("Désolé, pas de données disponibles pour le mois saisi.")
        else:          
            counter = 1
            for ligne in least_profit:
                print(f" Boisson {counter} la moins vendue est la numéro {ligne[1]}, {ligne[2]}")
                counter +=1

    # 5 employés qui ont vendu le moins de boissons ce mois-ci
        least_sold = cursor.execute(""" SELECT prenom, Employes.nom, COUNT(id_boisson) as count 
                                    FROM Employes, Ventes, Carte, Etablissement
                                    WHERE matricule = employe_id AND nom_bar = ? AND id_boisson = boisson_id
                                    AND Etablissement.name = Employes.nom_bar
                                    GROUP BY matricule HAVING date LIKE ? 
                                    ORDER BY count LIMIT 5; """, (bar[0], date))

        for ligne in least_sold:
            print(f"{ligne[0]} {ligne[1]} a vendu {ligne[2]} boissons")
        
else:
    # Le matricule ne correspond pas à celui d'un manager
    print("Désolé, vous n'avez pas accès à ces informations.")

bdd.close()            
