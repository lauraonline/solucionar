import numpy as np # vou começar importando a biblioteca numpy, que é uma biblioteca de álgebra linear para python.

# essa classe será a "máquina de resolver sistemas".
# ela guarda dois valores: o resultado do sistema e o tipo de sistema.
class ResolvedorSistema:
    def __init__(self): # o construtor principal da classe, que serve para inicializar os contêineres em que os valores serão guardados.
        self.resultado = None # é atribuído um valor nulo para que o contêiner de resultado seja criado.
        self.tiposistema = None # é atribuído um valor nulo para que o contêiner de tipo de sistema seja criado.
        # o método resolver é o principal responsável por receber os coeficientes e termos independentes e retornar o tipo de sistema e o resultado.
        # os coeficientes vem em forma matricial e os termos independentes em forma de vetor.
    def resolver(self, coeficientes, termosindependentes):
        try: # o try serve pra que se der erro, o computador armazene a mensagem de erro em uma variável pra mostrar pro usuário.

            # é hora de converter os coeficientes para um array numpy.
            # arrays são uma estrutura de dados em que todos os elementos do mesmo tipo são armazenados em sequência, dentro de uma única variável.

            # eu vou usar arrays por eles serem uma maneira do computador entender melhor os dados.
            # assim, ele vê os dados como uma matriz e obtemos a capacidade de fazer operações com eles.
            A = np.array(coeficientes, dtype=float)
            # também vou converter os termos independentes para um array numpy.
            # ao contrário dos coeficientes, os termos independentes serão recebidos em forma de vetor (uma linha).
            b = np.array(termosindependentes, dtype=float)

            # a esse ponto, o computador vê os dados como uma matriz e um vetor. por exemplo, o sistema
            # 1x + 2y + 3z = 10
            # 4x + 5y + 6z = 11
            # 7x + 8y + 9z = 12
            # seria representado como:
            # A = [[1, 2, 3],
            #      [4, 5, 6],
            #      [7, 8, 9]]
            # b = [10, 11, 12]

            # agora, é preciso verificar o tipo de sistema.
            # se o número de linhas da matriz A (A.shape[0]) é igual ao número de colunas (A.shape[1]), o sistema é quadrado e se pode partir para a resolução.
            if A.shape[0] == A.shape[1]: 
                # vou usar o método det do np.linalg, o módulo de álgebra linear do numpy, para calcular o determinante da matriz que contém os coeficientes e armazená-lo em det.
                det = np.linalg.det(A)
                # como o computador usa base 2 para representar os números, ele pode ter propensão a confundir o 0 com um número muito pequeno.
                # por isso, vou usar a função round para arredondar a saída de det para 5 casas decimais.
                # depois, comparo o resultado com 0. 
                if round(det, 5) != 0: # se o determinante não for 0, o sistema é possível e determinado. 
                    # vou usar o método solve do np.linalg, o módulo de álgebra linear do numpy, para resolver o sistema.
                    self.resultado = np.linalg.solve(A, b)
                    self.tiposistema = "sistema possível e determinado"
                else:
                    # se o determinante for 0, o sistema pode ser possível e indeterminado ou impossível.
                    # para descobrir qual é o caso, vou usar o método matrix_rank do np.linalg.
                    # com ele, vou calcular o posto da matriz A. caso o posto seja menor que o número de linhas, as equações são linhas coincidentes no plano cartesiano. no entanto, isso se aplica somente se os termos independentes forem proporcionais às equações.
                    # logo, vou checar a proporção entre esses dois.
                    rankA = np.linalg.matrix_rank(A)
                    # calculando o posto da matriz aumentada A|b, eu posso checar se os termos independentes obedecem às equações. caso isso não ocorra, as equações se tornam linhas paralelas no plano cartesiano, o que caracteriza um sistema impossível.
                    rankAb = np.linalg.matrix_rank(np.c_[A, b])
                    # botando tudo isso em prática, vou checar se o posto de A é igual ao posto de A|b.
                    # caso seja, as duas equações são coincidentes e o sistema é possível e indeterminado.
                    if rankA == rankAb:
                        self.tiposistema = "sistema possível e indeterminado"
                    # caso não seja, as duas equações são paralelas e o sistema é impossível.
                    else:
                        self.tiposistema = "sistema impossível"
            else:

                # logicamente, se o número de linhas não é igual ao número de colunas,
                # o sistema não é quadrado e foge do escopo do programa.
                raise ValueError("o sistema não é quadrado.")
            
            # por fim, o programa retorna o tipo de sistema e o resultado.
            return self.tiposistema, self.resultado
        
        # se ocorrer um erro, ele retorna a mensagem de erro adequada.  
        except Exception as e:
            raise Exception(f"x_x ocorreu um erro ao resolver o sistema: {str(e)}")