# 🚇 GPS & Traitement de Graphes — Métro de Lyon

Une application de bureau qui rend les **algorithmes de graphes visibles** : on
génère un graphe, on lance un parcours, on regarde le résultat se dessiner. Puis
on applique exactement les mêmes algorithmes au **vrai réseau du métro de Lyon**
pour calculer un itinéraire.

Interface **CustomTkinter**, graphes dessinés avec **networkx + matplotlib**.

> Projet universitaire (théorie des graphes). Les algorithmes sont **implémentés à
> la main** — networkx ne sert qu'à l'affichage, jamais au calcul. C'était tout
> l'intérêt de l'exercice.

## Deux onglets

### 1. Tests unitaires — le bac à sable

Génère un graphe aléatoire (ordre réglable par curseur), puis :

| Algorithme | Ce qu'il répond |
|---|---|
| **Parcours en profondeur** (DFS) | Dans quel ordre visite-t-on tout depuis un sommet ? |
| **Parcours en largeur** (BFS) | Idem, mais par cercles concentriques (file `deque`) |
| **Dijkstra** | Quel est le plus court chemin entre deux sommets pondérés ? |
| **Recherche de chaîne** | Existe-t-il un chemin entre A et B ? |
| **Détection de cycle** | Le graphe contient-il un circuit ? |

Le graphe est redessiné à chaque étape (`graph/graph.png`) avec les poids des
arêtes affichés.

### 2. Métro de Lyon — le cas réel

Le réseau lyonnais est chargé comme un graphe pondéré (les stations sont les
sommets, les temps de trajet les poids). On choisit une ligne, une station de
départ et d'arrivée, et **Dijkstra calcule l'itinéraire** — le même code que dans
le bac à sable, appliqué à une vraie carte.

DFS et BFS sont également disponibles sur le réseau, pour explorer la desserte
depuis une station.

## Lancer

Prérequis : **Python 3.11+**

```bash
pip install customtkinter networkx matplotlib pillow
cd Main
python main.py
```

> Sous Linux/macOS : le code construit certains chemins d'images à la Windows
> (`graph\graph.png`). Si l'affichage du graphe échoue, c'est de là que ça vient.

## Structure

| Fichier | Rôle |
|---|---|
| `Main/main.py` | Toute l'application : interface, algorithmes, réseau du métro |
| `Main/graph/` | Images des graphes régénérées à chaque calcul |
| `Main/lyon.png` | Fond de carte |
| `Main/main.spec` | Spec PyInstaller (build d'un exécutable) |

## Ce que j'en retiens

Tout tient dans un seul `main.py` de 800 lignes, interface et logique mélangées :
c'est le principal défaut du projet. Séparer les algorithmes (purs, testables) de
l'affichage aurait permis de les tester sans ouvrir une fenêtre — et c'est
exactement ce que je ferais aujourd'hui.

## Licence

[MIT](LICENSE)
