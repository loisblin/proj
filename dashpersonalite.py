# -*- coding: mbcs -*-
from collections import defaultdict
import json
import plotly.express as px
import pandas as pd
import sys
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime, timezone

# Ouvrir le fichier JSON
sys.stdout.reconfigure(encoding='utf-8')
def filtrearticle(selected_articles,datatotal):
    dataselect=[]
    for article in selected_articles:
        dataselect.append(datatotal[article])
    return dataselect
def filtretemps(value):
    temps_en_secondes_debut = value[0]
    date_obj = datetime.fromtimestamp(temps_en_secondes_debut, timezone.utc)
    date_formattee_debut = date_obj.strftime('%Y-%m')
    temps_en_secondes_fin = value[1]
    date_obj = datetime.fromtimestamp(temps_en_secondes_fin, timezone.utc)
    date_formattee_fin = date_obj.strftime('%Y-%m')
    date_debut=date_formattee_debut.split("-")
    date_fin=date_formattee_fin.split("-")
    date=[date_debut,date_fin]
    return date
def top10max(article,annee,mois):
    top10=[]
    if str(mois) in article['metadata-all']['fr']['month'][str(annee)] and 'per' in article['metadata-all']['fr']['month'][str(annee)][str(mois)]:
        celebrite_mois = article['metadata-all']['fr']['month'][str(annee)][str(mois)]['per']
        top=sorted(celebrite_mois.items(), key=lambda t: t[1])
        top.reverse()
        L=len(top)
        if L>10:
            L=10
        for k in range(0,L):
            top10.append(top[k])
    else:
        top10=[]
    return(top10)
def concatenetop(listetop):
    occurrences = defaultdict(int)

    for liste_tuples in listetop:
        for element, count in liste_tuples:
            occurrences[element] += count

    # Trier le dictionnaire en fonction des occurrences (somme des nombres d'apparitions) de manière décroissante
    sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)

    # Sélectionner les 10 premiers éléments pour obtenir le top 10
    top_10 = sorted_occurrences[:10]
    return(top_10)
def get_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key    

# Ouvrir le fichier JSON




date=[["2019","5"],["2021","11"]]
def concatenetop2(listetop):
    occurrences = defaultdict(int)

    for liste_tuples in listetop:
        if isinstance(liste_tuples, tuple):
            # Si liste_tuples est un tuple, ajoutez-le tel quel
            occurrences[liste_tuples[0]] += liste_tuples[1]
        else:
            # Sinon, traitez chaque élément comme un tuple
            for element in liste_tuples:
                # Assurez-vous que element[1] peut être converti en entier
                try:
                    count = int(element[1])
                except (TypeError, ValueError):
                    # En cas d'erreur de conversion, ignorez cet élément
                    continue

                occurrences[element[0]] += count

    # Trier le dictionnaire en fonction des occurrences (somme des nombres d'apparitions) de manière décroissante
    sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)

    # Sélectionner les 10 premiers éléments pour obtenir le top 10
    top_10 = sorted_occurrences
    return top_10


def locpers(article,pers,annee,mois):
    toploc=[]
    if str(mois) in article['metadata-all']['fr']['month'][str(annee)] and 'per' in article['metadata-all']['fr']['month'][str(annee)][str(mois)]:
        loc_mois = article['metadata-all']['fr']['day'][str(annee)][str(mois)]
        for jour in range(1,32):
            if str(jour)in loc_mois:
                if pers in article['metadata-all']['fr']['day'][str(annee)][str(mois)][str(jour)]["per"]:    
                    loc_jour=article['metadata-all']['fr']['day'][str(annee)][str(mois)][str(jour)]["loc"]
                    top=sorted(loc_jour.items(), key=lambda t: t[1])
                    top.reverse()
                    L=len(top)
                    
                    for k in range(0,L):
                        toploc.append(top[k])
    return toploc if toploc else None



def famousmap(per,dataselect,dateselect):
    date = [[int(dateselect[0][0]), int(dateselect[0][1])], [int(dateselect[1][0]), int(dateselect[1][1])]]
    toploc=[]
    for article in dataselect:
        
        if date[0][0] == date[1][0]:
             for mois in range(date[0][1], date[1][1] + 1):
                toplocmois=concatenetop2(locpers(article,per,date[0][0],(mois)))
                for top in toplocmois:
                    toploc.append(top)
        else:
            for annee in range(date[0][0], date[1][0] + 1):
                for mois in range(date[0][1],13):
                    toplocmois=locpers(article,per,(annee),(mois))
                    if toplocmois is not None:
                        topp=concatenetop2(toplocmois)
                        for top in topp:
                            toploc.append(top)
                for mois in range(1,date[1][1]):
                    toplocmois=locpers(article,per,(annee),(mois))
                    if toplocmois is not None:
                        topp=concatenetop2(toplocmois)
                        for top in topp:
                            toploc.append(top)
                    
                    
    toplocconca=concatenetop2(toploc)
    data=[]
    for top in toplocconca:
        data.append({'lieu': top[0], 'fois': top[1]})
    df = pd.DataFrame(data)

    # Normalisez les données pour les adapter à la palette de couleurs
    fig = px.choropleth(
    df,
    locations='lieu',
    locationmode='country names',
    color='fois',
    color_continuous_scale="Viridis",
    title=f"Frequence des lieux ou {per} a de l'influence",
    labels={'fois': 'Nombre de fois'}
    )
    return fig


def voispers(article, pers, annee, mois):
    toploc = []
    if str(mois) in article['metadata-all']['fr']['month'][str(annee)] and 'kws' in article['metadata-all']['fr']['month'][str(annee)][str(mois)]:
        loc_mois = article['metadata-all']['fr']['day'][str(annee)][str(mois)]
        for jour in range(1, 32):
            if str(jour) in loc_mois:
                if pers in article['metadata-all']['fr']['day'][str(annee)][str(mois)][str(jour)]["per"]:
                    loc_jour = article['metadata-all']['fr']['day'][str(annee)][str(mois)][str(jour)]["kws"]
                    top = sorted(loc_jour.items(), key=lambda t: t[1])
                    top.reverse()
                    L = len(top)
                    
                    for k in range(0, L):
                        toploc.append(top[k])
    return toploc if toploc else None

def moyper(per, dataselect, dateselect):
    date = [[int(dateselect[0][0]), int(dateselect[0][1])], [int(dateselect[1][0]), int(dateselect[1][1])]]
    toploc = []
    for article in dataselect:
        if date[0][0] == date[1][0]:
            for mois in range(date[0][1], date[1][1] + 1):
                toplocmois = voispers(article, per, date[0][0], mois)
                for top in toplocmois:
                    toploc.append(top)
        else:
            for annee in range(date[0][0], date[1][0] + 1):
                for mois in range(date[0][1], 13):
                    toplocmois = voispers(article, per, annee, mois)
                    if toplocmois is not None:
                        for top in toplocmois:
                            toploc.append(top)
                for mois in range(1, date[1][1]):
                    toplocmois = voispers(article, per, annee, mois)
                    if toplocmois is not None:
                        for top in toplocmois:
                            toploc.append(top)

    mot_occurrences = {}

    for mot, apparitions in toploc:
        if mot in mot_occurrences:
            mot_occurrences[mot] += apparitions
        else:
            mot_occurrences[mot] = apparitions

    # Transformation du dictionnaire en une liste de tuples
    aggregated_list = [(mot, apparitions) for mot, apparitions in mot_occurrences.items()]

    # Tri de la liste agrégée en fonction du nombre d'apparitions (le deuxième élément du tuple)
    sorted_aggregated_list = sorted(aggregated_list, key=lambda x: x[1], reverse=True)

    # Sélection des 10 premiers éléments de la liste triée
    top_10_mots = sorted_aggregated_list[:10]

    top_10_mots =toploc[:10]
    
    data = []
    for t in top_10_mots:
        data.append({'mots': t[0], 'fois': t[1]})
    df = pd.DataFrame(data)

    # Normalisez les données pour les adapter à la palette de couleurs
    fig = px.bar(df, x="mots", y="fois",
             labels={"mots": "Mots cles", "fois": "Nombre de mentions"},
             title=f"Nombre de mentions des mots cles pour {per}")
    return fig




datatotal={}
with open('mali.json', 'r', encoding='utf-8') as json_file:
    datamali1 = json.load(json_file)
    
    datatotal["datamali1"]=datamali1

with open('topaz-data732--france--fr.sputniknews.africa--20190101--20211231.json', 'r', encoding='utf-8') as json_file:
    datafr1 = json.load(json_file)
    datatotal["datafr1"]=datafr1
with open('topaz-data732--france--french.presstv.ir--20190101--20211231.json', 'r', encoding='utf-8') as json_file:
    datafr2 = json.load(json_file)
    datatotal["datafr2"]=datafr2
with open('topaz-data732--france--www.egaliteetreconciliation.fr--20190101--20211231.json', 'r', encoding='utf-8') as json_file:
    datafr3 = json.load(json_file)
    datatotal["datafr3"]=datafr3
with open('topaz-data732--france--www.fdesouche.com--20190101--20211231.json', 'r', encoding='utf-8') as json_file:
    datafr4 = json.load(json_file)
    datatotal["datafr4"]=datafr4
with open('topaz-data732--mali--fr.sputniknews.africa--20190101--20211231.json', 'r', encoding='utf-8') as json_file:
    datamali2 = json.load(json_file)
    datatotal["datamali2"]=datamali2

with open('topaz-data732--mali--french.presstv.ir--20190101--20211231.json', 'r', encoding='utf-8') as json_file:
    datamali3 = json.load(json_file)
    datatotal["datamali3"]=datamali3


articledcc = [{'label': data_name, 'value': data_name} for data_name in datatotal.keys()]





# Initialisation de l'application Dash
app = dash.Dash(__name__)
# Créez un DataFrame pour gérer les dates
date_df = pd.date_range(start="2019-01-01", end="2021-12-31", freq='M')
# Mise en page de l'application
app.layout = html.Div([
    html.H1("Visualisation des donnees concernant les personnages important "),
    
    # Sélection de la période et des articles
    dcc.RangeSlider(
        id='date-slider',
        min=date_df.min().timestamp(),
        max=date_df.max().timestamp(),
        marks={date.timestamp(): date.strftime('%Y-%m-%d') for date in date_df},
        step=None,
        value=[date_df.min().timestamp(), date_df.max().timestamp()],
    ),
    html.Div(id='date-output-container',
             style={'font-size': '24px',  # Ajoutez cette ligne pour augmenter la taille du texte
                    'text-align': 'center',  # Ajoutez cette ligne pour centrer le texte horizontalement
                    'margin-top': '20px'}),
    html.Div("Choix article:", style={'text-decoration': 'underline','font-size': '18px'}),
    dcc.Checklist(
        id='article-Checklist',
        options=articledcc,
        value=[option['value'] for option in articledcc]  # Sélectionnez toutes les options par défaut
    ),
    
    # Graphique du top des personnages
    dcc.Graph(
        id='top-characters-graph',
        
        clickData={'points': [{'customdata': 'default_value'}]}  # Définissez une valeur par défaut
    ),
    html.Div(id='selected-person-output', style={
            'margin-top': '20px',
            'text-align': 'center',
            'margin': 'auto',
            'font-size': '20px',  # Ajoutez cette ligne pour augmenter la taille du texte
            'border': '2px solid black',  # Ajoutez cette ligne pour ajouter une bordure
            'padding': '10px'  # Ajoutez cette ligne pour ajouter un espace intérieur
        }),
    
    html.Div([
        dcc.Graph(
            id='graph1',
            # Assurez-vous de configurer correctement les données ici
        ),
        dcc.Graph(
            id='graph2',
            # Assurez-vous de configurer correctement les données ici
        ),
    ], style={'width': '100vw', 'display': 'flex','flex-wrap':'wrap'})
])

@app.callback(
    dash.dependencies.Output('date-output-container', 'children'),
    [dash.dependencies.Input('date-slider', 'value')]
)
def update_output(value):
    date_start = datetime.utcfromtimestamp(value[0]).strftime('%Y-%m-%d')
    date_end = datetime.utcfromtimestamp(value[1]).strftime('%Y-%m-%d')
    return f'Date de depart: {date_start} - Date de fin: {date_end}'
# Callback pour mettre à jour le graphique du top des personnages
@app.callback(
    Output('top-characters-graph', 'figure'),
    [Input('date-slider', 'value'),
     Input('article-Checklist', 'value')]
)



def update_top_characters_graph(selected_dates, selected_articles):
    # Code pour filtrer les données en fonction des sélections
    dataselect = filtrearticle(selected_articles, datatotal)
    dateselect = filtretemps(selected_dates)
    
    date = [[int(dateselect[0][0]), int(dateselect[0][1])], [int(dateselect[1][0]), int(dateselect[1][1])]]

    # Code pour créer le graphique du top des personnages
    top = []
    for article in dataselect:
        topart = []
        if date[0][0] == date[1][0]:
            for k in range(date[0][1], date[1][1] + 1):
                topart.append(top10max(article, dateselect[0][0], str(k)))
        else:
            for k in range(date[0][0], date[1][0] + 1):
                if k == date[0][0]:
                    start_month = date[0][1]
                else:
                    start_month = 1

                if k == date[1][0]:
                    end_month = date[1][1] + 1
                else:
                    end_month = 13

                for i in range(start_month, end_month):
                    topart.append(top10max(article, str(k), str(i)))

        
        topartconca = concatenetop(topart)
        

        if len(topartconca) > 10:
            L = 10
        else:
            L = len(topartconca)
        for i in range(0, L):
            top.append({'article': get_key_by_value(datatotal,article), 'top10': topartconca[i][0], 'fois': topartconca[i][1]})

    # Utilisez la bibliothèque Plotly Express pour faciliter la création de graphiques
    df = pd.DataFrame(top)
    #df['article'] = df['article'].apply(lambda x: str(x))  # Convertir les dictionnaires en chaînes de caractères
    fig = px.bar(df, x="top10", y="fois", color="article",
             labels={"top10": "Personalite", "fois": "fois", "article": "article"},
             title="personnalite en fonction de leur nombre d'apparitions")
    return fig


# Callbacks pour mettre à jour les deux graphiques dépendants

@app.callback(
    Output('graph1', 'figure'),
    [Input('top-characters-graph', 'clickData'),
     Input('date-slider', 'value'),
     Input('article-Checklist', 'value')]
)
def update_graph1(clickData, selected_dates, selected_articles):
    # Code pour filtrer les données en fonction de la personne choisie dans le top
    dataselect = filtrearticle(selected_articles, datatotal)
    dateselect = filtretemps(selected_dates)
    
    

    
    
    if clickData is None:
        # Aucun clic, retourner un graphique vide
        return {}
    
    selected_person = clickData['points'][0]['x']
    
    

    # Utiliser la personne sélectionnée pour générer le graphique 1
    fig=famousmap(selected_person, dataselect, dateselect)
    return fig

@app.callback(
    Output('graph2', 'figure'),
    [Input('top-characters-graph', 'clickData'),
     Input('date-slider', 'value'),
     Input('article-Checklist', 'value')]
)
def update_graph2(clickData, selected_dates, selected_articles):
    # Code pour filtrer les données en fonction de la personne choisie dans le top
    dataselect = filtrearticle(selected_articles, datatotal)
    dateselect = filtretemps(selected_dates)
    
    # Utilisez la bibliothèque Plotly Express pour faciliter la création de graphiques
    
    if clickData is None:
        # Aucun clic, retourner un graphique vide
        return {}
    
    selected_person = clickData['points'][0]['x']
    
    fig=moyper(selected_person, dataselect, dateselect)
    return fig
@app.callback(
    Output('selected-person-output', 'children'),
    [Input('top-characters-graph', 'clickData')]
    )
def update_selected_person_output(clickData):
    # Obtenez la personne sélectionnée à partir des données de clic
    if clickData is None:
        return 'Aucune personne sélectionnée'
    else:
        selected_person = clickData['points'][0]['x']
        return f'Personne selectionnee : {selected_person}'
# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)

            
