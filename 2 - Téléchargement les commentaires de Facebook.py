#Imports :  
import requests 
import pandas as pd
import os, sys
#'Requests' permet d'envoyer des requêtes HTTP organiques, sans nécessiter de travail manuel
#'os' module fournit un moyen portable d’utiliser les fonctionnalités dépendantes du système d’exploitation

#Saisie de FB_TOKEN specifié 
fb_token = ""
try:
	#Les variables d'environnement sont accessibles via os.environ
    fb_token = os.environ['FB_TOKEN']
except:
    print "Veillez saisir la variable d'environnement FB_TOKEN"
    sys.exit(-1)

#page & post info pour verifier leurs sentiments
fb_pageid = "624258451196"
fb_postid = "12488754962145785"

#initialisation des variable pour stockage les données du post (commentaires, date de creation de chaqune) 
commentlst = []
datelst = []

#generation du URL de post avec fb_token 
url = "https://graph.facebook.com/v2.9/"+ fb_pageid +"_"+ fb_postid +"/comments?limit=100&access_token="+fb_token

#remplie de commentaires et date de creation de chaqune
while(True):
    posts = requests.get(url)
    posts_json = posts.json()
    for x1 in posts_json['data']:
        commentlst.append(x1.get('message').encode('utf-8').strip())
        datelst.append(x1.get('created_time'))
    next_page = ""
    try:
        next_page = posts_json['paging']['next']
        url = next_page
    except:
        break
    if not next_page: break
    print "Nombre Commantaires: %s,  Page Suivante: %s" % ( len(commentlst), url)

print "\nGeneration de fichier JSON"


#Affichage des information des commentaires et leur date de creation  
df = pd.DataFrame({'commentaire': commentlst, 'dates': datelst})
df['dates'] = pd.to_datetime(df['dates'])
df['day_of_week'] = df['dates'].dt.weekday_name
df['year'] = df['dates'].dt.year
df['month'] = df['dates'].dt.month
df['count'] = 1 

#conversion dataframe à fichier json
df.to_json('commentaires_data.json')