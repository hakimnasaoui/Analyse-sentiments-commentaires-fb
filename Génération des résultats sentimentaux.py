#imports :
import requests 
import json
from google.cloud import language, exceptions
# google.cloud est une API cree par Google, 
# nous permettant d'utiliser des bibliothèques client Google Cloud 'Cloud Natural Language' dans notre projet.


client = language.Client()
# export GOOGLE_APPLICATION_CREDENTIALS environment variable 


#Ouverture de fichier json de commentaires du post specifie
with open('commentaires_data.json') as data_file:
    data = json.load(data_file)

sentiment_list = []
for x1,y1  in data['commentaire'].items():
    try:
        document = client.document_from_text(y1)
        sentiment = document.analyze_sentiment().sentiment
        sentiment_list.append({"id": x1, "commentaire": y1, "sentiment_score": sentiment.score, "sentiment_magnitude": sentiment.magnitude })
        print "OK"
    except:
        print "Echec"
			

#generation des sentiments des commentaire sous fichier json (w = mode ecritue)
with open('sentiment_commentaires.json', 'w') as outfile:
    json.dump(sentiment_list, outfile)