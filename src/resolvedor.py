class ResolvedorSistema:
    # Essa classe será nossa "máquina de resolver sistemas".
    # Ela guarda dois valores: o resultado do sistema e o tipo de sistema.
    def __init__(self): # O construtor da classe, que serve para inicializar os contêineres em que os valores serão guardados.
        self.resultado = None # É atribuído um valor nulo para que o contêiner de resultado seja criado.
        self.tipo_sistema = None # É atribuído um valor nulo para que o contêiner de tipo de sistema seja criado.

    def resolver_2x2(self, coeficientes, termos_independentes):
        # O método resolver_2x2 é o principal responsável por receber os coeficientes e termos independentes,
        # e retornar o tipo de sistema e o resultado.
        try: # O bloco try é responsável por executar o código e capturar possíveis erros.
            # Caso o sistema não seja 2x2, o erro é capturado e uma mensagem de erro é exibida.
            if len(coeficientes) != 2 or len(coeficientes[0]) != 2 or len(termos_independentes) != 2:
                raise ValueError("O sistema deve ser 2x2")
            # O determinante é calculado usando a fórmula a11*a22 - a12*a21.
            det = coeficientes[0][0] * coeficientes[1][1] - coeficientes[0][1] * coeficientes[1][0]

            # Caso o determinante seja diferente de zero, o sistema é determinado.
            if abs(det) > 1e-10: # O valor 1e-10 ( 0.0000000001 ) é usado ao invés de zero para evitar erros.
                                 # Caso ocorra um erro de arredondamento e o computador obtenha um valor muito próximo de zero,
                                 # o código ainda assim deverá funcionar perfeitamente.
                # Utilizando a regra de Cramer para calcular os valores de x e y
                x = (termos_independentes[0] * coeficientes[1][1] - termos_independentes[1] * coeficientes[0][1]) / det
                y = (termos_independentes[1] * coeficientes[0][0] - termos_independentes[0] * coeficientes[1][0]) / det
                self.tipo_sistema = "determinado"
                self.resultado = [x, y]
                # Saída do tipo de sistema (determinado) e o resultado (x, y)
                return self.tipo_sistema, self.resultado
            
            # Quando o determinante é zero, o sistema deve ser classificado como indeterminado ou impossível.
            # Para isso, precisamos verificar se as equações são proporcionais (múltiplas uma da outra) ou não.
            # Por exemplo:
            # 2x + 3y = 4   Estas equações são proporcionais, e neste caso,
            # 4x + 6y = 8   a segunda equação é igual a 2 vezes a primeira.
            #
            # 2x + 3y = 4   Neste caso, as equações não são proporcionais.
            # 4x + 6y = 9
            # Vamos verificar se alguma das equações é uma linha de zeros (Por exemplo: 0x + 0y = 0).
            # Se for, não há proporção entre as equações, pois não tem como dividir por zero.
            if abs(coeficientes[0][0]) < 1e-10 and abs(coeficientes[0][1]) < 1e-10:
                proporcao_coef = None
            elif abs(coeficientes[1][0]) < 1e-10 and abs(coeficientes[1][1]) < 1e-10:
                proporcao_coef = None
            # Se não houver linha de zeros, tentaremos calcular a proporção entre as equações.
            # Se o coeficiente a11 for diferente de zero (Não dá pra dividir por zero), usaremos ele para calcular a proporção.
            elif abs(coeficientes[0][0]) > 1e-10: 
                proporcao_coef = coeficientes[1][0] / coeficientes[0][0]
            # Se o coeficiente a12 for diferente de zero (Não dá pra dividir por zero), usaremos ele para calcular a proporção.
            elif abs(coeficientes[0][1]) > 1e-10:
                proporcao_coef = coeficientes[1][1] / coeficientes[0][1]
            # Se não der com o a11 e nem com o a12, não há proporção entre as equações.
            else:
                proporcao_coef = None
                
            # Agora, vamos determinar se o sistema é indeterminado ou impossível.
            # Primeiro, trabalharemos com os casos em que há proporção entre as equações.
            # Se os termos independentes manterem a mesma proporção, o sistema é indeterminado.
            # Caso contrário, o sistema é impossível.
            if proporcao_coef is not None:
                # É utilizada uma equação para verificar a proporção entre os termos independentes.
                # É calculada a diferença entre o termo independente da segunda equação
                # e o termo independente da primeira equação multiplicado pela proporção das equações.
                # Caso o valor absoluto (sem sinal negativo) dessa diferença seja zero (ou menor que 0.0000000001),
                # o sistema é indeterminado.
                if abs(termos_independentes[1] - proporcao_coef * termos_independentes[0]) < 1e-10:
                    self.tipo_sistema = "indeterminado"
                    self.resultado = None
                else:
                    # Caso contrário (se a diferença for maior que 0.0000000001), não há proporção entre
                    # os termos independentes e portanto, o sistema é impossível.
                    self.tipo_sistema = "impossivel"
                    self.resultado = None
            # Agora, vamos trabalhar com os casos em que não há proporção entre as equações.
            else:
                # Se o termo independente da segunda equação for zero (ou menor que 0.0000000001),
                # o sistema é indeterminado. Vale lembrar que a esse ponto, uma das equações já é uma linha de zeros.
                if abs(termos_independentes[1]) < 1e-10:
                    self.tipo_sistema = "indeterminado"
                    self.resultado = None
                else:
                    # Se o termo independente da segunda equação não for zero, o sistema é impossível.
                    # Por exemplo: 0x + 0y = 1 (Não há como resolver isso).
                    self.tipo_sistema = "impossivel"
                    self.resultado = None
                    # Notemos que em ambos os casos (indeterminado e impossível),
                    # o campo de resultado sempre será None (ou nulo). Isso é porque
                    # sistemas impossíveis não possuem solução, e sistemas indeterminados
                    # possuem infinitas soluções (e seria impossível listar todas).
            # Por fim, o método retorna o tipo de sistema e o resultado.
            return self.tipo_sistema, self.resultado
        # Caso ocorra um erro, uma mensagem de erro é exibida.
        except Exception as e: # O erro é capturado dentro da variável (contêiner) "e".
            raise Exception(f"Erro ao resolver o sistema: {str(e)}")  # Então, o erro é exibido ao usuário.