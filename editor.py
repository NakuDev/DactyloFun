# -*- coding: utf-8 -*-
import csv



def lire_donnees_csv(chemin):
    fichier = open(chemin)
    table = list(csv.DictReader(fichier, delimiter=";"))
    fichier.close()
    return table

def ecrire_donnees_csv(table, sortie): 
    f = open(sortie, "w")
    w = csv.DictWriter(f, table[0].keys()) # Création d'un "stylo"
    w.writeheader() # Le stylo écrit dans le fichier les descripteurs
    w.writerows(table) # Le stylo écrit les données de table
    f.close()


df = lire_donnees_csv("dict2.csv")

for word in df:
    word["taille"] = len(word["mot"])

ecrire_donnees_csv(df, "dictout.csv")