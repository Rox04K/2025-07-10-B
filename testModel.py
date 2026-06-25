from model.model import Model

model = Model()

model.creaGrafo(5, '2016-01-01', '2018-12-28')
print('Grafo correttamente creato')

nodi, archi = model.getInfo() #Questa formattazione può variare in base all'esempio
print(f'Numero di nodi: {nodi}')
print(f'Numero di archi: {archi}')


print()
best = model.getBestNodi()
print(f'Top 5 nodi:')
for b in best:
    print(f'{b[0]} con valore {b[1]}')

print()
cammino, punteggio = model.getCamminoOttimo()
print(f'Il cammino ottimo ha un punteggio di {punteggio} ed è composto da {len(cammino)} nodi')
for s in cammino:
    print(f'{s}')