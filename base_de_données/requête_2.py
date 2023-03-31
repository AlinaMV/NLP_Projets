#!usr/bin/env python3
# -*- coding: utf-8 -*-

# La BDD bar a 4 tables : Employes , Etablissement, Carte, Ventes

""" Le script donne à chaque manager la possibilité d’afficher le nombre de ventes
effectuées ce mois-ci par ses employés et le montant que cela représente,
ainsi que le bénéfice généré pour chaque employé du bar."""

import csv
import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor() 
bdd.text_factory = str  # pour éviter les erreurs d'encodage

# On récupère la matricule de l'employé
user = input("Bonjour, saisissez votre matricule, s'il vous plaît.\n")

# On crée une liste des matricules des managers pour ne donner l'accès qu'aux managers
managers_request = cursor.execute("SELECT manager_id FROM Etablissement").fetchall()
managers_list = [i[0] for i in managers_request]

# si on souhaite récupérer la liste des matricules des managers, afin de tester le programme :
# print(managers_list)

# On récupère le nom du bar du manager
bar = cursor.execute('SELECT name FROM Etablissement WHERE manager_id == ?', (user,)).fetchone()

if user in managers_list:
    nb_ventes = cursor.execute("""SELECT nom_bar, COUNT(*) FROM Employes, Ventes
                       WHERE matricule = employe_id AND nom_bar = ? 
                       GROUP BY nom_bar HAVING date LIKE '__/11/2022'""", (bar[0],)).fetchone()
    print(f"Le nombre de ventes dans le bar {nb_ventes[0]} = {nb_ventes[1]}")
    montant_total = cursor.execute("""SELECT SUM(prix) FROM Employes, Ventes, Carte
                           WHERE matricule = employe_id AND id_boisson = boisson_id
                           GROUP BY nom_bar HAVING nom_bar = ? AND date LIKE '__/11/2022'""", (bar[0],)).fetchone()
    print(f"Le montant total des ventes ce mois-ci = {round(montant_total[0])}")
    benefice_par_employe = cursor.execute("""SELECT prenom, employes.nom, SUM(prix) FROM Employes, Ventes, Carte
                               WHERE matricule = employe_id AND id_boisson = boisson_id
                               GROUP BY nom_bar, matricule HAVING nom_bar = ? AND date LIKE '__/11/2022'""", (bar[0],)).fetchall()
    for i in benefice_par_employe:
        print(f"Le bénéfice généré par {i[0]} {i[1]} = {round(i[2], 2)} euros.")
else:
    print("Désolé, vous n'avez pas accès à ces informations.")


bdd.close()