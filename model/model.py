import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._IDMap = {}

        self._bestCammino = []
        self._bestPunteggio = 0

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getCategories()

    def creaGrafo(self, categoria, start, end):
        self._grafo.clear()
        self._IDMap = {}

        nodi = DAO.getNodi(categoria)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._IDMap[n.product_id] = n

        #NON FUNZIONANTE
        archi = DAO.getArchi(categoria, start, end, self._IDMap)
        pesi = DAO.getPesi(categoria, start, end)

        for a in archi:
            u = a[0]
            valoriU = pesi[u.product_id]
            v = a[1]
            valoriV = pesi[v.product_id]
            peso = valoriU[1] + valoriV[1]

            if valoriU[1] < valoriV[1]:
                self._grafo.add_edge(u, v, weight=peso)
            elif valoriU[1] > valoriV[1]:
                self._grafo.add_edge(v, u, weight=peso)
            else:
                self._grafo.add_edge(u, v, weight=peso)
                self._grafo.add_edge(v, u, weight=peso)

        '''archiPesati = DAO.getArchiPesati(categoria, start, end)
        for uscente_id, entrante_id, peso in archiPesati:
            u = self._IDMap[uscente_id]
            v = self._IDMap[entrante_id]
            self._grafo.add_edge(u, v, weight=peso)'''

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

    def getNodes(self):
        return list(self._grafo.nodes())

    def getCamminoOttimo(self, start, end, lun):
        self._bestCammino = []
        self._bestPunteggio = 0

        # SE HO UN NODO DI PARTENZA
        parziale = [self._IDMap[start]]
        self._ricorsione(parziale, end, lun)

        return self._bestCammino, self._bestPunteggio

    def _ricorsione(self, parziale, end, limite):

        if parziale[-1].product_id == end:
            if len(parziale) == limite:
                pesoAttuale = self._peso(parziale)
                if pesoAttuale > self._bestPunteggio:
                    self._bestCammino = copy.deepcopy(parziale)
                    self._bestPunteggio = pesoAttuale
                return
            else:
                return

        validi = self._grafo.successors(parziale[-1])

        for n in validi:
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, end, limite)
                parziale.pop()

    def _peso(self, parziale):
        peso = 0

        for p in range(len(parziale)-1):
            u = parziale[p]
            v = parziale[p+1]
            peso += self._grafo[u][v]['weight']

        return peso
    

