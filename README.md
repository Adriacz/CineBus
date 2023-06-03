# CineBus
La pràctica CineBus consisteix en 4 mòduls implementats en python(```billborad.py```, ```bus.py```, ```city.py```, ```demo.py```)

Amb el bot de telegram, els usuaris tindran l'oportunitat de buscar restaurants segons els requisits que tinguin (lloc, gustos...), veure la informació dels restaurants, així com, si es desitja, veure la ruta més ràpida per arribar al destí escollit (restaurant), des de la posició actual de l'usuari.

## Getting Started

Aquestes instruccions permetran que una còpia del projecte estigui en funcionament a la màquina local amb finalitats de desenvolupament i proves.

### Prerequisites
Per instal·lar aquest projecte, s'hauria de tenir instal·lat ```pip3``` per tal de poder instal·lar tots els paquets necessaris del ```requirements.txt``` (adjuntat en el fitxer ```.zip``` del treball). 


### Installing

El fitxer ```.zip``` conté els següents fitxers:

- ```barcelona.gpickle``` - El graf dels carrers de Barcelona guardat, per no haver-lo de crear cada cop.

- ```restaurants.csv```, ```estacions.csv```, ```accessos.csv``` - fitxers amb totes les dades necessàries per crear els grafs.

- ```restaurants.py``` - conté tot el codi relacionat amb l'obtenció de la llista de restaurants i les cerques corresponents per a trobar restaurants desitjats.

- ```metro.py``` - conté tot el codi relacionat amb la construcció del graf del metro.

- ```city.py``` - conté tot el codi relacionat amb la construcció del graf de la ciutat i la cerca de les rutes més ràpides entre dos punts de la ciutat. 

- ```bot.py``` - conté tot el codi relacionat amb el bot de Telegram, la seva funció és recomanar 12 restaurants a l'usuari, donar la informació d'algun d'aquests 12 restaurants (si així es demana), així com, indicar la ruta més ràpida fins al restaurant escollit.

- ```requirements.txt``` - Fitxer que conté tots els paquets que es necessiten per a l'execució.

- ```README.md``` - documentació del fitxer.

- ```images``` - imatges utilitzades en el README.md.

--- 

Els paquets principals que es troben en el ```requirements.txt``` i les seves funcionalitats bàsiques en els nostres mòduls són els següents:

```networkx``` - usat per manipular grafs.

```osmnx``` - usat per obtenir grafs de llocs (Barcelona).

```haversine``` - usat per calcular distàncies entre coordenades.

```staticmap``` - usat per pintar mapes.

```python-telegram-bot``` - usat per a poder interactuar amb el Telegram.

```pandas``` - usat per llegir fitxers CSV.

```fuzzysearch``` - usat per a fer la cerca difusa.

Per instal·lar els paquets necessaris per al projecte es pot utilitzar a la terminal la següent comanda. Per fer-ho s'ha d'estar en el mateix directori on es troba el requirements.txt.

```python
$ pip3 install -r requirements.txt
```