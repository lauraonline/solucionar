import tkinter as tk # vou começar importando o módulo tkinter, que é uma biblioteca gráfica que vem com o python.
from tkinter import ttk, messagebox # do tkinter, vou importar ttk, que são os nossos botões, rótulos, etc. e o messagebox, que é a caixa que exibirá mensagens de erro.
import numpy as np # vou importar o numpy, que é uma biblioteca de álgebra linear para python.
from resolvedor import ResolvedorSistema # tambem vou importar a nossa classe existente ResolvedorSistema, que é a "máquina de resolver sistemas".

# essa classe criará a interface gráfica do programa pro usuário poder inserir os dados e obter o resultado.
class InterfaceSistema:
    def criarinterface(self): # definindo o método em que vão ficar os elementos da interface (ex. título, seletor de tamanho, botão, etc.). eu vou usar esse método depois no __init__
        # usando um label pra exibir o nome do programa
        ttk.Label(self.frameprincipal, text="solucionar()", # nome do programa dentro do frameprincipal
                font=('Courier New', 16)).grid(row=0, column=0, columnspan=6, pady=10) # declarando a fonte e tamanho, a posição e o espaçamento dentro do frameprincipal
        
        # usando outro label pra construir o seletor de tamanho do sistema (número de equações)
        ttk.Label(self.frameprincipal, text="Número de equações:").grid(row=1, column=0) # criando a label e o texto
        self.combotamanho = ttk.Combobox(self.frameprincipal, values=[2, 3, 4], width=2) # usando um combobox (vem com o tkinter) pra criar o seletor. parâmetros: valores de 2 a 4 e a largura da caixa de seleção.
        self.combotamanho.set(2) # declarando o valor padrão da caixa de seleção, que é 2 (o sistema mais simples possivel).
        self.combotamanho.grid(row=1, column=1) # declarando a posição da caixa de seleção em relação a janela (na mesma linha do rótulo, mas uma coluna à frente).
        self.combotamanho.bind('<<ComboboxSelected>>', self.mudartamanho) # pegando o valor da caixa de seleção e executando o método mudartamanho, que usará-o como entrada.
        
        # criando o quadro que vai conter a entrada do sistema de equações
        self.framesistema = ttk.LabelFrame(self.frameprincipal, text="Sistema de Equações", padding="10")
        self.framesistema.grid(row=2, column=0, columnspan=6, pady=10) # declarando a posição do quadro em relação a janela e o espaço entre ele e o botão de resolver.
        # eu podia ter criado outra label só pro quadro em que vai ficar o sistema
        
        # criando o botão de resolver o sistema dentro do frameprincipal acima e fazendo ele executar o método resolver
        ttk.Button(self.frameprincipal, text="Resolver", command=self.resolver).grid(row=4, column=0, columnspan=6, pady=10)
        
        # criando a caixa de resultado com um tk.Text dentro do frameprincipal
        self.resultadotext = tk.Text(self.frameprincipal, height=5, width=40) # height = 5 pra poder caber tipo, x, y, z, w. width = 40 pra caber "Tipo: sistema possível e indeterminado"
        self.resultadotext.grid(row=5, column=0, columnspan=6, pady=10) # declarando a posição da caixa de resultado em relação a janela. com row = 5, a caixa de resultado vai ficar abaixo do botão de resolver.

    def __init__(self): # o construtor principal da classe vai puxar bem mais peso, porque aqui eu vou precisar de muito mais elementos do que no resolvedor.
        # crio a janela principal com o construtor tk.Tk() e assinalo o título da janela e o tamanho.
        self.janela = tk.Tk()
        self.janela.title("solucionar()") # esse título é o que fica na barra superior da janela
        self.janela.geometry("400x500")
        
        # declarando o resolvedor que importei do arquivo resolvedor.py. ele vai ser usado no método resolver pra... resolver o sistema. 
        self.resolvedor = ResolvedorSistema()
        
        # criando o quadro que vai ficar imediatamente dentro da janela declarada acima. ela é muito usada no método criarinterface porque ela contém tudo visual do programa.
        self.frameprincipal = ttk.Frame(self.janela, padding="10")
        self.frameprincipal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # chamando o método criarinterface pra fazer a interface e eu poder declarar os valores dos elementos dentro dela
        self.criarinterface()
        
        # declarando o tamanho atual do sistema, que vai ser 2 por padrão.
        self.tamanhoatual = 2
        
        # chamando o método atualizarmatriz pra criar a matriz de entrada inicial
        self.atualizarmatriz(2)

    # esse método serve pra limpar o quadro framesistema declarado em criarinterface e criar uma nova matriz de entrada com o tamanho selecionado pelo usuário. ele também é chamado na abertura do programa pra criar os espacinhos pro usuário inserir a primeira matriz, bem como os símbolos de variável, sinal de igual e sinal de +.
    def atualizarmatriz(self, tamanho): # o parâmetro tamanho é o número de equações que o usuário quer que o sistema tenha
        # destruindo todas as crianças (apagando os widgets) que estão dentro do framesistema
        for widget in self.framesistema.winfo_children():
            widget.destroy()
            
        # declarando as listas em que vão ficar os coeficientes e os termos independentes de cada equação
        self.entradasmatriz = []
        self.entradastermos = []
        # declarando a lista de variáveis padrão
        variaveis = ['x', 'y', 'z', 'w']
        
        # para cada equação do sistema,
        for i in range(tamanho):
            linhacoef = [] # declarando os coeficientes da equação em uma lista temporária
            frameequacao = ttk.Frame(self.framesistema) # criando um frame pra cada equação (fica mais organizado e escalável assim). isso usa o framesistema que eu declarei em criarinterface.
            frameequacao.grid(row=i, column=0, pady=5) # posicionando o frame com base no índice da equação (a primeira vai ficar na linha 0, a segunda na linha 1, etc.). isso faz com que as equações fiquem uma embaixo da outra
            
            # para cada coeficiente na equação atual (x, y, z, w),
            for j in range(tamanho):
                entrada = ttk.Entry(frameequacao, width=5) # criando uma caixa de entrada para o coeficiente dentro do frameequacao declarado acima. width = 5 pra caber um número com duas casas decimais.
                entrada.grid(row=0, column=j*3) # posicionando a caixa de entrada com base no índice do coeficiente (o x vai ficar na coluna 0, o y na coluna 1, etc.). isso faz com que os coeficientes de cada equação fiquem um ao lado do outro. inclusive, eu uso j*3 no column porque entre cada caixa de entrada de coeficiente vai ter três "espaços" (coeficiente, sinal de igual, variável).
                linhacoef.append(entrada) # adicionando a caixa de entrada à lista linhacoef. eu vou usar ela mais lá embaixo
                
                # criando um rótulo pra cada variável com base no índice do coeficiente (x, y, z, w). o +1 no column é pra variável ficar logo depois da caixa de entrada.
                ttk.Label(frameequacao, text=variaveis[j]).grid(row=0, column=j*3 + 1)
                
                # criando um rótulo pro sinal de +. o if, usando o valor (tamanho) que deve ser entrada de toda instância do método atualizarmatriz, checa se o coeficiente não é o último da equação. 
                if j < tamanho - 1:
                    ttk.Label(frameequacao, text="+").grid(row=0, column=j*3 + 2, padx=5) # se não for, o sinal de + é posicionado logo ao lado da variável (x, y, z, w). padx = 5 pra ele não ficar colado na variável.
            
            # criando o rótulo do sinal de igual depois de todos os coeficientes. dá pra saber onde fica o lugar dele porque tamanho*3 é o número de coeficientes + o número de variáveis + o número de sinais de +. padx = 5 pra ele não ficar colado na variável.
            ttk.Label(frameequacao, text="=").grid(row=0, column=tamanho*3, padx=5)
            
            # posicionando a caixa de entrada do termo independente da equação. mesmo esquema da caixa de entrada de coeficiente. também colocando a entrada na lista entradatermo.
            entradatermo = ttk.Entry(frameequacao, width=5)
            entradatermo.grid(row=0, column=tamanho*3 + 1) # calcular o lugar do termo independente é igualzinho ao sinal de igual, só que tamanho*3 + 1 é o número de coeficientes + o número de variáveis + o número de sinais de + + o solitário sinal de igual.
            
            # adicionando as listas linhacoef e entradatermo às listas entradasmatriz e entradastermos. elas serão usadas mais tarde nos métodos lermatriz e lertermos.
            self.entradasmatriz.append(linhacoef)
            self.entradastermos.append(entradatermo)

    # esse método vai pegar o valor da caixa de seleção (self.combotamanho), tratar ele e usar como entrada pro outro método atualizarmatriz
    def mudartamanho(self, event): # o parâmetro event é necessário porque esse método vai acontecer quando o usuário selecionar um valor na caixa de seleção (esse é o evento)
        novotamanho = int(self.combotamanho.get()) # convertendo o valor atual da caixa de seleção para inteiro (ele por padrão é uma string, que NÃO pode ser usado pra esse propósito) e declarando ele como novotamanho
        if novotamanho != self.tamanhoatual: # as próximas operações vão ser feitas só se o novo tamanho não for o tamanho atual. isso deixa o programa mais limpinho e eficiente. ps: o tamanho atual é declarado lá no __init__.
            self.tamanhoatual = novotamanho # sobrescrevendo o tamanho atual com novotamanho
            self.atualizarmatriz(novotamanho) # executando o método atualizarmatriz que está logo acima com novotamanho como entrada
            self.resultadotext.delete(1.0, tk.END) # limpando a caixa de resultado por completa (1.0 é o início e tk.END é o fim). isso também deixa o programa mais limpinho e bonito

    # esse método vai pegar os valores dos coeficientes, que a essa altura estão na lista entradasmatriz. ela é uma lista de listas, onde cada lista é uma linha da matriz.
    # o computador vê ela mais ou menos assim:
    # entradasmatriz = [[x, y, z],
    #                     [a, b, c],
    #                     [d, e, f]]
    # o método vai pegar cada valor de cada entrada, tratá-los pra uso do resolvedor e armazenar tudo em outra lista de listas, que vai ser usada no método resolver.
    def lermatriz(self):
        try: # usando o try pra capturar erros e exibir mensagens de erro
            matriz = [] # declarando a lista que vai armazenar a matriz de coeficientes pra propósitos do método resolver
            for i in self.entradasmatriz: # para cada equação do sistema, (nota mental: i = linhas, j = colunas)
                valoreslinha = [] # declarando os coeficientes de cada equação em uma lista temporária (mesma coisa do linhacoef em atualizarmatriz)
                for j in i: # para cada coeficiente na equação atual, (nota mental: i = linhas, j = colunas)
                    if j.get().strip() == "": # se a entrada estiver vazia,
                        raise ValueError("Todas as entradas devem ser preenchidas!") # mande o usuário preencher todas as entradas
                    valor = float(j.get()) # convertendo o valor pra float (número real)
                    valoreslinha.append(valor) # e armazenando ele na lista valoreslinha
                matriz.append(valoreslinha) # e adicionando a lista valoreslinha à lista matriz
                # a esse ponto, a lista matriz vai ser algo como:
                # matriz = [[x, y, z],
                #           [a, b, c],
                #           [d, e, f]]
                # a principal diferença entre ela e a lista que a gente começou, entradasmatriz, é que as entradas são floats, ou números reais, e o computador consegue trabalhar com elas no método resolver.
            return matriz # retornando a lista matriz como saída do método
        except ValueError as e: # se tiver algum erro,
            raise ValueError(str(e)) # exiba a mensagem de erro em forma de string

    # esse método pega o valor de cada termo independente da equação de dentro da lista entradastermos.
    # em contraste à entradasmatriz, que é uma lista de listas (matriz), entradastermos é uma lista simples (vetor).
    # ela está mais ou menos assim:
    # entradastermos = [x, y, z]
    def lertermos(self):
        try: # usando o try pra capturar erros e exibir mensagens de erro
            termos = [] # declarando a lista que vai armazenar os termos independentes tratados e prontos pro método resolver
            for j in self.entradastermos: # para cada termo independente na equação atual, (nota mental: i = linhas, j = colunas)
                if j.get().strip() == "": # se a entrada estiver vazia,
                    raise ValueError("Todas as entradas devem ser preenchidas!") # mande o usuário preencher todas as entradas (essa parte é igual ao método lermatriz)
                valor = float(j.get()) # convertendo o valor pra float também (número real)
                termos.append(valor) # e armazenando ele na lista termos (essa lista já pode ir pro resolver)
            return termos # retornando a lista termos como a saída do método
            # similarmente ao método lermatriz, a lista termos está idêntica à lista entradastermos:
            # termos = [x, y, z]
            # a diferença é que as entradas são floats, ou números reais, prontos pra ser usados no método resolver abaixo.
        except ValueError as e: # se tiver algum erro,
            raise ValueError(str(e)) # exiba a mensagem de erro em forma de string.

    # esse método vai pegar os valores das entradas do sistema, tratá-los e usar como entrada pro método resolver da classe ResolvedorSistema, que mora lá no outro arquivo, resolvedor.py.
    def resolver(self): # o método resolver vai ser executado quando o usuário clicar no botão de resolver. ao contrário do método mudartamanho, esse método não precisa de parâmetro de evento porque ele vai ser executado apenas quando o usuário clicar no botão, e não quando um valor é atualizado.
        try: # o try serve pra que se o programa encontrar um erro, a mensagem seja memorizada pelo computador pra ser exibida ao usuário
            coeficientes = self.lermatriz() # pegando os valores da matriz A do sistema e declarando como coeficientes
            termos = self.lertermos() # pegando os valores do vetor b do sistema e declarando como termos
            
            tipo, resultado = self.resolvedor.resolver(coeficientes, termos) # usando o método resolver da classe ResolvedorSistema com as entradas coeficientes e termos para resolver o sistema e obter o tipo e o resultado. os resultados vão ser armazenados nas variáveis tipo e resultado respectivamente.
            
            self.resultadotext.delete(1.0, tk.END) # antes de mostrar o resultado, é preciso limpar a caixa de resultado. isso serve pra que se o sistema não for determinado, o resultado do último sistema determinado resolvido não se misture com o tipo do sistema atual.
            
            textoresultado = f"Tipo: {tipo}\n" # criando a string que vai ser mostrada como resultado. o método resolver já armazenou o tipo do sistema na variável tipo.
            
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
                    textoresultado += f"{variaveis[i]} = {valor:.2f}\n" 
                
            self.resultadotext.insert(1.0, textoresultado) # inserindo o resultado na caixa de resultado, começando a partir da primeira linha (1.0).
        except ValueError as e: # capturando as mensagens de erro ligadas às entradas (isso geralmente pega os erros que acontecem quando o usuário não preenche as entradas corretamente)
            messagebox.showerror("Erro", str(e)) # exibindo a mensagem de erro
        except Exception as e: # esse except é mais genérico, pra pegar qualquer outro erro que não foi citado antes.
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}") # exibindo a mensagem de erro também

    def executar(self): # esse método serve pra executar o programa
        self.janela.mainloop() # o mainloop mantém o programa rodando e a janela aberta

# esse if serve pra que a janela seja aberta só se o usuário rodar o arquivo diretamente, e não se alguém importar ele como módulo, pra usar a interface em outro projeto ou algo assim.
if __name__ == "__main__": 
    interface = InterfaceSistema()
    interface.executar() # chamando o método executar que tá logo acima pro programa rodar