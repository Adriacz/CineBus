from bs4 import BeautifulSoup
import requests
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
#import pdb; pdb.set_trace() per comprovar

@dataclass 
class Film: 
    title: str
    genre: List[str]
    director: List[str]
    actors: List[str]

@dataclass 
class Cinema: 
    name: str
    address: str

@dataclass 
class Projection: 
    film: Film
    cinema: Cinema
    time: Tuple[int, int]   # hora:minut
    language: str

@dataclass 
class Billboard: 
    films: list[Film]
    cinemas: list[Cinema]
    projections: list[Projection]


def process_film(film: Dict[str, Any]) -> Film:
    return Film(film["title"], film["genre"], film["directors"], film["actors"])


def process_projection(film: Film, cine: Cinema, time: str, version: str) -> Projection:
    listed_time = time.split(":")
    listed_version = version.split(",")

    if listed_version[0] == "Versión Original":
        language = "VO"
    else:
        language = "Spanish"

    return Projection(film, cine, (int(listed_time[0]), int(listed_time[1])), language)

def traduce_adress(adress: str) -> str:
    """Tradueix una adressa txt en una adressa admisible per la llibreria osmnx"""

    words: list[str] = adress.split()
    # canvis necessaris per cada paraula:
    for i in range(len(words)):
        if words[i].lower() == "calle":
            words[i] = "carrer"
        elif words[i].lower() == "avenida":
            words[i] = "avinguda"
        elif words[i].lower() == "paseig" or words[i].lower() == "paseo":
            words[i] = "passeig"
        elif words[i].lower() == "sta":
            words[i] = "carrer de santa"
        elif words[i] == "s/n":
            words[i] = ""
    return ' '.join(words)


def read() -> Billboard:


    films_dict: Dict[str, Film] = dict()
    cinemas_dict: Dict[str, Cinema] = dict()
    projections_list: list[Projection] = list()

    urls = ["https://www.sensacine.com/cines/cines-en-72480/?page=1","https://www.sensacine.com/cines/cines-en-72480/?page=2","https://www.sensacine.com/cines/cines-en-72480/?page=3"]
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # nomes 1 dia 
        #carta = soup.find_all("div", class_="tabs_box_pan item-0")
        #for pelis in carta:  # Arreglar dir andreu
        cines = soup.find_all("div", class_="margin_10b j_entity_container")
        for cine in cines:
            #processar el cinema
            name_class = cine.find("h2", class_="tt_18")
            name = name_class.find("a").get_text().replace("\n", "")
            adress = cine.find_all("span", class_="lighten")[1].text.replace("\n", "") 
            if "Barcelona" in adress:
                cinemas_dict[name] = Cinema(name, traduce_adress(adress))
            
            
            #buscar items-resa
        days1 = soup.find_all("div", class_="tabs_box_pan item-0")
        for day1 in days1:
            pelis = day1.find_all("div", class_ = "item_resa")
            for peli in pelis:
                jw = peli.find("div", class_="j_w")
                film_info = json.loads(jw.get("data-movie"))
                film = process_film(film_info)
                films_dict[film.title] = film

                cinema_info = json.loads(jw.get("data-theater"))
                cinema_name = cinema_info["name"]

                if cinema_name in cinemas_dict.keys():
                    version = jw.find("span", class_="bold").get_text()
                    for em in peli.find_all("em"):
                        times = em.get("data-times")
                        times_dict = json.loads(times)
                        projections_list.append(process_projection(film, cinemas_dict[cinema_name.rstrip()], times_dict[0], version))

    return Billboard(list(films_dict.values()), list(cinemas_dict.values()), projections_list)

bill = read()