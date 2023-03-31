#!usr/bin/env python3
# -*- coding: utf-8 -*-

# La BDD bar a 4 tables : Employes , Etablissement, Carte, Ventes
# Attention! ce script permet d'éliminer des données de la table Carte

""" Le script permet d'afficher et de supprimer les boissons les moins consommées
et/ou les boissons qui rapportent le moins d’argent.
Le nombre de boissons à supprimer est défini en ligne de commande, en entrée du script."""

import csv
import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()
bdd.text_factory = str  # pour éviter les erreurs d'encodage

# creation des listes pour les id_boissons les moins vendues
list1_boisson_del = [] 
list2_boisson_del = []

# création d'une liste des matricules des managers pour ne donner l'accès qu'aux managers
managers_request = cursor.execute("SELECT manager_id FROM Etablissement").fetchall()
managers_list = [i[0] for i in managers_request]

# Décommenter pour tester le programme avec un matricule de manager
# print(managers_list)

# On récupère la matricule de l'employé
user = input("Bonjour, saisissez votre matricule, s'il vous plaît.\n")

# On récupère le nom du bar du manager
bar = cursor.execute('SELECT name FROM Etablissement WHERE manager_id == ?', (user,)).fetchone()

def del_boissons(del_list, cat, limit):
    delete = int(input(f"Parmi ces moins {cat}, combien de boissons souahaitez-vous supprimer de la Carte (maximum possible {limit})? "))
    if delete <= limit:
        i = 0
        while i < delete:
            cursor.execute("""DELETE FROM Carte 
                            WHERE id_boisson LIKE ?""", (del_list[i],) )
            i+=1
        print("Les boissons ont été supprimées de votre base de données.")        
    else: 
        print("Désolé, vous ne pouvez pas supprimer les boissons, sans avoir consulté les données correspondantes.")



# Boissons les moins vendues
if user in managers_list:
    set_limit = int(input("Veuillez saisir le nombre de boissons les moins vendues ou les moins rentables que vous souhaitez afficher : "))
    least_sold = cursor.execute("""SELECT nom_bar, COUNT(id_boisson) as lowest, id_boisson, Carte.nom 
                                    FROM Employes, Ventes, Carte
                                    WHERE matricule = Employe_id AND nom_bar = ? AND id_boisson = boisson_id
                                    GROUP BY nom_bar, id_boisson
                                    ORDER BY lowest LIMIT ?""", (bar[0], set_limit)).fetchall() 
    for ligne in least_sold:
        print(f" Parmi les boissons les moins vendues au bar {ligne[0]} est {ligne[3]} : (id:{ligne[2]}), vendues {ligne[1]} fois") 
        list1_boisson_del.append(ligne[2]) 


    # nombre de boissons moins rentables en input() et affichage des ces boissons moins rentables
    least_profit= cursor.execute("""SELECT nom_bar, Sum(prix) as lowest, id_Boisson, Carte.nom FROM Employes, Ventes, Carte
                       WHERE matricule = employe_id AND nom_bar = ? AND id_boisson = boisson_id
                       GROUP BY nom_bar, id_boisson
                       ORDER BY lowest LIMIT ?""", (bar[0], set_limit)).fetchall()         
    for ligne in least_profit:   
        print(f" Au bar {ligne[0]}, parmi les boissons les moins rentables se trouve {ligne[3]}: (id:{ligne[2]}), vendues pour un monant de {round(ligne[1], 3)} euros.")
        list2_boisson_del.append(ligne[2]) 

    answer =  input(f"Parmi les moins vendues et les moins rentables, lesquelles souhaitez-vous supprimer (tapez: vendues, rentables ou aucune)? ")
    if answer == "vendues": 
        del_boissons(list1_boisson_del, "vendues", set_limit)
    elif answer == "rentables":
        del_boissons(list2_boisson_del, "rentables", set_limit)
    else:
        exit()
else:
    print("Désolé, vous n'avez pas accès à ces informations.")

bdd.commit()
bdd.close()

# supprimer bars.bd et relancer le premier script "Exercice_1...", pour des requêtes sur la bdd originale
