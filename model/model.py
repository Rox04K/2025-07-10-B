import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._IDMap = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getCategories()

    def creaGrafo(self, categoria, start, end):
        #Come prima cosa bisogna pulire il grafo per poterlo ricreare senza dati vecchi
        self._grafo.clear()
        self._IDMap = {}

        nodi = DAO.getNodi(categoria)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._IDMap[n.product_id] = n

        archi = DAO.getArchi(categoria, start, end, self._IDMap)
        pesi = DAO.getPesi(categoria, start, end)

        for a in archi:
            u = a[0]
            valoriU = pesi[u.product_id]
            v = a[1]
            valoriV = pesi[v.product_id]
            peso = valoriU[1] + valoriV[1]

            if valoriU[0] < valoriV[0]:
                self._grafo.add_edge(u, v, weight=peso)
            elif valoriU[0] > valoriV[0]:
                self._grafo.add_edge(v, u, weight=peso)
            else:
                self._grafo.add_edge(u, v, weight=peso)
                self._grafo.add_edge(v, u, weight=peso)

    def getInfo(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getBestNodi(self):
        result = []
        for n in self._grafo.nodes():
            archiEntranti = list(self._grafo.in_edges(n, data=True))
            archiUscenti = list(self._grafo.out_edges(n, data=True))

            somma = 0
            for e,f,d in archiEntranti:
                somma += d['weight']

            for u, v, w in archiUscenti:
                somma -= w['weight']

            result.append((n, somma))

        result.sort(key=lambda x: x[1], reverse=True)
        return result[:5]
    
    

