import numpy as np
import pandas as pd
import spacy
import pickle
from sentence_transformers import SentenceTransformer
import transformers as ppb
from sklearn.linear_model import LogisticRegression

from webScraper import webScraping

### Functies 
def text_to_sent_list(text, nlp, embedder, min_len=2):
    ''' Returns cleaned article sentences and BERT sentence embeddings '''
    
    #convert to list of sentences
    text = nlp(text)
    sents = list(text.sents)
    #remove short sentences by threshhold                                                                                                
    sents_clean = [sentence.text for sentence in sents if len(sentence)> min_len]
    #remove entries with empty list
    sents_clean = [sentence for sentence in sents_clean if len(sentence)!=0]
    #remove new lines from list
    sents_clean = [sentence.replace("/n", "") for sentence in sents_clean if len(sentence)!=0]
    #embed sentences (deafult uses BERT SentenceTransformer)
    sents_embedding= np.array(embedder.encode(sents_clean, convert_to_tensor=True))

    return sents_clean, sents_embedding

def get_pred_sum(text_clean, y_pred, thresh, amount):
    ''' Returns the summary that the model predicted '''

    sentenceScoreList = []
    for i in range(len(y_pred)):
        if y_pred[i][0] > thresh:
            sentenceScoreList.append(y_pred[i][0])
    
    #print(sentenceScoreList)
            
    predSentenceScoreIndexList =  sorted( [(x,i) for (i,x) in enumerate(sentenceScoreList)], reverse=True )[:amount]
    predSentenceIndexList = []
    for item in predSentenceScoreIndexList:
        predSentenceIndexList.append(item[1])
    
    #print(predSentenceIndexList)

    summarySentenceList = []
    for index in sorted(predSentenceIndexList):
        summarySentenceList.append(text_clean[index])

    summary = ""
    for item in summarySentenceList:
        summary += item
        summary += " "
    
    return summary
            
def predictSummary(articleLink):
    # Webscraping functie uitvoeren die de tekst uit een gegeven link haalt
    webscraper = webScraping(articleLink)

    if webscraper["status"] == True:

        try:
            #variabelen defineren
            model_file = "data/logisticRegression_model.pickle"
            article_file = "data/article.txt"
            nlp = spacy.load("en_core_web_sm")
            embedder = SentenceTransformer('distilbert-base-nli-mean-tokens')
        except:
            response = {
                "status":False,
                "message":"Something went wrong getting the model"
            }
            return response 
        
        try:
            #articel inlezen
            article = open(article_file).read()

            # Een lijst met elke zin in en een lijst met embeddings van elke zin aanmaken
            text_clean, text_embedding = text_to_sent_list(article, nlp, embedder)

            #De betekenis van de volledige tekst berekenen en uitdruikken in een vector
            doc_mean = text_embedding.mean(axis=0).reshape(1,-1)

            X = np.hstack((text_embedding[0].reshape(1,-1), doc_mean))
            for i in range(1, len(text_embedding)):
                X_new = np.hstack((text_embedding[i].reshape(1,-1), doc_mean))

                X = np.vstack((X, X_new))
        except:
            response = {
                "status":False,
                "message":"Something went wrong formating the data"
            }
            return response 

        try:
            # getrain model ophalen
            model = pickle.load(open(model_file, 'rb'))

            y_pred = model.predict_proba(X)

            sentenceAmount = round(len(y_pred) / 5)
            if sentenceAmount < 3:
                sentenceAmount = 3
            if sentenceAmount > 8:
                sentenceAmount = 8

            predictedSummary = get_pred_sum(text_clean, y_pred, 0.50, sentenceAmount)

        except:
            response = {
                "status":False,
                "message":"Something went wrong generating the summary"
            }
            return response 
        
        response = {
            "status":True,
            "message":"Successfully generated a summary",
            "heading":webscraper["heading"],
            "summary":predictedSummary
        }
        return response 

    else:
        return webscraper 





