import customtkinter
from collections import deque
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 
import random
from random import choice
import networkx as nx
import matplotlib.pyplot as plt
import os

dossier = "graph"


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()

root.title('SAE2.02')
root.geometry("1280x720")

windows = customtkinter.CTkTabview(root,
                               width = 1250,
                               height=1250,
                               )
windows.pack()

tab1 = windows.add("Aléatoire")
tab2 = windows.add("Métro")


#########################################################################################################################################
# Aléatoire
#########################################################################################################################################

##################################
# Titre
##################################

titreframe = customtkinter.CTkFrame(tab1,)
titreframe.pack()
titrealea = customtkinter.CTkLabel(titreframe,  text='Test Unitaires', font=('bolder', 50))
titrealea.pack()


##################################
# Paramètres générateur
##################################

def init_graph(order):
    graph = {i: [] for i in range(order)}
    return graph

def add_edge(graph, src, dest, weight=1, ):
    # Ajouter une arête de src à dest
    graph[src].append((dest, weight))
    oriented = orienteoption.get()
    if oriented == 'Oui':
        oriented = True
    else:
        oriented = False
    # Si graphe non orienté, ajouter également une arête de dest à src
    if not oriented:
        graph[dest].append((src, weight))


def sliding(value):
    sommet_val.configure(text=int((value)))
count = 0

def random_exclude(range_start, range_end, excludes):
    r = random.randint(range_start, range_end)
    while r == excludes:
        r = random.randint(range_start, range_end)
    return r

def generate_graph():
    a = int(slide_sommet.get())
    b = int(poids.get())
    j = init_graph(a)
    for i in range(a):
        n = random.randint(1, 3)  # Générer un nombre aléatoire de voisins entre 1 et 3
        for _ in range(n):
            voisin = random_exclude(0, a-1, i)
            add_edge(j, i, voisin, random.randint(1, b))
    return j


graph = {}
def submit():

    global graph

    graph = generate_graph()

    G = nx.Graph()
    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors:
            G.add_edge(vertex, neighbor, weight=weight)


    pos = nx.spring_layout(G, k=0.2)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=10, node_color='skyblue', font_size=6, font_color='black', edge_color='gray', width=1.5)


    edge_labels = {(edge[0], edge[1]): edge[2]['weight'] for edge in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=5)
    edge_labels = {(edge[0], edge[1]): edge[2]['weight'] for edge in G.edges(data=True)}
    plt.savefig(os.path.join(dossier, "graph.png"))
    plt.close()

    graphique = customtkinter.CTkImage(Image.open("graph\\graph.png"), size=(500,375))
    afficher_image.configure(image = graphique)

generateframe = customtkinter.CTkFrame(tab1, fg_color="#2b2b2b")
generateframe.pack(anchor= N, side= LEFT)
default = customtkinter.CTkImage(Image.open("graph\\default.png"))
afficher_image = customtkinter.CTkLabel(generateframe, text = "", image= default)
afficher_image.pack(anchor = W, padx = 100, pady = (40) )

alea = customtkinter.CTkFrame(generateframe, width = 250, height=150, fg_color="#323232", corner_radius=20)
alea.pack(anchor = W, side = BOTTOM, padx = 100)
titrealea = customtkinter.CTkLabel(alea,text = "Saisir les paramètres :", font=('Bolder', 25), height=30)
titrealea.pack()
button_submit = customtkinter.CTkButton(alea, text = "Générer", command=submit)
button_submit.pack(side=BOTTOM, pady=(20,0))
slides = customtkinter.CTkFrame(alea, fg_color="#323232")
slides.pack(anchor= W,side= LEFT)
poidss= customtkinter.CTkFrame(alea, fg_color="#323232")
poidss.pack(anchor = W,side= LEFT)
slides_contenu = customtkinter.CTkFrame(slides, fg_color="#323232")
slides_contenu.pack(pady=(0,7))
orienteframe = customtkinter.CTkFrame(alea,fg_color="#323232" )
orienteframe.pack(anchor = W,side= LEFT)


sommetxt = customtkinter.CTkLabel(slides_contenu, text="Sommets :  ", font=("Helvetica", 20))
sommetxt.pack(side = LEFT)
sommet_val = customtkinter.CTkLabel(slides_contenu, text="", font=("Helvetica", 18))
sommet_val.pack(side = LEFT)
poidstxt = customtkinter.CTkLabel(poidss, text="Poids :  ", font=("Helvetica", 20))
poidstxt.pack()
orientetxt = customtkinter.CTkLabel(orienteframe, text="Orienté :  ", font=("Helvetica", 20))
orientetxt.pack()

poids = customtkinter.CTkEntry(poidss, placeholder_text="Entrez le poids")
poids.pack( padx = 10)
slide_sommet = customtkinter.CTkSlider(slides,
                                       from_ = 0,
                                       to=1000,
                                       command=sliding)
slide_sommet.pack(pady=(0,5))
slide_sommet.set(0)
oriente = ['Oui', 'Non']
orienteoption = customtkinter.CTkOptionMenu(orienteframe, values=oriente,)
orienteoption.pack()


##################################
# Menu Options 
##################################
optionsframe = customtkinter.CTkFrame(tab1, fg_color="#2b2b2b")
optionsframe.pack(anchor = E, side = RIGHT)
options = customtkinter.CTkTabview(optionsframe,
                            width = 500,
                            height=500,
                            fg_color='#323232',
                            border_color="#267390",
                            border_width=2,
                            corner_radius=16
                            )
options.pack()

dfs = options.add('DFS')
bfs = options.add('BFS')
chemin = options.add('Touver Chemin')
dijkstra = options.add('Dijkstra')
cycle = options.add('Chercher Cycle')

##################################
# Paramètres DFS
##################################

def recupererdebutdfs():
    depart = int(entrydfsdepart.get())
    result = dfsfonction(graph, depart, visites=None, resultat=None)
    string = f'Parcours en profondeur en partant\n du sommet {depart} : \n'
    for x in result:
        string += f'\n {x}'
    resultatfonctiondfs.configure(text= string)

def dfsfonction(graph, depart, visites=None, resultat=None):
    if visites is None:
        visites = set()
    if resultat is None:
        resultat = []

    visites.add(depart)
    resultat.append(depart)

    for voisin, _ in graph[depart]:
        if voisin not in visites:
            dfsfonction(graph, voisin, visites, resultat) 
    return resultat

dfstitre = customtkinter.CTkLabel(dfs, text="Parcourir le graphe en profondeur en partant d'un sommet", font=('bolder', 15))
dfstitre.pack(pady=(0,10))

dep_arv = customtkinter.CTkFrame(dfs, fg_color="#434343")
dep_arv.pack()
dfsdepart = customtkinter.CTkLabel(dep_arv, text="Départ :", font=("Helvetica", 20))
dfsdepart.pack()
entrydfsdepart = customtkinter.CTkEntry(dep_arv, placeholder_text="Sommet de départ")
entrydfsdepart.pack(padx = 10)

resultatdfs = customtkinter.CTkScrollableFrame(dfs, width= 300)
resultatdfs.pack()
resultatfonctiondfs = customtkinter.CTkLabel(resultatdfs, text = "", height=20)
resultatfonctiondfs.pack()

generate_dfs = customtkinter.CTkButton(dfs, text = "Rafraîchir", command=recupererdebutdfs)
generate_dfs.pack(pady=10)

##################################
# Paramètres BFS
##################################

def recupererdebutbfs():
    depart = int(entrybfsdepart.get())
    result = dfsfonction(graph, depart)
    string = f'Parcours en largeur en partant \n  du sommet {depart} : \n'
    for x in result:
        string += f'\n {x}'
    resultatfonctionbfs.configure(text= string)

def bfsfonction(graph, depart):
    visites = set([depart])
    file = deque([depart])
    resultat = []
    while file:
        sommet = file.popleft()
        resultat.append(sommet)
        for voisin, _ in graph[sommet]:
            if voisin not in visites:
                visites.add(voisin)
                file.append(voisin)
    return resultat

bfstitre = customtkinter.CTkLabel(bfs, text="Parcourir le graphe en largeur en partant d'un sommet", font=('bolder', 15))
bfstitre.pack(pady=(0,10))

dep_arvbfs = customtkinter.CTkFrame(bfs, fg_color="#434343")
dep_arvbfs.pack()
bfsdepart = customtkinter.CTkLabel(dep_arvbfs, text="Départ :", font=("Helvetica", 20))
bfsdepart.pack()
entrybfsdepart = customtkinter.CTkEntry(dep_arvbfs, placeholder_text="Sommet de départ")
entrybfsdepart.pack(padx = 10)

resultatbfs = customtkinter.CTkScrollableFrame(bfs, width=300)
resultatbfs.pack()
resultatfonctionbfs = customtkinter.CTkLabel(resultatbfs, text = "", height=20)
resultatfonctionbfs.pack()

generate_bfs = customtkinter.CTkButton(bfs, text = "Rafraîchir", command=recupererdebutbfs)
generate_bfs.pack(pady=10)

##################################
# Dijkstra
##################################
def construire_chemin(debut, fin, predecesseurs):
    chemin = []
    sommet_courant = fin
    try:

        while sommet_courant != debut:
            chemin.append(sommet_courant)
            sommet_courant = predecesseurs[sommet_courant]
        chemin.append(debut)

        return chemin
    except Exception as e:
        resultatfonctiondijkstra.configure(text = f'Aucun chemin possible du sommet {debut} à {fin}  ')
        



def calculdijkstra(graphe, debut):
    distances = {node: float('inf') for node in graphe}
    predecesseurs = {node: None for node in graphe}
    distances[debut] = 0
    sommets_visites = set()

    while sommets_visites != set(graphe):
        sommet_courant = min((node for node in graphe if node not in sommets_visites), key=lambda x: distances[x])
        sommets_visites.add(sommet_courant)

        for voisin, poids in graphe[sommet_courant]:
            dist_voisin = distances[sommet_courant] + poids
            if dist_voisin < distances[voisin]:
                distances[voisin] = dist_voisin
                predecesseurs[voisin] = sommet_courant

    return distances, predecesseurs

def entredijsktra():
    debut = int(dijkstraentrydepart.get())
    fin = int(dijkstraentryarrive.get())

    distance, predecesseurs = calculdijkstra(graph, debut)
    chemin = construire_chemin( debut, fin, predecesseurs)
    chemin.reverse()

    cheminstring = ''
    if chemin:
        for x in chemin:
            cheminstring += f'\n{x}'
        resultatfonctiondijkstra.configure(text = f'Avec une distance de {distance[fin]}, \n Voici le chemin le plus court \n du Sommet {debut} au Sommet {fin} : \n {cheminstring}  ')
        highlited = []

        highlited.append((chemin[0], chemin[1]))
        for i in range(2, len(chemin)):
            highlited.append((chemin[i-1], chemin[i]))
        
        G = nx.Graph()
        for vertex, neighbors in graph.items():
            for neighbor, weight in neighbors:
                G.add_edge(vertex, neighbor, weight=weight)


        pos = nx.spring_layout(G, k=0.2)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=10, node_color='skyblue', font_size=6, font_color='black', edge_color='gray', width=1.5)


        edge_labels = {(edge[0], edge[1]): edge[2]['weight'] for edge in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=5)
        for edge in highlited:
            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='red', width=2)

        plt.show()
    else :
        resultatfonctiondijkstra.configure(text = 'Aucun chemin trouvé ')
        
def obtenir_entree_sommet_valide(message, ordre):
    while True:
        entree = input(message)
        try:
            sommet = int(entree)
            if sommet == -1 or 0 <= sommet < ordre:
                return sommet
            else:
                print(f"Le numéro de sommet saisi n'est pas valide. Veuillez saisir un numéro de sommet entre 0 et {ordre - 1} ou -1 pour annuler.")
        except ValueError:
            print("Veuillez saisir un nombre entier valide ou -1 pour annuler.")

dijkstratitre = customtkinter.CTkLabel(dijkstra, text='Trouver le chemin le plus court entre 2 sommet distincts', font=('bolder', 15))
dijkstratitre.pack(pady=(0,10))
    
dijkstraframe = customtkinter.CTkFrame(dijkstra, fg_color="#434343")
dijkstraframe.pack()

dijkstradepart = customtkinter.CTkFrame(dijkstraframe, fg_color="#434343")
dijkstradepart.pack(side = LEFT, padx=20)

dijkstraarrive = customtkinter.CTkFrame(dijkstraframe, fg_color="#434343")
dijkstraarrive.pack(padx=20)

dijkstraentreetxt = customtkinter.CTkLabel(dijkstradepart, text="Départ :", font=("Helvetica", 20))
dijkstraentreetxt.pack()
dijkstraentrydepart = customtkinter.CTkEntry(dijkstradepart, placeholder_text="Sommet de départ")
dijkstraentrydepart.pack()

dijkstraarrivetxt = customtkinter.CTkLabel(dijkstraarrive, text="Arrivée:", font=("Helvetica", 20))
dijkstraarrivetxt.pack()
dijkstraentryarrive = customtkinter.CTkEntry(dijkstraarrive, placeholder_text="Sommet d'Arrivée")
dijkstraentryarrive.pack()


resultatdijkstra = customtkinter.CTkScrollableFrame(dijkstra,  width=300)
resultatdijkstra.pack()
resultatfonctiondijkstra = customtkinter.CTkLabel(resultatdijkstra, text = "", height=20)
resultatfonctiondijkstra.pack()

bouttondijkstra = customtkinter.CTkButton(dijkstra, text = "Rafraîchir", command=entredijsktra)
bouttondijkstra.pack(pady=10)
##################################
# Chemin
##################################

def trouver_chaine(graphe, depart, arrivee):
    visites = set()
    chemin = []

    def chercher_chemin(sommet_courant, arrivee, chemin):
        chemin.append(sommet_courant)
        if sommet_courant == arrivee:
            return True

        for voisin, _ in graphe[sommet_courant]:
            if voisin not in visites:
                visites.add(voisin)
                if chercher_chemin(voisin, arrivee, chemin):
                    return True

        chemin.pop()
        return False

    if chercher_chemin(depart, arrivee, chemin):
        return chemin
    else:
        return None

def entrechemin():
    debut = int(cheminentrydepart.get())
    fin = int(cheminentryarrive.get())

    resultat_chaine = trouver_chaine(graph, debut, fin)
    cheminchaine = ''
    if resultat_chaine:
        for x in resultat_chaine:
            cheminchaine += f'\n{x}'
        resultatfonctionchemin.configure(text = f"Chemin de {debut} à {fin} : \n {cheminchaine}")
    else:
        resultatfonctionchemin.configure(text = f"Aucun Chemin de {debut} à {fin}")


chemintitre = customtkinter.CTkLabel(chemin, text='Vérifier si le chemin est possible entre 2 sommet distincts', font=('bolder', 15))
chemintitre.pack(pady=(0,10))

cheminframe = customtkinter.CTkFrame(chemin, fg_color="#434343")
cheminframe.pack()

chemindepart = customtkinter.CTkFrame(cheminframe, fg_color="#434343")
chemindepart.pack(side = LEFT,  padx=20)

cheminarrive = customtkinter.CTkFrame(cheminframe, fg_color="#434343")
cheminarrive.pack(padx=20)

cheminentreetxt = customtkinter.CTkLabel(chemindepart, text="Départ :", font=("Helvetica", 20))
cheminentreetxt.pack()
cheminentrydepart = customtkinter.CTkEntry(chemindepart, placeholder_text="Sommet de départ")
cheminentrydepart.pack()

cheminarrivetxt = customtkinter.CTkLabel(cheminarrive, text="Arrivée:", font=("Helvetica", 20))
cheminarrivetxt.pack()
cheminentryarrive = customtkinter.CTkEntry(cheminarrive, placeholder_text="Sommet d'Arrivée")
cheminentryarrive.pack()


resultatchemin = customtkinter.CTkScrollableFrame(chemin,  width=300)
resultatchemin.pack()
resultatfonctionchemin = customtkinter.CTkLabel(resultatchemin, text = "", height=20)
resultatfonctionchemin.pack()

bouttonchemin = customtkinter.CTkButton(chemin, text = "Rafraîchir", command=entrechemin)
bouttonchemin.pack(pady=10)
##################################
# Rechercher cycle
##################################

    
def detecter_cycle(graphe):
    visites = set()
    pile = []

    def recherche_cycle(sommet, parent):
        visites.add(sommet)
        pile.append(sommet)

        for voisin, _ in graphe[sommet]:
            if voisin not in visites:
                if recherche_cycle(voisin, sommet):
                    return True
            elif parent is not None and voisin != parent:
                return True

        pile.pop()
        return False

    for sommet in graphe:
        if sommet not in visites:
            if recherche_cycle(sommet, None):
                return True
    return False

def entrecycle():
    a = detecter_cycle(graph)

    if a:
        resultatfonctioncycle.configure(text = f"Cycle trouvé")
    else:
        resultatfonctioncycle.configure(text = f"Aucun cycle trouvé")


cycletitre = customtkinter.CTkLabel(cycle, text='Vérifier il existe un cycle dans le graphe', font=('bolder', 15))
cycletitre.pack(pady=(0,10))

bouttoncycle = customtkinter.CTkButton(cycle, text = "Rafraîchir", command=entrecycle)
bouttoncycle.pack()

resultatfonctioncycle = customtkinter.CTkLabel(cycle, text = "", height=20, font=('bolder', 15))
resultatfonctioncycle.pack(pady = 20)


#########################################################################################################################################
# Métro
#########################################################################################################################################
metrolyon = customtkinter.CTkImage(light_image=Image.open('lyon.png'), size=(512,600))
metrolyonimage = customtkinter.CTkLabel(tab2, text="", image = metrolyon)
metrolyonimage.pack(anchor = W, side = LEFT, padx=100)
optionsframe = customtkinter.CTkFrame(tab2, fg_color="#2b2b2b")
optionsframe.pack(anchor = E, side = RIGHT)
options = customtkinter.CTkTabview(optionsframe,
                            width = 500,
                            height=500,
                            fg_color='#323232',
                            border_color="#267390",
                            border_width=2,
                            corner_radius=16
                            )
options.pack()

dfsmetro = options.add('DFS')
bfsmetro = options.add('BFS')
dijkstrametro = options.add('GPS')

def getgraphmetro():
    metro_lyon = nx.Graph()

    lignes = {
    'A': {
        ('Perrache', 'Ampère'): 3,
        ('Ampère', 'Bellecour'): 2,
        ('Bellecour', 'Cordeliers'): 2,
        ('Cordeliers', 'Hôtel de Ville'): 3,
        ('Hôtel de Ville', 'Foch'): 4,
        ('Foch', 'Charpennes'): 5,
        ('Charpennes', 'Masséna'): 3,
        ('Masséna', 'République - Villeurbanne'): 4,
        ('République - Villeurbanne', 'Gratte-Ciel'): 3,
        ('Gratte-Ciel', 'Flachet - Alain Gilles'): 4,
        ('Flachet - Alain Gilles', 'Cusset'): 3,
        ('Cusset', 'Laurent Bonnevay - Astroballe'): 3,
        ('Laurent Bonnevay - Astroballe', 'Vaulx-en-Velin - La Soie'): 4
    },
    'B': {
        ('Charpennes', 'Brotteaux'): 3,
        ('Brotteaux', 'Part-Dieu'): 2,
        ('Part-Dieu', 'Place Guichard'): 2,
        ('Place Guichard', 'Saxe - Gambetta'): 3,
        ('Saxe - Gambetta', 'Jean Macé'): 4,
        ('Jean Macé', 'Debourg'): 5
    },
    'C': {
        ('Hôtel de Ville', 'Croix-Paquet'): 3,
        ('Croix-Paquet', 'Croix-Rousse'): 2,
        ('Croix-Rousse', 'Hénon'): 3,
        ('Hénon', 'Cuire'): 4
    },
    'D': {
        ('Gorge de Loup', 'Vieux Lyon'): 2,
        ('Vieux Lyon', 'Bellecour'): 2,
        ('Bellecour', 'Saxe - Gambetta'): 3,
        ('Saxe - Gambetta', 'Guillotière - Gabriel Péri'): 2,
        ('Guillotière - Gabriel Péri', 'Sans Souci'): 3,
        ('Sans Souci', 'Grange Blanche'): 4,
        ('Grange Blanche', 'Laënnec'): 3,
        ('Laënnec', 'Mermoz - Pinel'): 3,
        ('Mermoz - Pinel', 'Parilly'): 4,
        ('Parilly', 'Gare de Vénissieux'): 3
    },
    'D bis': {
        ('Fourvière', 'Vieux Lyon'): 2,
        ('Vieux Lyon', 'Minimes'): 3,
        ('Minimes', 'St Just'): 3,
    }
    }
    for ligne, connexions in lignes.items():
        for stations, temps in connexions.items():
            metro_lyon.add_edge(*stations, weight=temps, ligne=ligne)
    return metro_lyon

lignesoption = ['A','B','C','D','D bis']
choisirligne = ['Choisir Ligne']
ligneA = ['Perrache', 'Ampère', 'Bellecour', 'Cordeliers', 'Hôtel de Ville','Foch', 'Charpennes', 'Masséna', 'République - Villeurbanne', 'Gratte-Ciel', 'Flachet - Alain Gilles', 'Cusset', 'Laurent Bonnevay - Astroballe', 'Vaulx-en-Velin - La Soie']
ligneB = ['Charpennes', 'Brotteaux', 'Part-Dieu', 'Place Guichard', 'Saxe - Gambetta', 'Jean Macé', 'Debourg']
ligneC = ['Hôtel de Ville','Croix-Paquet', 'Croix-Rousse','Hénon','Cuire']
ligneD = ['Gorge de Loup', 'Vieux Lyon', 'Bellecour', 'Saxe - Gambetta','Guillotière - Gabriel Péri', 'Sans Souci', 'Grange Blanche','Laënnec', 'Mermoz - Pinel', 'Parilly', 'Gare de Vénissieux']
ligneE = ['Fourvière','Vieux Lyon','Minimes','St Just']


##################################
# Paramètres DFS Métro
##################################

def changerlignedfs(choice):
    if choice == 'A':
        contenudfsligne.configure(values = ligneA)
    elif choice == 'B':
        contenudfsligne.configure(values = ligneB)
    elif choice == 'C':
        contenudfsligne.configure(values = ligneC)
    elif choice == 'D bis':
        contenudfsligne.configure(values = ligneE)
    elif choice == 'D':
        contenudfsligne.configure(values = ligneD)

def recupererdebutdfsmetro():
    visites = set()
    resultat = []
    depart = contenudfsligne.get()
    lignesgraph = getgraphmetro()
    dfsmetrofonction(depart,visites,resultat, lignesgraph)
    string = f"Parcours en profondeur en partant\n de l'arrêt {depart} :\n"
    for x in resultat:
        string += f'\n {x}'
    resultatfonctiondfsmetro.configure(text= string)

def dfsmetrofonction(noeud, visites, resultat, graphe):
    visites.add(noeud)
    resultat.append(noeud)
    for voisin in graphe.neighbors(noeud):
        if voisin not in visites:
            dfsmetrofonction(voisin, visites, resultat, graphe)

dfsmetrotitre = customtkinter.CTkLabel(dfsmetro, text="Parcourir le graphe en profondeur en partant d'un sommet", font=('bolder', 15))
dfsmetrotitre.pack(pady=(0,10))

dep_arvmetro = customtkinter.CTkFrame(dfsmetro, fg_color="#434343")
dep_arvmetro.pack()
dfsmetrodepart = customtkinter.CTkLabel(dep_arvmetro, text="Départ :", font=("Helvetica", 20))
dfsmetrodepart.pack()

entrydfsmetrodepart = customtkinter.CTkOptionMenu(dep_arvmetro, values=lignesoption, command=changerlignedfs)
entrydfsmetrodepart.pack(padx = 10, side = LEFT)
contenudfsligne = customtkinter.CTkOptionMenu(dep_arvmetro, values= ligneA)
contenudfsligne.pack(side = LEFT)

resultatdfsmetro = customtkinter.CTkScrollableFrame(dfsmetro, width= 300)
resultatdfsmetro.pack()
resultatfonctiondfsmetro = customtkinter.CTkLabel(resultatdfsmetro, text = "", height=20)
resultatfonctiondfsmetro.pack()

generate_dfsmetro = customtkinter.CTkButton(dfsmetro, text = "Rafraîchir", command=recupererdebutdfsmetro)
generate_dfsmetro.pack(pady=10)


##################################
# Paramètres BFS Métro
##################################

def changerlignebfs(choice):
    if choice == 'A':
        contenubfsligne.configure(values = ligneA)
    elif choice == 'B':
        contenubfsligne.configure(values = ligneB)
    elif choice == 'C':
        contenubfsligne.configure(values = ligneC)
    elif choice == 'D bis':
        contenubfsligne.configure(values = ligneE)
    elif choice == 'D':
        contenubfsligne.configure(values = ligneD)

def recupererdebutbfsmetro():
    depart = contenubfsligne.get()
    lignesgraph = getgraphmetro()
    resultat = bfsmetrofonction(lignesgraph, depart)
    string = f"Parcours en largeur en partant\n  de l'arrêt {depart} : \n"
    for x in resultat:
        string += f'\n {x}'
    resultatfonctionbfsmetro.configure(text= string)

def bfsmetrofonction(graphe, depart):
    visite = set([depart])
    file = deque([depart])
    resultat = []
    while file:
        sommet = file.popleft()
        resultat.append(sommet)
        for voisin in graphe.neighbors(sommet):
            if voisin not in visite:
                visite.add(voisin)
                file.append(voisin)
    return resultat

bfsmetrotitre = customtkinter.CTkLabel(bfsmetro, text="Parcourir le graphe en largeur en partant d'un sommet", font=('bolder', 15))
bfsmetrotitre.pack(pady=(0,10))

dep_arvmetro = customtkinter.CTkFrame(bfsmetro, fg_color="#434343")
dep_arvmetro.pack()
bfsmetrodepart = customtkinter.CTkLabel(dep_arvmetro, text="Départ :", font=("Helvetica", 20))
bfsmetrodepart.pack()

entrybfsmetrodepart = customtkinter.CTkOptionMenu(dep_arvmetro, values=lignesoption, command=changerlignebfs)
entrybfsmetrodepart.pack(padx = 10, side = LEFT)
contenubfsligne = customtkinter.CTkOptionMenu(dep_arvmetro, values= ligneA)
contenubfsligne.pack(side = LEFT)

resultatbfsmetro = customtkinter.CTkScrollableFrame(bfsmetro, width= 300)
resultatbfsmetro.pack()
resultatfonctionbfsmetro = customtkinter.CTkLabel(resultatbfsmetro, text = "", height=20)
resultatfonctionbfsmetro.pack()

generate_bfsmetro = customtkinter.CTkButton(bfsmetro, text = "Rafraîchir", command=recupererdebutbfsmetro)
generate_bfsmetro.pack(pady=10)



##################################
# Paramètres Dijkstra Métro
##################################

def changerlignedijkstra_depart(choice):
    if choice == 'A':
        contenudijkstralignedepart.configure(values = ligneA)
    elif choice == 'B':
        contenudijkstralignedepart.configure(values = ligneB)
    elif choice == 'C':
        contenudijkstralignedepart.configure(values = ligneC)
    elif choice == 'D bis':
        contenudijkstralignedepart.configure(values = ligneE)
    elif choice == 'D':
        contenudijkstralignedepart.configure(values = ligneD)

def changerlignedijkstra_arrive(choice):
    if choice == 'A':
        contenudijkstralignearrive.configure(values = ligneA)
    elif choice == 'B':
        contenudijkstralignearrive.configure(values = ligneB)
    elif choice == 'C':
        contenudijkstralignearrive.configure(values = ligneC)
    elif choice == 'D bis':
        contenudijkstralignearrive.configure(values = ligneE)
    elif choice == 'D':
        contenudijkstralignearrive.configure(values = ligneD)

def recupererdebutdijkstrametro():
    depart = contenudijkstralignedepart.get()
    arrive = contenudijkstralignearrive.get()
    lignesgraph = getgraphmetro()
    resultat = dijkstrametrofonction(lignesgraph, depart, arrive)
    string = f"Meilleur itiniéraire en partant\n de la station {depart} à la station {arrive} :\n"
    for x in resultat:
        string += f'\n {x}'
    resultatfonctiondijkstrametro.configure(text= string)

def dijkstrametrofonction(graphe, depart, arrivee):
    queue = set([depart])
    distances = {station: float('inf') for station in graphe.nodes()}
    distances[depart] = 0
    predecesseurs = {station: None for station in graphe.nodes()}

    while queue:
        courant = min(queue, key=lambda station: distances[station])
        queue.remove(courant)

        if courant == arrivee:
            break

        for voisin in graphe.neighbors(courant):
            alt_route = distances[courant] + graphe[courant][voisin]['weight']
            if alt_route < distances[voisin]:
                distances[voisin] = alt_route
                predecesseurs[voisin] = courant
                queue.add(voisin)

    chemin, courant = deque(), arrivee
    while predecesseurs[courant] is not None:
        chemin.appendleft(courant)
        courant = predecesseurs[courant]
    chemin.appendleft(depart)
    return list(chemin)

dijkstrametrotitre = customtkinter.CTkLabel(dijkstrametro, text="Trouver le meilleur itinéraire possible entre 2 stations", font=('bolder', 15))
dijkstrametrotitre.pack(pady=(0,10))

departmetro = customtkinter.CTkFrame(dijkstrametro, fg_color="#434343")
departmetro.pack()
dijkstrametrodepart = customtkinter.CTkLabel(departmetro, text="Départ :", font=("Helvetica", 20))
dijkstrametrodepart.pack()

entrydijkstrametrodepart = customtkinter.CTkOptionMenu(departmetro, values=lignesoption, command=changerlignedijkstra_depart)
entrydijkstrametrodepart.pack(padx = 10, side = LEFT)
contenudijkstralignedepart = customtkinter.CTkOptionMenu(departmetro, values= ligneA)
contenudijkstralignedepart.pack(side = LEFT)

arrivemetro = customtkinter.CTkFrame(dijkstrametro, fg_color="#434343")
arrivemetro.pack()
dijkstrametroarrive = customtkinter.CTkLabel(arrivemetro, text="Arrivée :", font=("Helvetica", 20))
dijkstrametroarrive.pack()

entrydijkstrametroarrive = customtkinter.CTkOptionMenu(arrivemetro, values=lignesoption, command=changerlignedijkstra_arrive)
entrydijkstrametroarrive.pack(padx = 10, side = LEFT)
contenudijkstralignearrive = customtkinter.CTkOptionMenu(arrivemetro, values= ligneA)
contenudijkstralignearrive.pack(side = LEFT)

resultatdijkstrametro = customtkinter.CTkScrollableFrame(dijkstrametro, width= 300)
resultatdijkstrametro.pack()
resultatfonctiondijkstrametro = customtkinter.CTkLabel(resultatdijkstrametro, text = "", height=20)
resultatfonctiondijkstrametro.pack()

generate_dijkstrametro = customtkinter.CTkButton(dijkstrametro, text = "Rafraîchir", command=recupererdebutdijkstrametro)
generate_dijkstrametro.pack(pady=10)




root.mainloop()