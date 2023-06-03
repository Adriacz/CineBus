import billboard as bb
import buses as bs
import city
from PIL import Image
from osmnx import geocoder
from typing import List, Tuple, Optional
from functools import cmp_to_key



class CineBus:
    g_walk: city.OsmnxGraph
    g_bus: bs.BusesGraph
    g_city: city.CityGraph
    bill: bb.Billboard

    def __init__(self, g_walk: city.OsmnxGraph, g_bus: bs.BusesGraph, g_city: city.CityGraph, bill: bb.Billboard) -> None:
        self.g_walk = g_walk
        self.g_bus = g_bus
        self.g_city = g_city
        self.bill = bill

    def _print_films_table(self) -> None:
        #bill = bb.read()
        for film in self.bill.films:
            print(film.title,
                "\nDirector:", *film.director, 
                "\nActors:", *film.actors, 
                "\nGèneres:", *film.genre)
            print(5*"-")
        input('Torna al menú')

    def _print_cinemas_table(self) -> None:

        for cine in self.bill.cinemas:
            print(cine.name)
            print(cine.address)
            print(5*"-")

    def _print_projections_table(self, projections: Optional[List[bb.Projection]] = None) -> None:
        if projections is None:
            projections = self.bill.projections

        if len(projections) == 0:
            print("NO S'HAN TROBAT RESULTATS")

        for proj in projections:
            if proj.time[1] < 10:
                mins = "00"
            else:
                mins = str(proj.time[1])
            time = str(proj.time[0]) + ":" + mins
            print(proj.film.title, 
                  "\nCinema: ", proj.cinema.name,
                  "\nHora:", time,
                  "\nGènere/s:", *proj.film.genre,
                  "\nLlengua:", proj.language)
            print(5*"-")

    def _show_billboard(self)-> None: 
        """"""
        print("1. Mostra les pel·lícules\n"
              "2. Mostra els cinemes\n"
              "3. Mostra les projeccions\n"
              "4. Torna al inici")
        
        op2 = int(input("Escull: "))
        while op2 != 4:
            if op2 == 1:
                self._print_films_table()
            elif op2 == 2:
                self._print_cinemas_table()
            elif op2 == 3:
                self._print_projections_table()

            print(20*"-")
            print("1. Mostra les pel·lícules\n"
              "2. Mostra els cinemes\n"
              "3. Mostra les projeccions\n"
              "4. Torna al inici")
            op2 = int(input("Escull: "))
            
        
    def _search_in_billboard(self) -> None: 
        op = 0
        filtered_projs = self.bill.projections

        print(10*"-")
        print("TRIA UN FILTRE:",
        "1. Filtra per nom de pel·lícula", 
        "2. Filtra per gènere",
        "3. Filtra per director",
        "4. Filtra per actor",
        "5. Filtra per nom de cinema", 
        "6. Filtra per hora (amb format HH:MM)",
        "7. Filtra per idioma (Spanish o VO)",
        "8. Torna al menú", 
        sep="\n")
        print(10*"-")
        op = int(input())

        while op != 8:
            filter = input("Introdueix el filtre: ")
            print()
            if op == 1:
                filtered_projs = search_by_title(filter, filtered_projs)
                self._print_projections_table(filtered_projs)
            elif op == 2:
                filtered_projs = search_by_genre(filter, filtered_projs)
                self._print_projections_table(filtered_projs)
            elif op == 3:
                filtered_projs = search_by_director(filter, filtered_projs)
                self._print_projections_table(filtered_projs)
            elif op == 4:
                filtered_projs = search_by_actor(filter, filtered_projs)
                self._print_projections_table(filtered_projs)
            elif op == 5:
                filtered_projs = search_by_cinema(filter, filtered_projs)
                self._print_projections_table(filtered_projs)
            elif op == 6:
                time = filter.split(":")
                h, min = int(time[0]), int(time[1])
                filtered_projs = search_by_time((h, min), filtered_projs)
                self._print_projections_table(filtered_projs)
            elif op == 7:
                filtered_projs = search_by_language(filter, filtered_projs)
                self._print_projections_table(filtered_projs)
            print()
            print(10*"-")
            print("AFEGEIX UN ALTRE FILTRE:",
            "1. Filtra per nom de pel·lícula", 
            "2. Filtra per gènere",
            "3. Filtra per director",
            "4. Filtra per actor",
            "5. Filtra per nom de cinema", 
            "6. Filtra per hora (hh:mm)",
            "7. Filtra per idioma (Spanish o VO)",
            "8. Torna al menú", 
            sep="\n")
            op = int(input())


    def _show_buses_graph(self) -> None: 
        print("Tria l'opció", 
              "1. Graf de busos sense el mapa de Barcelona",
              "2. Graf de busos sobre el mapa de Barcelona",
              "3. Torna al menú", sep="\n")
        op2 = int(input())
        if op2 == 1:
            bs.show(self.g_bus)
        else: 
            imagebuses = Image.open("BusGraph.png")  
            imagebuses.show()  

        
    def _show_city_graph(self) -> None: 

        imagecity = Image.open("CityGraph.png")  
        imagecity.show()  


    def _show_path(self, p: city.Path) -> None:
        city.plot_path(self.g_city, p, "Path.png")
        imageplot = Image.open("Path.png")
        imageplot.show()

    def search_route(self)-> None:
        """"""
        #L'usuari introdueix quina peli vol i a partir de quina h la vol veure
        film = input("Pel·lícula: ")
        time = input("Hora de sortida (hh:mm): ").split(":")
        initial_time = (int(time[0]), int(time[1]))

        #L'usuari introdueix l'ubicació actual
        print("Indica el punt de sortida")
        print("1. Buscar per coordenades")
        print("2. Buscar per ubicació actual")
        op2 = int(input())
        while op2 != 1 and op2 != 2:
            print("Error al introduir el número")
            print("1. Buscar per coordenades")
            print("2. Buscar per ubicació actual")
            op2 = int(input())

        if op2 == 1:
            coord_x = float(input("Introdueix la longitud (x): "))
            coord_y = float(input("Introdueix la latitud (y): "))
            initial_coord = coord_x, coord_y          
        elif op2 == 2:
            ubi = str(input("Introdueix l'ubicació actual"))
            try: 
                initial_coord = geocoder.geocode(ubi)
            except:
                print("Error a l'introduir la direcció")           

        #Mirem quin cinema la fa més aviat
        possible_projections = search_by_time(initial_time, search_by_title(film, self.bill.projections))
        possible_projections.sort(key=cmp_to_key(compare_by_time))
        projection: Optional[bb.Projection] = None
        try:
            i = 1
            assert possible_projections
            curr_cine_adress = possible_projections[0].cinema.address
            curr_cine_coord = geocoder.geocode(curr_cine_adress)
            curr_path, curr_time = city.find_path_and_time(self.g_walk, self.g_city, initial_coord, curr_cine_coord)
            while not projection and i < len(possible_projections):
                if curr_cine_adress != possible_projections[i].cinema.address:
                    curr_cine_adress = possible_projections[i].cinema.address
                    curr_cine_coord = geocoder.geocode(curr_cine_adress)
                    curr_path, curr_time = city.find_path_and_time(self.g_walk, self.g_city, initial_coord, curr_cine_coord)
                    arrival = (initial_time[0] + curr_time //60, (initial_time[1] + curr_time)%60)
                    if arrival[0] < possible_projections[i].time[0] or (arrival[0] == possible_projections[i].time[0] and arrival[1] <= possible_projections[i].time[0]):
                        projection = possible_projections[i]
                i += 1

            assert projection is not None
            city.plot_path(self.g_city, curr_path, "path.png")
            print(10*"-", "\nLa millor opció per veure avui la pel·lícula", film, "a partir de les", time, "és:", "\n-----")
            print("CINEMA:", projection.cinema.name, projection.cinema.name, projection.cinema.address, sep="\n")
            print("HORA D'INICI:\n", projection.time[0], ":", projection.time[1], "\nTEMPS DEL RECORREGUT:\n", curr_time, " minuts\n", "VEURE RECORREGUT: apreta enter", sep="")
            input()
            self._show_path(curr_path)        
            #intentar implementar dir quines línies de bus s'han d'agafar
        except AssertionError:
            print("No s'ha trobat cap projecció que coincideixi amb la teva cerca")


    def process_command(self, op: int):
        """"""
        if op == 1:
            self._show_billboard()
        elif op == 2:
            self._search_in_billboard()
        elif op == 3:
            self._show_buses_graph()
        elif op == 4:
            self._show_city_graph()
        elif op == 5:
            self.search_route()
        elif op != 6: 
            print("Comanda incorrecta")



def compare_by_time(p1: bb.Projection, p2: bb.Projection) -> int:
    if p1.time[0] != p2.time[1]:
        return p1.time[0] - p2.time[0]
    return p1.time[1] - p2.time[1]

def search_by_title(title: str, projections: List[bb.Projection]) -> List[bb.Projection]:
    filter = title.lower()
    return [projection for projection in projections if filter in projection.film.title.lower()]

def search_by_genre(genre: str, projections: List[bb.Projection]) -> List[bb.Projection]:
    filter = genre.lower()
    return [projection for projection in projections if any(filter in g.lower() for g in projection.film.genre)]

def search_by_actor(actor: str, projections: List[bb.Projection]) -> List[bb.Projection]:
    filter = actor.lower()
    return [projection for projection in projections if any(filter in a.lower() for a in projection.film.actors)]

def search_by_director(director: str, projections: List[bb.Projection]) -> List[bb.Projection]:
    filter = director.lower()
    return [projection for projection in projections if any(filter in d.lower() for d in projection.film.director)]

def search_by_cinema(name: str, projections: List[bb.Projection]) -> List[bb.Projection]:
    filter = name.lower()
    return [projection for projection in projections if filter in projection.cinema.name.lower()]

def search_by_time(filter: Tuple[int, int], projections: List[bb.Projection]) -> List[bb.Projection]:
    return [projection for projection in projections if (filter[0] < projection.time[0]) or (filter[0] == projection.time[0] and filter[1] <= projection.time[1])]                        

def search_by_language(language: str, projections: List[bb.Projection]) -> List[bb.Projection]:
    filter = language.lower()
    return [projection for projection in projections if filter in projection.language.lower()]
                        


def create_buses_graph() -> bs.BusesGraph:
    """"""
    graph = bs.get_buses_graph()
    bs.plot(graph, nom_fitxer="BusGraph.png")
    return graph

def create_walking_graph() -> city.OsmnxGraph:
    return city.load_osmnx_graph(filename="citygraph.grf")    

def create_city_graph(g1: city.OsmnxGraph, g2: bs.BusesGraph) -> city.CityGraph:
    """"""
    g = city.build_city_graph(g1, g2)
    city.plot(g, "CityGraph.png")
    return g

def read_billboard()-> bb.Billboard:
    """"""
    return bb.read()


def main()-> None:   
    g_buses = create_buses_graph()
    g_walk = create_walking_graph()
    g_city = create_city_graph(g_walk, g_buses)
    bill = read_billboard()
    op = 1
    cinebus = CineBus(g_walk, g_buses, g_city, bill)
    
    while op != 6:
        print("", 20*"-", sep="\n")
        print("Cinebus\nAutors: Andreu Fernández i Adrià Capdevila")
        print("1. Mostra la cartellera",
              "2. Cerca la cartellera", 
              "3. Mostra el graf de busos",
              "4. Mostra el graf de la ciutat",
              "5. Busca ruta",
              "6. Surt", sep="\n")
        op = int(input())
        cinebus.process_command(op)
        print()
        
if __name__ == "__main__":
    main()


# 1) Fer Traductor 
# 2) Funció passi adreça cine a cood geocode 
# 3) A partir path obtenir en temps, i imprimir durada minima del trajecte  --> Fer funció city


