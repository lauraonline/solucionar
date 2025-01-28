import unittest
from src.resolvedor import ResolvedorSistema

class TestResolvedor2x2(unittest.TestCase):
    def setUp(self):
        self.resolvedor = ResolvedorSistema()

    def test_sistema_determinado(self):
        # x + y = 3
        # 2x + 3y = 8
        coeficientes = [[1, 1], [2, 3]]
        termos_independentes = [3, 8]

        tipo, resultado = self.resolvedor.resolver_2x2(coeficientes, termos_independentes)

        self.assertEqual(tipo, "determinado")
        self.assertAlmostEqual(resultado[0], 1) # x = 1
        self.assertAlmostEqual(resultado[1], 2) # y = 2

    def test_sistema_impossivel(self):
        # x + y = 1
        # x + y = 2
        coeficientes = [[1, 1], [1, 1]]
        termos_independentes = [1, 2]

        tipo, resultado = self.resolvedor.resolver_2x2(coeficientes, termos_independentes)

        self.assertEqual(tipo, "impossivel")
        self.assertIsNone(resultado)
    
    def test_sistema_indeterminado(self):
        # x + y = 2
        # 2x + 2y = 4
        coeficientes = [[1, 1], [2, 2]]
        termos_independentes = [2, 4]

        tipo, resultado = self.resolvedor.resolver_2x2(coeficientes, termos_independentes)

        self.assertEqual(tipo, "indeterminado")
        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main()