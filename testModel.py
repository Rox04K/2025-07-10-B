from model.model import Model

model = Model()

model.creaGrafo(7, '2017-03-11', '2018-05-25')
print('Grafo correttamente creato')

nodi, archi = model.getInfo() #Questa formattazione può variare in base all'esempio
print(f'Numero di nodi: {nodi}')
print(f'Numero di archi: {archi}')


print()
best = model.getBestNodi()
print(f'Top 5 nodi:')
for b in best:
    print(f'{b[0]} con valore {b[1]}')

