# CineBus
Tria pel·li i vés-hi en bus! 🚌 🎞️

## Introducció
La pràctica CineBus consisteix en 4 mòduls implementats en python(```billborad.py```, ```bus.py```, ```city.py```, ```demo.py```)

Els usuaris podran interactuar amb l'aplicació a través del programa principal demo. Aquest ofereix una interfície interactiva per tal que usuaris puguin observar les característiques de les pel·lícules que s'emeten als cinemes de Barcelona (director, actors, gènere...), així com, la ruta més ràpida per arribar al cinema on la fan des de la posició i hora actual de l'usuari.

### Requisits previs
Per instal·lar el projecte, s'hauria de tenir instal·lat ```python``` i disposar de ```pip``` per poder instal·lar tots els paquets necessaris descrits a ```requirements.txt```  

### Instal·lació

El fitxer ```.zip``` conté els següents fitxers:

- ```barcelona.grf``` - el graf dels carrers de Barcelona

- ```city.py``` - conté el codi que crea el graf de la ciutat fusionant el graf dels busos amb el graf dels carrers de Barcelona. També inclou la cerca de la ruta més ràpida entre dos punts de la ciutat. 

- ```buses.py``` - conté el codi per construir el graf de busos.

- ```billboard.py``` - conté el codi per obtenir les dades a través de la web dels cinemes de Barcelona i les pel·lícules que emeten i les característiques d'aquestes. 

- ```demo.py``` - conté el codi  que genera l'interfície interactiva per tal que l'usuari pugui cercar les dades sobre les pel·lícules i cinemes de Barcelona, així com indicar la ruta més ràpida per arribar al cinema escollit per veure la pel·lícula.

- ```requirements.txt``` - Fitxer que conté tots els paquets  necessaris per a l'execució del programa.

- ```README.md``` - documentació de la pràctica.

- ```*.png``` - imatges adjuntades pel README.md.


Per instal·lar els paquets necessaris del Cinebus cal accedir al terminal i usar la comanda ```pip install ``` seguinda del nom de la llibreria. També es poden instal·lar tots ràpidament fent servir ```requirements.txt```. Per fer-ho cal anar al mateix directori on es troba el requirements.txt i executar la comanda:

```python
$ py -m pip install -r requirements.txt
```

## Paquets necessaris

Els paquets principals descrits en el ```requirements.txt``` i les seves funcionalitats bàsiques implementades als nostres mòduls són els següents:

```requests``` - Per baixar-se fitxers de dades.

```beautifulsoup```- Per llegir dades dels arbres HTML.

```networkx``` - Per crear i manipular grafs.

```osmnx``` - Per obtenir grafs de localitzacios (Barcelona).

```haversine``` - Per calcular distàncies entre coordenades.

```staticmap``` - Per pintar mapes.

## Mòdul ```billboard.py```

El mòdul ```billboard``` s'encarrega d'aconseguir les dades de tots els cinemes de Barcelona i les seves cartelleres mitjançant el web scraping.

La funció principal del programa és ```read``` la qual obté les dades dels arbres HTML a través de la pàgina web Sensacine i retorna dades que pertanyen a la classe Billboard que contene les pel·lícules, cinemes i projeccions.

Addicionalment, s'ha implementat un conjunt de funcions que apliquen filtres de cerca per tal de facilitar a l'usuari trobar la informació segons les seves preferències. 

## Mòdul ```buses.py```

El mòdul ```buses``` s'encarrega de crear un graf no dirigit de les línies d'autobús de Barcelona a partir de les dades llegides d'un fitxer ```.json``` de la AMB. Els nodes del graf representen les parades de bus, i les arestes el recorregut traçat pel bus de parada a parada. 

Els nodes (class) guarden informació sobre les característiques de la parada, com les seves coordenades i a través dels pesos de les arestes es calcula les distàncies entre parades. 

El mòdul proporciona dues accions per visualitzar els resultats en una imatge. 
- L'acció ```show``` mostra interactivament en una finestra el graf de busos. 
- L'acció ```plot``` guarda en una imatge el graf de busos amb el mapa de Barcelona de fons. 

## Mòdul ```city.py```

El mòdul ```city``` és el responsable de proporcionar el **graf de la ciutat** que conté tota la informació necessària per torbar la ruta més ràpida entre dos punts de Barcelona, sigui amb autobús o a peu. El graf de la ciutat és producte de la fusió de dos grafs: El graf de Barcelona (obtingut del mòdul ```osmnx```) i el graf de busos (```buses.py```)  

Per tal de millorar l'eficiència del programa s'ha dissenyat de manera que el graf de la ciutat només es generi un cop i queda guardat en un fitxer per utilitzar-lo posteriorment. 

El graf de la ciutat té com a nodes totes les cruïlles i parades de bus. I les arestes marquen els camins.

Per tal de torbar la ruta més ràpida per anar a veure una pel·lícula s'ha implementat un Dijkstra.

El mòdul proporciona accions per visualitzar els resultats en una imatge. 
- El```show``` mostra interactivament en una finestra el graf de la ciutat. 
- El ```plot``` guarda en una imatge el graf de la ciutat amb el mapa de Barcelona de fons. 
- El ```plot_path``` permet veure una imatge de la ruta a seguir per arribar a la destinació. 

## Mòdul ```demo.py```

El mòdul ```demo``` és el programa principal i permet interactuar amb l'usuari. Inclou la visualització de la cartellera de pel·lícules la qual podem aplicar filtres per facilitar la cerca.
També mostra el graf de busos i de la ciutat. 
Permet a l'usuari veure la ruta més ràpida per veure la pel·lícula escollida a un cinema i mostra el camí a seguir amb bus o a peu. 

## Autors 
- Andreu Fernández Cubí 
- Adrià Capdevila Zurita