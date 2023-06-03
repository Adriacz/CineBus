import networkx as nx
import json
import requests
from staticmap import StaticMap, CircleMarker, Line
from typing import TypeAlias, Tuple
from dataclasses import dataclass
from haversine import haversine, Unit
import matplotlib.pyplot as plt
import matplotlib


BusesGraph: TypeAlias  = nx.Graph



@dataclass (frozen = True)
class Stop:
    id : int
    nom: str
    municipi: str
    IdLinia: int
    pos: Tuple[float, float]

'''Implementació de les arestes'''
class Bus:
    stop1: Stop
    stop2: Stop
    
    
    def __init__(self, stop1: Stop, stop2: Stop) -> None:
        self.stop1 = stop1
        self.stop2 = stop2

    def weight(self) -> float:
        dist = haversine(self.stop1.pos, self.stop2.pos, Unit.METERS)
        return dist

'''Implementació de les línies de bus'''
class BusLine:
    id : int
    stops : list[Stop]

    def __init__(self, id: int, stops: list[Stop]) -> None:
        self.id = id
        self.stops = stops
    
    def add_to_graph(self, g: BusesGraph) -> None:
        for stop in self.stops:
            if stop.municipi == "Barcelona":
                g.add_node(stop, pos=stop.pos)
        
        for i in range(len(self.stops) -1):
            if self.stops[i].municipi == "Barcelona" and self.stops[i+1].municipi == "Barcelona":
                bus = Bus(self.stops[i], self.stops[i+1])
                g.add_edge(bus.stop1, bus.stop2, w=bus.weight())


def get_buses_graph() -> BusesGraph:
        
    g: BusesGraph = nx.Graph()

    url = "https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json"    
    response = requests.get(url).json()    
    info = response["ObtenirDadesAMBResult"]["Linies"]["Linia"] #Seleccionem els camps que ens iteressen

    for linia in info:
        
        stops_data = linia["Parades"]["Parada"]
        lineId = int(linia["Id"])
        stops: list[Stop] = list()
        for stop in stops_data:
            id = stop["CodAMB"]
            name = stop["Nom"]
            x = stop["UTM_Y"]
            y = stop["UTM_X"]
            municipi = stop["Municipi"]
            stops.append(Stop(id, name, municipi, lineId, (x, y)))     
            
        line = BusLine(lineId, stops)
        line.add_to_graph(g)
    g.remove_edges_from(nx.selfloop_edges(g))

    return g


def show(g: BusesGraph) -> None:
    pos = nx.get_node_attributes(g, "pos")
    nx.draw(g, pos=pos, node_size= 5) # pos diu on s'ha de posar cada node, with_labels = False 
    plt.show()

def _plot_nodes(g: BusesGraph, m: StaticMap) -> None:
    for node in g.nodes():
        marker = CircleMarker(g.nodes[node]['pos'], "black", 3)
        m.add_marker(marker)

def _plot_edges(g: BusesGraph, m: StaticMap) -> None:
    for edge in g.edges():
        coords1 = [g.nodes[edge[0]]['pos'][0], g.nodes[edge[0]]['pos'][1]]
        coords2 = [g.nodes[edge[1]]['pos'][0], g.nodes[edge[1]]['pos'][1]]
        line = [coords1, coords2]
        edge_to_draw = Line(line, "#0000FF", 1)
        m.add_line(edge_to_draw)



def plot(g: BusesGraph, nom_fitxer: str) -> None: 
    m = StaticMap(2000, 2000, 80)
    _plot_nodes(g,m) 
    _plot_edges(g, m)
    image = m.render()
    image.save(nom_fitxer)



def main()->None:
    g = get_buses_graph()
    show(g)
    plot(g, "BusGraphProva.png")

if __name__ == "__main__":
    main()