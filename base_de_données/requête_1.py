#!usr/bin/env python3
#-*- coding: utf-8 -*-

# bdd bar a 4 tables : Employes , Etablissement, Carte, Ventes
# Le droit d'accès à la BDD est réservé aux managers

""" Le script permet de consulter le nombre total de boissons vendues par chaque employé 
ainsi que le montant total associé à ces ventes."""

import csv
import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()
bdd.text_factory = str # pour éviter les erreurs d'encodage

# On crée une liste des matricules des managers pour ne donner l'accès qu'aux managers
managers_request = cursor.execute("SELECT manager_id FROM Etablissement").fetchall()
managers_list = [i[0] for i in managers_request]

# si on souhaite récupérer la liste des matricules des managers, afin de tester le programme :
# print(managers_list)

# On récupère la matricule de l'employé
user = input("Bonjour, veuillez saisir votre matricule, s'il vous plaît.\n")

# On récupère le nom du bar du manager
bar = cursor.execute('SELECT name FROM Etablissement WHERE manager_id == ?', (user,)).fetchone()

if user in managers_list:
    # Nombre total de boissons vendues par employé (prénom, nom matricule), et le montant associé
    cursor.execute("""SELECT E.prenom, E.nom, V.employe_id, COUNT(V.boisson_id), SUM(C.prix)
                    FROM Ventes as V, Carte as C, Employes as E 
                    WHERE V.boisson_id = C.id_boisson AND E.matricule = V.employe_id
                    GROUP BY V.employe_id HAVING nom_bar = ?;""", (bar[0],))
    for ligne in cursor.fetchall():
        print(f"{ligne[0]} {ligne[1]}, matricule: {ligne[2]}, a vendu : {ligne[3]} boissons, pour un montant total de: {round(ligne[4], 3)} euros.")
else:
    print("Désolé, vous n'avez pas accès à ces informations.")

bdd.close()