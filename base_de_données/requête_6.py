#!usr/bin/env python3
# -*- coding: utf-8 -*-

# La BDD bar a 4 tables : Employes , Etablissement, Carte, Ventes

""" Permet à chaque manager d’afficher les employés
qui ont vendu le plus de cocktails du jour et de bières en pression."""

import csv
import sqlite3


bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()
bdd.text_factory = str  # pour éviter les erreurs d'encodage


# On récupère le matricule de l'employé
user = input("Bonjour, saisissez votre matricule, s'il vous plaît.\n")

# On crée une liste des matricules des managers pour ne donner l'accès qu'aux managers
managers_request = cursor.execute("SELECT manager_id FROM Etablissement").fetchall()
managers_list = [i[0] for i in managers_request]
if user in managers_list:
    # On récupère le nom du bar du manager
    bar = cursor.execute('SELECT name FROM Etablissement WHERE manager_id == ?', (user,)).fetchone()

    # Nombre total de bières en pression (ID = 29) et de cocktails du jour (ID = 2).
    # On affiche trois employés ayant vendu le plus de boissons en question.
    nb_boissons_vendues = cursor.execute("""SELECT prenom, E.nom, nom_bar, COUNT(date) 
                          FROM Employes AS E, Ventes, (SELECT nom AS nom_boisson, id_boisson FROM Carte WHERE id_boisson = 29 OR id_boisson = 2)
                          WHERE employe_id = matricule AND boisson_id = id_boisson GROUP BY matricule, nom_bar
                          HAVING nom_bar = ? ORDER BY COUNT(date) DESC LIMIT 3""", (bar[0],)).fetchall()

    for i in nb_boissons_vendues:
        print(f"{i[0]} {i[1]} du bar {i[2]} a vendu {i[3]} bières en pression et cocktails du jour.")

else:
    # Le matricule ne correspond pas à celui d'un manager
    print("Désolé, vous n'avez pas accès à ces informations.")

bdd.close()