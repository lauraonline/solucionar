import unittest
import numpy as np
from src.resolvedor import ResolvedorSistema

class TestResolvedorGeral(unittest.TestCase):
    def setUp(self):
        self.resolvedor = ResolvedorSistema()
    
    def test_sistema_3x3_determinado(self):
        # 2x + 3y + z = 1
        # 6x - 2y - z = -14
        # 3x + y - z = 1
        coeficientes = [
            [2, 3, 1],
            [6, -2, -1],
            [3, 1, -1]
        ]
        termos_independentes = [1, -14, 1]

        tipo, resultado = self.resolvedor.resolver(coeficientes, termos_independentes)

        self.assertEqual(tipo, "sistema possível e determinado")
        self.assertAlmostEqual(resultado[0], -2) # x = -2
        self.assertAlmostEqual(resultado[1], 3) # y = 3
        self.assertAlmostEqual(resultado[2], -4) # z = -4

    def test_sistema_3x3_indeterminado(self):
        # x + y + z = 6
        # 2x + 2y + 2z = 12
        # 3x + 3y + 3z = 18
        coeficientes = [
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3]
        ]
        termos_independentes = [6, 12, 18]

        tipo, resultado = self.resolvedor.resolver(coeficientes, termos_independentes)

        self.assertEqual(tipo, "sistema possível e indeterminado")
        self.assertIsNone(resultado)

    def test_sistema_3x3_impossivel(self):
        # 2x + 3y - z = 3
        # x - 2y + 3z = 4
        # 5x + 4y + z = 5
        coeficientes = [
            [2, 3, -1],
            [1, -2, 3],
            [5, 4, 1]
        ]
        termos_independentes = [3, 4, 5]

        tipo, resultado = self.resolvedor.resolver(coeficientes, termos_independentes)

        self.assertEqual(tipo, "sistema impossível")
        self.assertIsNone(resultado)

    def test_sistema_4x4_determinado(self):
        # x - 2y + 2z - 3w = 15
        # 3x + 4y - z + w = -6
        # 2x - 3y + 2z - w = 17
        # x + y - 3z - 2w = -7
        coeficientes = [
            [1, -2, 2, -3],
            [3, 4, -1, 1],
            [2, -3, 2, -1],
            [1, 1, -3, -2]
        ]
        termos_independentes = [15, -6, 17, -7]

        tipo, resultado = self.resolvedor.resolver(coeficientes, termos_independentes)

        self.assertEqual(tipo, "sistema possível e determinado")
        self.assertAlmostEqual(resultado[0], 2) # x = 2
        self.assertAlmostEqual(resultado[1], -2) # y = -2
        self.assertAlmostEqual(resultado[2], 3) # z = 3
        self.assertAlmostEqual(resultado[3], -1) # w = -1

    def test_sistema_4x4_indeterminado(self):
        # x + 2y - z + w = 3
        # 2x + 4y - 2z + 2w = 6
        # 3x + 6y - 3z + 3w = 9
        # x - y + 2z - 3w = 2
        coeficientes = [
            [1, 2, -1, 1],
            [2, 4, -2, 2],
            [3, 6, -3, 3],
            [1, -1, 2, -3]
        ]
        termos_independentes = [3, 6, 9, 2]

        tipo, resultado = self.resolvedor.resolver(coeficientes, termos_independentes)

        self.assertEqual(tipo, "sistema possível e indeterminado")
        self.assertIsNone(resultado)
    
    def test_sistema_4x4_impossivel(self):
        # x + y + z + w = 1
        # 2x + 2y + 2z + 2w = 2
        # 3x + 3y + 3z + 3w = 4
        # 4x + 4y + 4z + 4w = 5
        coeficientes = [
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3],
            [4, 4, 4, 4]
        ]
        termos_independentes = [1, 2, 4, 5]

        tipo, resultado = self.resolvedor.resolver(coeficientes, termos_independentes)

        self.assertEqual(tipo, "sistema impossível")
        self.assertIsNone(resultado)

    def test_sistema_subdeterminado(self):
        # x + y + z + w = 1
        # 2x + 2y + 2z + 2w = 2
        # 3x + 3y + 3z + 3w = 4
        coeficientes = [
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3]
        ]
        termos_independentes = [1, 2, 4]

        tipo, resultado = self.resolvedor.resolver(coeficientes, termos_independentes)

        self.assertIsNone(tipo)
        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main()
