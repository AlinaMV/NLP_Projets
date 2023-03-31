#!usr/bin/env python3
#-*- coding: utf-8 -*-

# creátion de la base de données (fichier bars.db) à partir des 4 tables : Employes , Etablissements, Carte, Ventes

import csv
import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()
bdd.text_factory = str # pour éviter les erreurs d'encodage


cursor.execute("CREATE TABLE Employes (prenom TEXT NOT NULL, nom TEXT NOT NULL, \
    matricule TEXT PRIMARY KEY, profession TEXT NOT NULL, nom_bar TEXT NOT NULL);")

cursor.execute("CREATE TABLE Etablissement (idEtablissement INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, adresse TEXT NOT NULL, \
        numTel TEXT NOT NULL, manager_id TEXT NOT NULL, FOREIGN KEY(manager_id) REFERENCES Employes(matricule));")

cursor.execute("CREATE TABLE Carte (id_boisson INTEGER PRIMARY KEY, nom TEXT NOT NULL, \
        type TEXT NOT NULL, prix REAL NOT NULL, degre REAL, quantite REAL NOT NULL);")

cursor.execute("CREATE TABLE Ventes (employe_id TEXT NOT NULL, boisson_id INTEGER NOT NULL, date TEXT NOT NULL , \
               FOREIGN KEY (employe_id) REFERENCES Employes(matricule), FOREIGN KEY (boisson_id) REFERENCES Carte(id_boisson));" )


""" Une variable PATH pour faciliter le travail depuis plusieurs ordinateurs. 
Saisissez le chemin vers le dossier contenant les fichiers csv. 
"""
PATH = "data/"

# lecture du fichier employes.csv
employeFile = open(PATH+'employes.csv', 'r')
csvEmploye = csv.DictReader(employeFile, delimiter='\t')

for employe in csvEmploye:
    cursor.execute("INSERT INTO Employes (prenom, nom, matricule, profession, nom_bar) VALUES (:Prenom, :Nom, :Matricule, :Profession, :Nom_Bar)", (employe))

employeFile.close()

# lecture du fichier etablissements.csv
etabFile = open(PATH+'etablissements.csv', 'r')
csvEtab = csv.DictReader(etabFile, delimiter='\t')

for etablissement in csvEtab:
    cursor.execute("INSERT INTO Etablissement (name, adresse, numTel, manager_id) VALUES (:Name, :Adresse, :NumTel, :Manager_Id)", etablissement)

etabFile.close()

# lecture du fichier carte.csv
carteFile = open(PATH+'carte.csv', 'r')
csvCarte = csv.DictReader(carteFile, delimiter='\t')

for carte in csvCarte:
    cursor.execute ("INSERT INTO Carte (id_boisson, nom, type, prix, degre, quantite) VALUES (:Id_Boisson, :Nom, :Type, :Prix, :Degre, :Quantite)", carte)

carteFile.close()

#lecture du fichier ventes.csv
ventesFile = open(PATH+'ventes.csv', 'r')
csvVentes = csv.DictReader(ventesFile, delimiter='\t')

for vente in csvVentes: 
    cursor.execute ("INSERT INTO Ventes (employe_id , boisson_id , date) VALUES (:Employe_Id, :Boisson_Id, :Date)", vente)

ventesFile.close()

bdd.commit()
bdd.close()



