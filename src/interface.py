import tkinter as tk # importamos o módulo tkinter, que é uma biblioteca gráfica que vem com o python.
from tkinter import ttk, messagebox # do tkinter, importamos ttk, que são os nossos botões, rótulos, etc. e o messagebox, que é a caixa que exibirá mensagens de erro.
import numpy as np # importamos o numpy, que é uma biblioteca de álgebra linear para python.
from resolvedor import ResolvedorSistema # importamos a nossa classe existente ResolvedorSistema, que é a "máquina de resolver sistemas".

class InterfaceSistema:
    def __init__(self):
        # Criando a janela principal
        self.janela = tk.Tk()
        self.janela.title("Resolvedor de Sistemas Lineares")
        self.janela.geometry("800x500")
        
        # Inicializando o resolvedor
        self.resolvedor = ResolvedorSistema()
        
        # Criando o frame principal
        self.frame_principal = ttk.Frame(self.janela, padding="10")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Criando os elementos da interface
        self._criar_interface()
        
        # Tamanho atual do sistema
        self.tamanho_atual = 2
        
        # Criando a matriz de entrada inicial
        self._atualizar_matriz(2)

    def _criar_interface(self):
        # Título
        ttk.Label(self.frame_principal, text="Resolvedor de Sistemas Lineares", 
                 font=('Arial', 16)).grid(row=0, column=0, columnspan=6, pady=10)
        
        # Seletor de tamanho
        ttk.Label(self.frame_principal, text="Número de equações:").grid(row=1, column=0)
        self.combo_tamanho = ttk.Combobox(self.frame_principal, values=[2, 3, 4], width=5)
        self.combo_tamanho.set(2)
        self.combo_tamanho.grid(row=1, column=1)
        self.combo_tamanho.bind('<<ComboboxSelected>>', self._mudar_tamanho)
        
        # Frame para o sistema de equações
        self.frame_sistema = ttk.LabelFrame(self.frame_principal, text="Sistema de Equações", padding="10")
        self.frame_sistema.grid(row=2, column=0, columnspan=6, pady=10)
        
        # Botão de resolver (agora centralizado)
        ttk.Button(self.frame_principal, text="Resolver", command=self._resolver).grid(row=4, column=0, columnspan=6, pady=10)
        
        # Área de resultado
        self.resultado_text = tk.Text(self.frame_principal, height=5, width=40)
        self.resultado_text.grid(row=5, column=0, columnspan=6, pady=10)

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

    def _mudar_tamanho(self, event):
        novo_tamanho = int(self.combo_tamanho.get())
        if novo_tamanho != self.tamanho_atual:
            self.tamanho_atual = novo_tamanho
            self._atualizar_matriz(novo_tamanho)
            # Limpa a área de resultado
            self.resultado_text.delete(1.0, tk.END)

    def _ler_matriz(self):
        try:
            matriz = []
            for linha in self.entradas_matriz:
                valores_linha = []
                for entrada in linha:
                    valor = float(entrada.get() or 0)
                    valores_linha.append(valor)
                matriz.append(valores_linha)
            return matriz
        except ValueError:
            return None

    def _ler_termos(self):
        try:
            termos = []
            for entrada in self.entradas_termos:
                valor = float(entrada.get() or 0)
                termos.append(valor)
            return termos
        except ValueError:
            return None

    def _resolver(self):
        coeficientes = self._ler_matriz()
        termos = self._ler_termos()
        
        if coeficientes is None or termos is None:
            messagebox.showerror("Erro", "Por favor, insira apenas números válidos")
            return
            
        try:
            tipo, resultado = self.resolvedor.resolver(coeficientes, termos)
            # Limpa o texto anterior
            self.resultado_text.delete(1.0, tk.END)
            
            # Mostra o tipo do sistema
            texto_resultado = f"Tipo: {tipo}\n"
            
            # Mostra os valores das variáveis APENAS se o sistema for determinado
            if tipo == "sistema possível e determinado" and resultado is not None:
                variaveis = ['x', 'y', 'z', 'w']
                for i, valor in enumerate(resultado):
                    texto_resultado += f"{variaveis[i]} = {valor:.2f}\n"
                
            self.resultado_text.insert(tk.END, texto_resultado)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def executar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    interface = InterfaceSistema()
    interface.executar()