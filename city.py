"""
El modul city crea un graf no dirigit fusionat el graf dels carrers de Barcelona amb el graf de les lines d'autobús existents.
Gràcies això podrem obtenir el camí més ràpid per anar d'un lloc a un altre a peu i/o en bus.
"""
from typing import TypeAlias, Tuple, List
import networkx as nx
import osmnx as ox
import pickle
import os
from haversine import haversine 
from dataclasses import dataclass
import matplotlib.pyplot as plt 
from staticmap import StaticMap, CircleMarker 
from math import ceil
from buses import * 

CityGraph : TypeAlias = nx.Graph
OsmnxGraph : TypeAlias = nx.MultiDiGraph
Coord : TypeAlias = Tuple[float, float]   # (latitude, longitude)

Cruilla: TypeAlias = Coord

# Les nodes tipus cruilla són int i nodes del bus (parades) són Stop.
Path: TypeAlias = List[int | Stop]

WALKING_SPEED = 1.3 #velocitat mitjana caminat és de 1.3 m/s (4.7 km/h)
BUS_SPEED = 3.3 # velocitat mitjana dels busos de Bcn és de 3.3 m/s (12 km/h)

class Edge:
    type: str
    _distance: float
    _time: float

    def __init__(self, type: str, dist: float) -> None:
        """Constructor de la classe aresta"""
        self.type = type
        self._distance = dist
        # Classifiquem les arestes en tipus bus i tipus peu
        if type == "busline":
            self._time = self._distance / BUS_SPEED # Calula el temps que tarda anat amb bus
        else:
            self._time = self._distance / WALKING_SPEED # Calcula el temps que tarda anat a peu

    def time(self) -> float:
        """Retorna el temps de les arestes"""
        return self._time 


def get_osmnx_graph() -> OsmnxGraph: 
    """
    Obté el graf dels carrers de Barcelona "g" i eliminar la informació de la geometria dels camins
    """
    # Obté el graf de Barcelona
    g: OsmnxGraph = ox.graph_from_place("Barcelona, Spain", network_type='walk', simplify=True) # type: ignore

    # Eliminem la informació de geometria perquè no ens cal
    for u, v, key, geom in g.edges(data="geometry", keys=True): # type: ignore
        if geom is not None:
            del(g[u][v][key]["geometry"])

    return g


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None: 
    """Guarda el graf dels carrers de Barcelona "g" al fitxer "filename" """
    pickle_out = open(filename, "wb")
    pickle.dump(g, pickle_out)
    pickle_out.close()


def load_osmnx_graph(filename: str) -> OsmnxGraph: 
    """
    Retorna el graf "g" previament creat i guardat al fitxer "filename", 
    si no s'havia creat, el crea i el guarda al fitxer "filename"
    """
    # Si el fitxer ja existeix, podem accedir a la informació des del filename  
    if os.path.exists(filename):
        graph = pickle.load(open(filename, "rb"))
    # Sinó, obtenim el graf i el guardem al fitxer
    else:
        graph = get_osmnx_graph()
        save_osmnx_graph(graph, filename)
    return graph


def _street_nodes(g: CityGraph, g1: OsmnxGraph) -> None:
    """Afegiex els nodes tipus cruilla del OsmnxGraph "g1" al CityGraph "g" """
    # Obtenim les coordenades x, y del OsmnxGraph (graf Bcn)
    x = nx.get_node_attributes(g1, "x")
    y = nx.get_node_attributes(g1, "y")

    # iterem sobre els nodes de "g1" i afegim les coord dels nodes a "g"
    for node in g1.nodes:
        position: Coord = x[node], y[node]
        g.add_node(node, pos=position, type="cruilla")


def _street_edges(g: CityGraph, g1: OsmnxGraph) -> None:
    """Afegeix les arestes tipus street des del OsmnxGraph "g1" al CityGraph "g" """ 
    # Recorrem totes les arestes del graf "g1"
    # Per cada node i els seus adjecents obtenim la info...
    for u, nbrsdict in g1.adjacency():
        # per cada node adjacent v i les (u,v) arestes obtenim la info...
        for v, edgesdict in nbrsdict.items():
            # Els grafs osmnx són multigrafs, però només considerem la primera aresta 
            dist = edgesdict[0]["length"]    # edgesdict conté la info de la primera aresta 
            edge_info = Edge("street", dist)
            g.add_edge(u, v, info=edge_info, w=edge_info.time())


def _bus_nodes(g: CityGraph, g1: OsmnxGraph, g2: BusesGraph) -> None:
    """
    Afegeix els parades de bus(nodes) procedent del BusesGraph "g2",al CityGraph "g" 
    i connecta afegeix les arestes que connecten les parades de bus de "g2" amb les cruilles de "g1"
    """
    x_coords: List[float] = list()
    y_coords: List[float] = list()

    # Itera sobre les parades i afegim les seves corrdenades al graf g
    for stop in g2.nodes (data=True):
        x, y = stop[1]['pos']
        x_coords.append(x)
        y_coords.append(y)
        g.add_node(stop[0], pos=(x,y), type="parada")

    # Troba al cruilla més propera a cada parada
    nearest, dist = ox.distance.nearest_nodes(g1, x_coords, y_coords, return_dist=True) # type: ignore
    
    # S'afegeixen les arestes entre nodes
    for i, stop in enumerate(list(g2.nodes)):
        union_edge = Edge("union", dist[i])
        g.add_edge(stop, nearest[i], info=union_edge, w=union_edge.time())


def _bus_edges(g: CityGraph, g2: BusesGraph) -> None:
    """Afegeix les arestes dels busos (recorregut de parada a parada) del BusGraph "g2" al CityGraph "g" """ 
    for edge in g2.edges:
        bus = Bus(edge[0], edge[1])
        edge_info = Edge("busline", bus.weight())  # Afegim els pesos de les arestes
        g.add_edge(edge[0], edge[1], info=edge_info, w=edge_info.time())  


def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
    """
    Retorna un CityGraph "g" permetrà buscar camins tan a peu com en bus, 
    ja que fusiona el OsmnxGraph "g1" amb el BusesGraph "g2"
    """
    g: CityGraph = nx.Graph()

    # Afegim el nodes dels carrers, tipus cruilla 
    _street_nodes(g, g1)
    # Afegim les arestes que formen els carrers, tipus street
    _street_edges(g, g1)
    # Afexim els nodes de les parades de busos i les arestes que connecten ambdós grafs.
    _bus_nodes(g, g1, g2)
    # Afegim les arestes dels busos, tipus busline
    _bus_edges(g, g2)
    # Borra arestes que connecten un node amb ell mateix 
    g.remove_edges_from(nx.selfloop_edges(g))

    return g


def _calculate_path_time(p: Path, g: CityGraph, extra_dist: float) -> int:
    """Retorna el temps mínim del recorregut en minuts"""
    extra_time = extra_dist / WALKING_SPEED
    path_time = sum([g.edges[p[i], p[i+1]]["w"] for i in range(len(p) -1)])
    return ceil((extra_time + path_time) / 60)


def find_path_and_time(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Tuple[Path, int]:
    """
    Troba el camí més curt en temps per arribar a un cinema de la manera més ràpida, des de
    la ubicació acutal 'src' fins el cinema 'dst' 
    ---
    'g': <CityGraph amb tots els nodes i arestes tant dels busos com dels carrers
    'ox_g': OsmnxGraph que conté tots els nodes i arestes
    'src': coords de la ubicació inicial
    'dst': coords de la destinació 
    """

    x_src, y_src = src
    x_dst, y_dst = dst
    # Torba el node més proper a la ubicació acutual 'src' i de la destinació 'dst' 
    nearest_nodes, dist = ox.distance.nearest_nodes(
        ox_g, [x_src, x_dst], [y_src, y_dst], return_dist=True)

    # Troba el camí més curt des del node inicial (nearest_nodes[0]) cap al final (nearest_nodes[1])
    path = nx.dijkstra_path(g, source=nearest_nodes[0],
                            target=nearest_nodes[1],
                            weight="w")
    time = _calculate_path_time(path, g, sum(dist))
    return path, time


def show(g: CityGraph) -> None: 
    """Mostra el CityGraph "g" de forma interactiva en una finestra""" 
    pos = nx.get_node_attributes(g, "pos")
    nx.draw(g, pos=pos, node_size= 5) # pos diu on s'ha de situar cada node 
    plt.show()


def _plot_nodes(g: CityGraph, m: StaticMap) -> None:
    """Imprimeix els nodes del graf 'g' """
    for node in g.nodes:  #posar un if pq el color sigui diferent en funció del tipus
        marker = CircleMarker(g.nodes[node]['pos'], "#111112", 2)
        m.add_marker(marker)


def _plot_edges(g: CityGraph, m: StaticMap) -> None:
    """Imprmeix les arestes del graf 'g' """
    # si les arestes són de tipus bus, color vermell, si és un camí a pau color blau
    for edge in g.edges(data = True):      
        coord1 = g.nodes[edge[0]]["pos"]
        coord2 = g.nodes[edge[1]]["pos"]
        if edge[2]["info"].type == "busline":
            color = "#192DC6"
        else:
            color = "#C6191E"
        line = Line((coord1, coord2), color, 2)
        m.add_line(line)


def plot(g: CityGraph, filename: str) -> None: 
    """"
    Guarda el CityGraph "g" al filename. Aquest conté el mapa de Barcelona de fons.
    En primer pla es mostren les lines de busos i els carrers de Barcelona.
    """
    m = StaticMap(2000, 2000, 80)
    # Funció per printejar Nodes
    _plot_nodes(g, m)
    #Funció per printejar arestes
    _plot_edges(g, m)
    image = m.render()
    image.save(filename)


def _obtenir_coords_node(g: CityGraph, node: int | Stop) -> Tuple[Coord, str]:
    """Obté les coordenades dels nodes i si hi ha un transbordament canvia de color de l'aresta"""
    if type(node) == int:
        coords = g.nodes[node]["pos"]
        color = "#192DC6"
    else:
        coords = node.pos
        color =  "#C6191E"
    return coords, color
    

def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    """Mostra el camí més ràpid 'p' i el guarda al fitxer 'filename' """

    # Generem el mapa de Bcn perquè és vegui de fons
    m = StaticMap(2000, 2000, 80)  
    coords1, color1 = _obtenir_coords_node(g, p[0])
    start_marker = CircleMarker(coords1, "#111112", 9)
    m.add_marker(start_marker)
    coords2 = 0.0 #inicialitzem variable per evitar error de tipus

    # iterem iniciant al 2n node al últim per poder comprovar el i, i-1
    for i in range(1, len(p)):
        coords2, color2 = _obtenir_coords_node(g, p[i])
        line = Line((coords1, coords2), color1, 7)
        m.add_line(line)     
        # Marquem els canvis de transport amb un punt negre  
        if color1 != color2:
            change_marker = CircleMarker(coords2, "#111112", 9)
            m.add_marker(change_marker)
        elif type(p[i]) == Stop and p[i].IdLinia != p[i-1].IdLinia:
            change_marker = CircleMarker(coords2, "#111112", 9)
            m.add_marker(change_marker)  
        coords1 = coords2
        color1 = color2

    #marcar la destinació amb un punt engre
    end_marker = CircleMarker(coords2, "#111112", 9)    
    m.add_marker(end_marker)            
    image = m.render()
    image.save(filename)

