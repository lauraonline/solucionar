import tkinter as tk # vou começar importando o módulo tkinter, que é uma biblioteca gráfica que vem com o python.
from tkinter import ttk, messagebox # do tkinter, vou importar ttk, que são os nossos botões, rótulos, etc. e o messagebox, que é a caixa que exibirá mensagens de erro.
import numpy as np # vou importar o numpy, que é uma biblioteca de álgebra linear para python.
from resolvedor import ResolvedorSistema # tambem vou importar a nossa classe existente ResolvedorSistema, que é a "máquina de resolver sistemas".

# essa classe criará a interface gráfica do programa pro usuário poder inserir os dados e obter o resultado.
class InterfaceSistema:
    def _criar_interface(self): # definindo o método em que vão ficar os elementos da interface (ex. título, seletor de tamanho, botão, etc.). eu vou usar esse método depois no __init__
        # usando um label pra exibir o nome do programa
        ttk.Label(self.frame_principal, text="solucionar()", # nome do programa dentro do frame_principal
                 font=('Courier New', 16)).grid(row=0, column=0, columnspan=6, pady=10) # declarando a fonte e tamanho, a posição e o espaçamento dentro do frame_principal
        
        # usando outro label pra construir o seletor de tamanho do sistema (número de equações)
        ttk.Label(self.frame_principal, text="Número de equações:").grid(row=1, column=0) # criando a label e o texto
        self.combo_tamanho = ttk.Combobox(self.frame_principal, values=[2, 3, 4], width=2) # usando um combobox (vem com o tkinter) pra criar o seletor. parâmetros: valores de 2 a 4 e a largura da caixa de seleção.
        self.combo_tamanho.set(2) # declarando o valor padrão da caixa de seleção, que é 2 (o sistema mais simples possivel).
        self.combo_tamanho.grid(row=1, column=1) # declarando a posição da caixa de seleção em relação a janela (na mesma linha do rótulo, mas uma coluna à frente).
        self.combo_tamanho.bind('<<ComboboxSelected>>', self._mudar_tamanho) # pegando o valor da caixa de seleção e executando o método _mudar_tamanho, que usará-o como entrada.
        
        # criando o quadro que vai conter a entrada do sistema de equações
        self.frame_sistema = ttk.LabelFrame(self.frame_principal, text="Sistema de Equações", padding="10")
        self.frame_sistema.grid(row=2, column=0, columnspan=6, pady=10) # declarando a posição do quadro em relação a janela.
        # eu podia ter criado outra label só pro quadro em que vai ficar o sistema
        
        # criando o botão de resolver o sistema dentro do frame_principal acima e fazendo ele executar o método _resolver
        ttk.Button(self.frame_principal, text="Resolver", command=self._resolver).grid(row=4, column=0, columnspan=6, pady=10)
        
        # Área de resultado
        self.resultado_text = tk.Text(self.frame_principal, height=5, width=40)
        self.resultado_text.grid(row=5, column=0, columnspan=6, pady=10)

    def __init__(self): # o construtor principal da classe vai puxar bem mais peso, porque aqui eu vou precisar de muito mais elementos do que no resolvedor.
        # crio a janela principal com o construtor tk.Tk() e assinalo o título da janela e o tamanho.
        self.janela = tk.Tk()
        self.janela.title("solucionar()")
        self.janela.geometry("400x500")
        
        # inicializo o resolvedor que importei do arquivo resolvedor.py.
        self.resolvedor = ResolvedorSistema()
        
        #
        self.frame_principal = ttk.Frame(self.janela, padding="10")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Criando os elementos da interface
        self._criar_interface()
        
        # Tamanho atual do sistema
        self.tamanho_atual = 2
        
        # Criando a matriz de entrada inicial
        self._atualizar_matriz(2)

    def _atualizar_matriz(self, tamanho):
        # Limpar frame do sistema
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
            
        # Criar sistema de equações
        self.entradas_matriz = []
        self.entradas_termos = []
        variaveis = ['x', 'y', 'z', 'w']
        
        # Para cada linha (equação)
        for i in range(tamanho):
            linha_coef = []
            # Frame para uma equação completa
            frame_equacao = ttk.Frame(self.frame_sistema)
            frame_equacao.grid(row=i, column=0, pady=5)
            
            # Para cada coeficiente na equação
            for j in range(tamanho):
                # Entrada do coeficiente
                entrada = ttk.Entry(frame_equacao, width=5)
                entrada.grid(row=0, column=j*3)
                linha_coef.append(entrada)
                
                # Variável (x, y, z, w)
                ttk.Label(frame_equacao, text=variaveis[j]).grid(row=0, column=j*3 + 1)
                
                # Sinal de + (exceto para o último termo)
                if j < tamanho - 1:
                    ttk.Label(frame_equacao, text="+").grid(row=0, column=j*3 + 2, padx=5)
            
            # Sinal de igual
            ttk.Label(frame_equacao, text="=").grid(row=0, column=tamanho*3, padx=5)
            
            # Termo independente
            entrada_termo = ttk.Entry(frame_equacao, width=5)
            entrada_termo.grid(row=0, column=tamanho*3 + 1)
            
            self.entradas_matriz.append(linha_coef)
            self.entradas_termos.append(entrada_termo)

    # esse método vai pegar o valor da caixa de seleção (self.combo_tamanho), tratar ele e usar como entrada pro outro método _atualizar_matriz
    # ele é um pouco redundante mas é melhor de entender do que ter um supermétodo 
    def _mudar_tamanho(self, event): # o parâmetro event é necessário porque esse método vai acontecer quando o usuário selecionar um valor na caixa de seleção (esse é o evento)
        novo_tamanho = int(self.combo_tamanho.get()) # convertendo o valor atual da caixa de seleção para inteiro (ele por padrão é uma string, que NÃO pode ser usado pra esse propósito) e declarando ele como novo_tamanho
        if novo_tamanho != self.tamanho_atual: # as próximas operações vão ser feitas só se o novo tamanho não for o tamanho atual. isso deixa o programa mais limpinho e eficiente. ps: o tamanho atual é declarado lá no __init__.
            self.tamanho_atual = novo_tamanho # sobrescrevendo o tamanho atual com novo_tamanho
            self._atualizar_matriz(novo_tamanho) # executando o método _atualizar_matriz que está logo acima com novo_tamanho como entrada
            self.resultado_text.delete(1.0, tk.END) # limpando a caixa de resultado por completa (1.0 é o início e tk.END é o fim). isso também deixa o programa mais limpinho e bonito

    def _ler_matriz(self):
        try:
            matriz = []
            for linha in self.entradas_matriz:
                valores_linha = []
                for entrada in linha:
                    # Verifica se a entrada está vazia
                    if entrada.get().strip() == "":
                        raise ValueError("Todas as entradas devem ser preenchidas!")
                    valor = float(entrada.get())
                    valores_linha.append(valor)
                matriz.append(valores_linha)
            return matriz
        except ValueError as e:
            # Propaga o erro específico
            raise ValueError(str(e))

    def _ler_termos(self):
        try:
            termos = []
            for entrada in self.entradas_termos:
                # Verifica se a entrada está vazia
                if entrada.get().strip() == "":
                    raise ValueError("Todas as entradas devem ser preenchidas!")
                valor = float(entrada.get())
                termos.append(valor)
            return termos
        except ValueError as e:
            # Propaga o erro específico
            raise ValueError(str(e))

    # esse método vai pegar os valores das entradas do sistema, tratá-los e usar como entrada pro método resolver da classe ResolvedorSistema, que mora lá no outro arquivo, resolvedor.py.
    def _resolver(self): # o método _resolver vai ser executado quando o usuário clicar no botão de resolver. ao contrário do método _mudar_tamanho, esse método não precisa de parâmetro de evento porque ele vai ser executado apenas quando o usuário clicar no botão, e não quando um valor é atualizado.
        try: # o try serve pra que se houver um erro, ele seja "capturado" e uma mensagem de erro seja exibida.
            coeficientes = self._ler_matriz() # pegando os valores da matriz A do sistema e declarando como coeficientes
            termos = self._ler_termos() # pegando os valores do vetor b do sistema e declarando como termos
            
            tipo, resultado = self.resolvedor.resolver(coeficientes, termos) # usando o método resolver da classe ResolvedorSistema com as entradas coeficientes e termos para resolver o sistema e obter o tipo e o resultado. os resultados vão ser armazenados nas variáveis tipo e resultado respectivamente.
            
            self.resultado_text.delete(1.0, tk.END) # antes de mostrar o resultado, é preciso limpar a caixa de resultado. isso serve pra que se o sistema não for determinado, o resultado do último sistema determinado resolvido não se misture com o tipo do sistema atual.
            
            texto_resultado = f"Tipo: {tipo}\n" # criando a string que vai ser mostrada como resultado. o método resolver já armazenou o tipo do sistema na variável tipo.
            
            # caso o sistema seja determinado, o resultado vai ser escrito na própria string tambem.
            if tipo == "sistema possível e determinado" and resultado is not None:
                variaveis = ['x', 'y', 'z', 'w'] # fazendo a lista de variáveis pra ficar mais fácil de escrever a string
                # usando o método enumerate para obter o índice (posição na lista de variáveis) e o valor de cada elemento da lista resultado.
                # assim, a lista estará formatada da seguinte forma (exemplo):
                # i = 0, valor = 1.00 (x = 1.00)
                # i = 1, valor = 2.00 (y = 2.00)
                # i = 2, valor = 3.00 (z = 3.00)
                # i = 3, valor = 4.00 (w = 4.00)
                for i, valor in enumerate(resultado):
                    # escrevendo a string de resultado já formatada usando expressões.
                    # as expressões fazem com que cada variável seja escrita de acordo com o seu índice (obtido com enumerate e armazenado em i) e então seja seguida pelo seu valor (também obtido com enumerate e armazenado em valor).
                    # assim, eu consigo fazer com que cada resultado seja escrito na sua própria linha, como x = 1.00 \n y = 2.00 \n z = 3.00 \n w = 4.00.
                    # o método .2f é pra que o valor seja arredondado pra duas casas decimais.
                    texto_resultado += f"{variaveis[i]} = {valor:.2f}\n" 
                
            self.resultado_text.insert(1.0, texto_resultado) # inserindo o resultado na caixa de resultado, começando a partir da primeira linha (1.0).
        except ValueError as e: # capturando as mensagens de erro ligadas às entradas (isso geralmente pega os erros que acontecem quando o usuário não preenche as entradas corretamente ou deixa elas vazias)
            messagebox.showerror("Erro", str(e)) # exibindo a mensagem de erro
        except Exception as e: # esse except é mais genérico, capaz de pegar qualquer outro erro que não foi citado antes.
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}") # exibindo a mensagem de erro também

    def executar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    interface = InterfaceSistema()
    interface.executar()