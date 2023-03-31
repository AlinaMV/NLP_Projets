#!usr/bin/env python3
# -*- coding: utf-8 -*-

# La BDD bar a 4 tables : Employes , Etablissement, Carte, Ventes


""" Ce script donne à chaque manager la possibilité d’afficher le nombre de ventes
effectuées ce mois-ci par ses employés et le montant que cela représente,
ainsi que le bénéfice généré pour chaque employé du bar. Le résultat s'affiche pour une date donnée.
Par exemple, on peut afficher les ventes effectuées à l’échelle de l’établissement le 24 novembre 2022.
La date est définie en ligne de commande, par l’utilisateur."""

import csv
import sqlite3
import re

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()
bdd.text_factory = str  # pour éviter les erreurs d'encodage


# On récupère le matricule de l'employé
user = input("Bonjour, saisissez votre matricule, s'il vous plaît.\n")

# On crée une liste des matricules des managers pour ne donner l'accès qu'aux managers
managers_request = cursor.execute("SELECT manager_id FROM Etablissement").fetchall()
managers_list = [i[0] for i in managers_request]

# On récupère le nom du bar du manager
bar = cursor.execute('SELECT name FROM Etablissement WHERE manager_id == ?', (user,)).fetchone()

# Ce message s'affichera, si la requête renvoie None
message = "Il paraît que la table ne contient aucun résultat pour cette date."

if user in managers_list:
    date = input("Saisissez la date au format DD/MM/YYYY pour voir les statistiques.\n")
    if re.fullmatch('\d\d/\d\d/\d{4}', date) is not None:

        # On récupère le résultat de chaque requête dans une variable
        nb_ventes = cursor.execute("""SELECT nom_bar, COUNT(*) FROM Employes, Ventes
                               WHERE matricule = employe_id AND nom_bar = ?
                               GROUP BY nom_bar, date HAVING date = ?""", (bar[0], date)).fetchone()

        montant_total = cursor.execute("""SELECT ROUND(Total) FROM (SELECT SUM(prix) AS Total FROM Employes, Ventes, Carte
                                   WHERE matricule = employe_id AND id_boisson = boisson_id
                                   GROUP BY nom_bar, date HAVING nom_bar = ? AND date = ?)""", (bar[0], date)).fetchone()

        benefice_par_employe = cursor.execute("""SELECT prenom, nom, ROUND(benef) FROM (SELECT prenom, Employes.nom, SUM(prix) AS benef FROM Employes, Ventes, Carte
                                       WHERE matricule = employe_id AND id_boisson = boisson_id
                                       GROUP BY nom_bar, date, matricule HAVING nom_bar = ? AND date = ?)""", (bar[0], date)).fetchall()

        # Si la base contient les informations pour la date saisie, on les affiche.
        # Sinon on dit que la base ne contient pas de données pour cette date.

        if nb_ventes and montant_total and benefice_par_employe is not None:
            print(f"Le nombre de ventes dans le bar {nb_ventes[0]} = {nb_ventes[1]}.")
            print(f"Le montant total des ventes pour la date saisie = {montant_total[0]}.")
            for i in benefice_par_employe:
                print(f"Le bénéfice généré par {i[0]} {i[1]} pour la date saisie = {i[2]} euros.")
        else:
            print(message)


    else:
        print("La date saisie n'est pas au bon format.")


else:
    # Le matricule ne correspond pas à celui d'un manager
    print("Désolé, vous n'avez pas accès à ces informations.")

bdd.close()