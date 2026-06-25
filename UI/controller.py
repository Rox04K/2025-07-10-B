import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._sceltaCategoria = None
        self._sceltaUtenteSP = None
        self._sceltaUtenteEP = None

    def fillDDCategory(self):
        opzioni = self._model.getCategories()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(
            key=x.category_id,
            text=x.category_name,
            data=x,
            on_click=self._readCategory
        ), opzioni))
        self._view._ddcategory.options = opzioniDD

    def _readCategory(self, e):
        scelta = e.control.data

        if scelta is None:
            self._sceltaCategoria = None

        else:
            self._sceltaCategoria = scelta
            print(self._sceltaCategoria)

    def handleCreaGrafo(self, e):
        categoria = self._sceltaCategoria
        if categoria is None:
            self._view.create_alert('Attenzione! Selezionare una categoria!')
            return
        start = self._view._dp1.value
        if start == "":
            self._view.create_alert('Attenzione! Selezionare una data di inizio!')
            return
        end = self._view._dp2.value
        if end == "":
            self._view.create_alert('Attenzione! Selezionare una data di fine!')
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'Date selezionate:'))
        self._view.txt_result.controls.append(ft.Text(f'Start date: {start}'))
        self._view.txt_result.controls.append(ft.Text(f'End date: {end}'))

        self._model.creaGrafo(categoria.category_id, start, end)
        self._view.txt_result.controls.append(ft.Text(f'Grafo correttamente creato:', color='green'))

        nodi, archi = self._model.getInfo()
        self._view.txt_result.controls.append(ft.Text(f'Numero di nodi: {nodi}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero di archi: {archi}'))

        self._fillDDProdotti()

        self._view.update_page()

    def _fillDDProdotti(self):
        opzioni = self._model.getNodes()

        opzioniSD = list(map(lambda x: ft.dropdown.Option(
            key=x.product_id,
            text=x.product_name,
            data=x,
            on_click=self._readChoiceSP
        ), opzioni))
        self._view._ddProdStart.options = opzioniSD

        opzioniED = list(map(lambda x: ft.dropdown.Option(
            key=x.product_id,
            text=x.product_name,
            data=x,
            on_click=self._readChoiceEP
        ), opzioni))
        self._view._ddProdEnd.options = opzioniED

    def _readChoiceSP(self, e):
        scelta = e.control.data

        if scelta is None:
            self._sceltaUtenteSP = None

        else:
            self._sceltaUtenteSP = scelta
            print(self._sceltaUtenteSP)

    def _readChoiceEP(self, e):
        scelta = e.control.data

        if scelta is None:
            self._sceltaUtenteEP = None

        else:
            self._sceltaUtenteEP = scelta
            print(self._sceltaUtenteEP)

    def handleBestProdotti(self, e):
        best = self._model.getBestNodi()
        self._view.txt_result.controls.append(ft.Text(f'I cinque prodotti più venduti sono:'))
        for b in best:
            self._view.txt_result.controls.append(ft.Text(f'{b[0]} with score {b[1]}'))

        self._view.update_page()

    def handleCercaCammino(self, e):
        start = self._sceltaUtenteSP
        if start is None:
            self._view.create_alert('Attenzione! Selezionare un prodotto da cui partire!')
            return
        end = self._sceltaUtenteEP
        if end is None:
            self._view.create_alert('Attenzione! Selezionare un prodotto a cui arrivare!')
            return
        if start.product_id == end.product_id:
            self._view.create_alert('Attenzione! I prodotti devono essere diversi!')
            return

        lun = self._view._txtInLun.value
        if lun == "":
            self._view.create_alert('Attenzione! Inserire la lunghezza del cammino')
            return
        try:
            lunInt = int(lun)
        except ValueError:
            self._view.create_alert('Attenzione! La lunghezza deve essere un numero intero positivo')
            return

        self._view.txt_result.controls.clear()
        cammino, punteggio = self._model.getCamminoOttimo(start.product_id, end.product_id, lunInt)
        self._view.txt_result.controls.append(ft.Text(f'Il cammino ottimo ha peso {punteggio}', color='green'))
        for b in cammino:
            self._view.txt_result.controls.append(ft.Text(f'{b}'))

        self._view.update_page()



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
