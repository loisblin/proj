import json
import plotly.express as px
import re
import unicodedata
from collections import defaultdict


with open('mali.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
def normalize_name(name):
   
    step1 = unicodedata.normalize("NFD",name)
    

    step2 = re.sub(r'[^a-zA-Z\s]','',step1)
    
    finalStep = step2.lower()
    return finalStep
def singular(word):

    if word.endswith("s"):
        return word[:-1]
    else:
        return word
def normalize_key(key):
    normalized_key = normalize_name(key.lower())
    return normalized_key
def normalize_keys(key_set):
    normalized_set = {normalize_key(key) for key in key_set}
    return normalized_set
def combine_and_normalize_keys(groups_of_keys):
    combined_keys = set()
    
    for key_set in groups_of_keys:
        combined_keys.update(key_set)
    
    normalized_keys = {normalize_key(key) for key in combined_keys}
    return normalized_keys
def creer_matrice_occurrence(liste_mots):
    matrice_occurrence = defaultdict(dict)

    for ligne in liste_mots:
        for i in range(len(ligne)):
            mot1 = ligne[i]
            for j in range(i + 1, len(ligne)):
                mot2 = ligne[j]

                
                matrice_occurrence[mot1][mot2] = matrice_occurrence[mot1].get(mot2, 0) + 1

              

    return matrice_occurrence

def concatenation(m1,m2):
    key1=m1.keys()
    key2=m2.keys()
    for k in key2:
        if k in key1:
            key3=m1[k].keys()
            key4=m2[k].keys()
            for i in key4:
                if i in key3:
                    m1[k][i]=m1[k][i]+m2[k][i]
                else:
                    m1[k][i]=m2[k][i]
        else:
            m1[k]=m2[k]
    return m1


def FM(article):
    contenu=article['content']
    kws=article['kws']
    loc=article['loc']
    org=article['org']
    per=article['per']
    mis=article['mis']
    kk=kws.keys()
    kl=loc.keys()
    ko=org.keys()
    kp=per.keys()
    km=mis.keys()
    kf=combine_and_normalize_keys([kk,kl,ko,kp,km])

    phrases=re.split('[?.]',contenu)
    
    
    M=[]
    for k in range(0,len(phrases)):
        motutile=[]
        phrasen=normalize_name(phrases[k])
        
        phrase=phrasen.split(' ')
        
        for word in phrase:
            normalized_word = normalize_name(word)
            wordf=singular(normalized_word)
            if wordf in kf and wordf!='faso':
                motutile.append(wordf)
            
        M.append(motutile)

            
    return(creer_matrice_occurrence(M))
def matrice_articles(data):
    M=creer_matrice_occurrence([])
    data_a_parcour=data['data-all']
    for annee in ['2019','2020','2021']:
        if annee in data_a_parcour:
            for mois in range(1, 13):
                mois_str = str(mois)
                if mois_str in data_a_parcour[annee]:
                    for jours in range(1, 32):
                        jours_str = str(jours)
                        if jours_str in data_a_parcour[annee][mois_str]:
                            articles_du_jour = data_a_parcour[annee][mois_str][jours_str]
                            if articles_du_jour:
                                M2 = FM(articles_du_jour[0])
                                concatenation(M, M2)

    return M

def filtrer_matrice_occurrence(matrice, seuil):
    mots_filtres = {}
    
    for mot, voisins in matrice.items():
        if mot!="" and voisins!="":
            voisins_filtres = {voisin: nombre_apparitions for voisin, nombre_apparitions in voisins.items() if voisins!=mot and nombre_apparitions > seuil}
        
            if voisins_filtres:
                mots_filtres[mot] = voisins_filtres
    
    return mots_filtres

def afficher_matrice_occurrence_heatmap(matrice):
    mots = list(matrice.keys())
    voisins = list({voisin for voisins in matrice.values() for voisin in voisins.keys()})
    valeurs = [[matrice[mot].get(voisin, 0) for voisin in voisins] for mot in mots]

    fig = px.imshow(valeurs, x=voisins, y=mots, color_continuous_scale='Viridis', labels=dict(color='Nombre d\'apparitions'))
    fig.update_layout(xaxis_title='Mots voisins', yaxis_title='Mots')
    fig.show()  







def graphfinal(data,filtre):
    M=matrice_articles(data)
    MF=filtrer_matrice_occurrence(M,filtre)

    return(afficher_matrice_occurrence_heatmap(MF))

graphfinal(data,5)







