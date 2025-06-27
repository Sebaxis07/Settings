from django.test import TestCase
from django.urls import reverse
from unittest.mock import Mock


class TestPaginaActual(TestCase):
    def test_pagina_actual_en_sesion(self):
        request = Mock()
        request.method = "GET"
        request.GET = {"pagina_actual": "2"}
        request.session = {}

        id = 1

        if "pagina_actual" in request.GET:
            request.session[f"pagina_actual_{id}"] = request.GET["pagina_actual"]

        #self.assertEqual(request.session[f"pagina_actual_{id}"], "3")  
        
class AgregarEliminarNotaTests(TestCase):
    def setUp(self):
        self.notas_key = "notas_libro_1"
        self.url = reverse('libro_detalle', args=[1])
        self.client.session[self.notas_key] = []
        self.client.session.save()

    def test_agregar_y_eliminar_nota(self):
       
        self.client.post(self.url, {'comentario': 'Nota temporal', 'color': 'red'})
        self.assertEqual(len(self.client.session[self.notas_key]), 5)

       
        response = self.client.post(self.url, {'eliminar_nota': 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.client.session[self.notas_key]), 1)
        
class EliminarNotaTests(TestCase):
    def setUp(self):
        self.notas_key = "notas_libro_1"
        self.url = reverse('libro_detalle', args=[1])
        self.client.session[self.notas_key] = [{'comentario': 'Nota de prueba'}]
        self.client.session.save()

    def test_eliminar_nota_invalida(self):
        
        response = self.client.post(self.url, {'eliminar_nota': 5})
        
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(len(self.client.session[self.notas_key]), 1)  

