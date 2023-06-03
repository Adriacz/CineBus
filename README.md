# CineBus
La pràctica CineBus consisteix en 4 mòduls implementats en python(```billborad.py```, ```bus.py```, ```city.py```, ```demo.py```)

El usuaris podran interactuar amb l'aplicació a través del demo. Aquest ofereix una Cinebus a través del demo, que ofereix una interfície interactiva per tal que usuaris puguin observar les característiques de les pel·lícules que es projecten als cinemes de Barcelona (director,actors,gènere...), així com, la ruta més ràpida per arribar al cinema on la fan des de la posició actual de l'usuari.

## Getting Started

Aquestes instruccions permetran que una còpia del projecte estigui en funcionament a la màquina local amb finalitats de desenvolupament i proves.

### Requisits previs
Per instal·lar el projecte, s'hauria de tenir instal·lat ```pip``` per tal de poder instal·lar tots els paquets necessaris descrits a ```requirements.txt```  

### Instal·lació

El fitxer ```.zip``` conté els següents fitxers:

- ```barcelona.grf``` - el graf dels carrers de Barcelona

- ```city.py``` - conté el codi que crea fusiona els graf dels busos amb el graf dels carrers de Barcelona i la cerca de les rutes més ràpides entre dos punts de la ciutat. 

- ```buses.py``` - conté el codi per construir el graf de busos.

- ```billboard.py``` - conté el codi per obtenir les dades a través de la web dels cinemes de Barcelona i les pel·lícules que emeten i les característiques d'aquestes. 

- ```demo.py``` - conté el codi  que genera l'interficíe interactiva per tal que l'usuari pugui cercar les dades sobre les pel·lícules i cinemes de Barcelona, així com indicar la ruta més ràpida per arribar al cinema escollit per veure la pel·lícula.

- ```requirements.txt``` - Fitxer que conté tots els paquets  necessaris per a l'execució del programa.

- ```README.md``` - documentació de la pràctica.

- ```*.png``` - imatges adjuntades pel README.md.


Per instal·lar els paquets necessaris del Cinebus cal accedir al terminal i usar la comanda ```pip install ``` seguinda del nom de la llibreria. També es poden instal·lar tots ràpidament usant ```requirements.txt```. Per fer-ho cal anar al mateix directori on es troba el requirements.txt i executar la comanda:

```python
$ pip install -r requirements.txt
```

## Paquets necessaris

Els paquets principals descrits en el ```requirements.txt``` i les seves funcionalitats bàsiques implementades als nostres mòduls són els següents:

```requests``` - usat per baixar-se fitxers de dades.

````beautifulsoup``` per llegir dades dels arbres HTML.

```networkx``` - usat per crear i manipular grafs.

```osmnx``` - usat per obtenir grafs de localitzacios (Barcelona).

```haversine``` - usat per calcular distàncies entre coordenades.

```staticmap``` - usat per pintar mapes.

## Mòdul ```billboard.py```

El mòdul billboard s'encarrega d'aconseguir les dades de tots els cinemes de Barcelona i les seves cartelleres.

La funció principal del programa és ```read``` la qual obté les dades dels arbres HTML a través de la pàgina web Sensacine i retorna dades tipus Billboard les quals contenen les pel·lícules, cinemes i projeccions.

## Mòdul ```buses.py```

El mòdul buses s'encarrega de crear graf de busos a partir de les dades llegides d'un fitxer ```.json``` obtingut a la AMB. Els nodes del graf representen les parades de bus, i les arestes el recorregut traçat pel bus de parada a parada.


**Funcions principals del buses**

***get_buses_graph***

***Show***

***Plot***


## Mòdul ```city.py```

***get_osmnx_praph***

***save_osmnx_graph***

***load_osmnx_graph***

***build_city_graph***


***find_path***


***show***


***plot***

## Mòdul ````bot.py```

## Execució dels testos´

### Mòdul ```billboard.py```

### Mòdul ```buses.py```


### Mòdul ```city.py```


### Mòdul ```demo.py```

## Autors 
- Andreu Fernández Cubí 
- Adrià Capdevila Zurita