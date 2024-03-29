#################################################################################
#																				
#	Attention, pour le bon fonctionnement du script							
#	veuillez renseigner les chemins vers :										
#	la grille annotée, l'enregistrement des logatomes et le ditionnare		
#	dans les variables 'grille', 'son', 'table_complete' juste au-dessous.	
#																			    
#################################################################################


# Le text grid qui contient mes diphones
grille = Read from file: "/Users/alina/Documents/PluriTAL/archives/Mercredi_phonetique/логатомы/grille_MIASNIKOVA.TextGrid"

# L'enregistrement des logatomes
son = Read from file: "/Users/alina/Documents/PluriTAL/archives/Mercredi_phonetique/логатомы/audio_MIASNIKOVA.wav"

# Le chemin vers le dictionnaire utilisé pour la synthèse
table_complete = Read Table from tab-separated file: "/Users/alina/Documents/PluriTAL/archives/Mercredi_phonetique/логатомы/dico1_MIASNIKOVA.txt"


#####################################################


# Le son vide va contenir le(s) mot(s) synthétisé(s)
son_vide = Create Sound from formula: "concatenation", 1, 0, 0.01, 44100, "0"


# On demande à l'utilisateur de saisir le mot ou la phrase à synthétiser.
# Ensuite on demande si la phrase est interrogative ou affirmative
# pour adapter l'intonation
form quel mot souhaitez-vous synthétiser ?
	text mot_ortho
	comment Est-ce que la phrase est interrogative ?
choice Choix
	button oui
	button non
endform


################## La transcription de la phrase saisie par l'utilisateur #####################

# L'affichage de chaque mot dans la phrase se trouve dans la boucle while
# sous forme de pauses commentées

# Pour chercher le dernier mot dans la boucle while :
mot_ortho$ = mot_ortho$ + " "

longueur_mot_ortho = length(mot_ortho$)
phrase$ = ""


while longueur_mot_ortho > 0
	espace = index(mot_ortho$, " ")
	mot1$=left$(mot_ortho$, espace-1)
	# pause le mot = 'mot1$'

	select 'table_complete' 
	extraction = Extract rows where column (text): "orthographe", "is equal to", mot1$
	select 'extraction'
	mot_phonetique$ = Get value: 1, "phonetique"
	# pause la transcription du mot = 'mot_phonetique$'
	phrase$ = phrase$ + mot_phonetique$

	mot_ortho$ = right$(mot_ortho$, longueur_mot_ortho-espace)
	longueur_mot_ortho = length(mot_ortho$)

	# pause mot 1 = 'mot1$', et le reste = 'mot_ortho$'


endwhile


# On ajoute au début et à la fin de la phrase les diphones avec un phonème et une pause annotée comme _
phrase$ = "_" + phrase$ + "_"

pause la transcription de la phrase à synthétiser : 'phrase$'

# printline 'phrase$'


#################### Le découpage en diphones et leur concaténation ############################



select 'grille'
nb_intervals = Get number of intervals: 1
longueur = length(phrase$)

# la deuxième boucle : 1 = tier number, a = interval number
# m1 = middle1, m2 = middle2

for i from 1 to longueur-1
	diphone$ = mid$(phrase$, i, 2)	
	char1_diphone$ = left$(diphone$, 1)	
	char2_diphone$ = right$(diphone$, 1)	

	for a from 1 to nb_intervals-1
		select 'grille'
		st_interval = Get start time of interval: 1, a 
		et_interval = Get end time of interval: 1, a
		lb_interval$ = Get label of interval: 1, a
		lb_interval_suivant$ = Get label of interval: 1, a+1
		et_interval_suivant = Get end time of interval: 1, a+1

		if (lb_interval$ = char1_diphone$ and lb_interval_suivant$ = char2_diphone$)
			m1 = (et_interval - st_interval)/2 + st_interval
			m2 = (et_interval_suivant - et_interval)/2 + et_interval
			# printline 'm1:3' / 'm2:3'
			# 3 = number of decimals

			select 'son'
			To PointProcess (zeroes): 1, "no", "yes"
			index1_m1 = Get nearest index: m1
			index2_m1 = Get time from index: index1_m1
			index1_m2 = Get nearest index: m2
			index2_m2 = Get time from index: index1_m2

			select 'son'
			extrait_son = Extract part: index2_m1, index2_m2, "rectangular", 1, "no"

			select 'son_vide'
			plus 'extrait_son'
			son_vide = Concatenate

		 endif

	endfor

endfor


################# La modification de la f0 #######################

selectObject: "Sound chain"
start_time = Get start time
end_time = Get end time
mid_time = end_time/2

manip = To Manipulation: 0.01, 75, 500
pitch = Extract pitch tier
Remove points between: 'start_time', 'end_time'

# Si la phrase est affirmative
if choix$ = "non"

	Add point: 'start_time', 250
	Add point: 'mid_time', 300
	Add point: 'end_time'*0.80, 250
	Add point: 'end_time', 200

	select 'manip'
	plus 'pitch'
	Replace pitch tier

	select 'manip'
	Get resynthesis (overlap-add)

	selectObject: "Sound chain"
	plusObject: "Manipulation chain"
	Replace original sound

# Si la phrase est interrogative
elif choix$ = "oui"
	
	Add point: 'start_time', 250
	Add point: 'mid_time', 280
	Add point: 'end_time'*0.80, 300
	Add point: 'end_time', 350

	select 'manip'
	plus 'pitch'
	Replace pitch tier

	select 'manip'
	Get resynthesis (overlap-add)

	selectObject: "Sound chain"
	plusObject: "Manipulation chain"
	Replace original sound

endif



################### La modification de la durée #########################


selectObject: "Sound chain"
manip = To Manipulation: 0.01, 75, 500
duration = Extract duration tier

Add point: 'start_time', 1
Add point: 'mid_time', 0.9
Add point: 'mid_time'+0.001, 0.9
Add point: 'end_time', 0.8

select 'manip'
plus 'duration'
Replace duration tier

select 'manip'
Get resynthesis (overlap-add)

selectObject: "Sound chain"
plusObject: "Manipulation chain"
Replace original sound

#########################################

# Nettoyage de la fenêtre Praat
select all
minusObject: "Sound chain"
Remove

# Renommage de l'audio synthétisé
selectObject: "Sound chain"
Rename: "Version finale"


#####################
