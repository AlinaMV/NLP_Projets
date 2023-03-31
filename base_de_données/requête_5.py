#!usr/bin/env python3
# -*- coding: utf-8 -*-

# La BDD bar a 4 tables : Employes , Etablissement, Carte, Ventes

""" Donne à chaque manager la possibilité d’afficher les boissons
qui ont rapporté le plus d’argent dans leur établissement ce mois-ci.
Affiche les employés ayant rapporté le plus d’argent."""

import csv
import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()
bdd.text_factory = str  # pour éviter les erreurs d'encodage


# On créé une liste des matricules des managers pour ne donner l'accès qu'aux managers
managers_request = cursor.execute("SELECT manager_id FROM Etablissement").fetchall()
managers_list = [i[0] for i in managers_request]

# Décommenter pour choisir un matricule de manager et vérifier les requêtes
# print(managers_list)

# On récupère le matricule de l'employé
user = input("Bonjour, saisissez votre matricule, s'il vous plaît.\n")

# On récupère le nom du bar du manager
bar = cursor.execute('SELECT name FROM Etablissement WHERE manager_id == ?', (user,)).fetchone()

# Le Bar et les 5 boissons ayant rapporté le plus d'argent ce mois-ci, novembre 2022
if user in managers_list:
    cursor.execute("""SELECT nom_bar, id_boisson, Carte.nom, SUM(prix) AS sales \
                    FROM Employes, Ventes, Carte
                    WHERE matricule = employe_id 
                    AND date LIKE '%/11/2022'
                    AND nom_bar LIKE ?
                    AND id_boisson = boisson_id
                    GROUP BY id_boisson
                    ORDER BY sales DESC LIMIT 5""", (bar[0],))
                    
    for ligne in cursor.fetchall():
        print(f" Votre bar {ligne[0]} a vendu boisson numéro: {ligne[1]}, {ligne[2]}, pour un montant total de: {round(ligne[3], 3)} euros")

    
    # Les 5 employés ayant rapporté le plus d'argent
    cursor.execute("""SELECT prenom, Employes.nom, SUM(prix) AS sales 
                    FROM Employes, Ventes, Carte, Etablissement 
                    WHERE matricule = employe_id 
                    AND boisson_id = id_boisson 
                    AND date LIKE '%/11/2022'
                    AND Etablissement.name = nom_bar
                    GROUP BY matricule HAVING nom_bar = ?
                    ORDER BY sales DESC LIMIT 5""", (bar[0],))
                        
    for ligne in cursor.fetchall():
        print(f" L'employé {ligne[0]} {ligne[1]} a vendu des boissons pour un montant total de: {round(ligne[2], 2)} euros")
                        

else:
    # Le matricule saisi ne correspond pas à celui d'un manager
    print("Désolé, vous n'avez pas accès à ces informations.")


bdd.close()