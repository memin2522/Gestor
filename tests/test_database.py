import unittest
import csv
import copy
import config
import database as db
import helpers

class TestDatabse(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('15J', 'Memas', 'Turbo'),
            db.Cliente('33X', 'Memin', 'Pinguin'),
            db.Cliente('88Q', 'Melman', 'Reyes')
        ]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('15J')
        cliente_inexistente = db.Clientes.buscar('16J')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)
    
    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('39X', 'Mamas', 'Te')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(nuevo_cliente.dni, '39X')
        self.assertEqual(nuevo_cliente.nombre, 'Mamas')
        self.assertEqual(nuevo_cliente.apellido, 'Te')

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('88Q'))
        cliente_modificado = db.Clientes.modificar('88Q', 'Melman', 'Mamon')
        self.assertEqual(cliente_a_modificar.apellido, 'Reyes')
        self.assertEqual(cliente_modificado.apellido, 'Mamon')

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('33X')
        cliente_buscado = db.Clientes.buscar('33X')
        self.assertEqual(cliente_borrado.dni, '33X')
        self.assertIsNone(cliente_buscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('85285285', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('15J')
        db.Clientes.borrar('33X')
        db.Clientes.modificar('88Q', 'Mariana', 'Garcia')
        
        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline='\n') as fichero:
            reader = csv.reader(fichero, delimiter=';')
            dni, nombre, apellido = next(reader)
        
        self.assertEqual(dni, '88Q')
        self.assertEqual(nombre, 'Mariana')
        self.assertEqual(apellido, 'Garcia')
