import tkinter as tk 
from tkinter import ttk, messagebox 
import numpy as np 
from resolvedor import ResolvedorSistema 

class InterfaceSistema:
    def criarinterface(self): 
        ttk.Label(self.frameprincipal, text="solucionar()", 
                font=('Courier New', 16)).grid(row=0, column=0, columnspan=6, pady=10) 
        ttk.Label(self.frameprincipal, text="Número de equações:").grid(row=1, column=0) 
        self.combotamanho = ttk.Combobox(self.frameprincipal, values=[2, 3, 4], width=2) 
        self.combotamanho.set(2) 
        self.combotamanho.grid(row=1, column=1) 
        self.combotamanho.bind('<<ComboboxSelected>>', self.mudartamanho) 
        self.framesistema = ttk.LabelFrame(self.frameprincipal, text="Sistema de Equações", padding="10")
        self.framesistema.grid(row=2, column=0, columnspan=6, pady=10) 
        ttk.Button(self.frameprincipal, text="Resolver", command=self.resolver).grid(row=4, column=0, columnspan=6, pady=10)
        self.resultadotext = tk.Text(self.frameprincipal, height=5, width=40) 
        self.resultadotext.grid(row=5, column=0, columnspan=6, pady=10)

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("solucionar()") 
        self.janela.geometry("400x500")
        self.resolvedor = ResolvedorSistema()
        self.frameprincipal = ttk.Frame(self.janela, padding="10")
        self.frameprincipal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.criarinterface()
        self.tamanhoatual = 2
        self.atualizarmatriz(2)

    def atualizarmatriz(self, tamanho): 
        for widget in self.framesistema.winfo_children():
            widget.destroy()
        self.entradasmatriz = []
        self.entradastermos = []
        variaveis = ['x', 'y', 'z', 'w']
        for i in range(tamanho):
            linhacoef = [] 
            frameequacao = ttk.Frame(self.framesistema) 
            frameequacao.grid(row=i, column=0, pady=5) 
            for j in range(tamanho):
                entrada = ttk.Entry(frameequacao, width=5) 
                entrada.grid(row=0, column=j*3) 
                linhacoef.append(entrada)
                ttk.Label(frameequacao, text=variaveis[j]).grid(row=0, column=j*3 + 1)
                if j < tamanho - 1:
                    ttk.Label(frameequacao, text="+").grid(row=0, column=j*3 + 2, padx=5) 
            ttk.Label(frameequacao, text="=").grid(row=0, column=tamanho*3, padx=5)
            entradatermo = ttk.Entry(frameequacao, width=5)
            entradatermo.grid(row=0, column=tamanho*3 + 1) 
            self.entradasmatriz.append(linhacoef)
            self.entradastermos.append(entradatermo)

    def mudartamanho(self, event): 
        novotamanho = int(self.combotamanho.get()) 
        if novotamanho != self.tamanhoatual: 
            self.tamanhoatual = novotamanho 
            self.atualizarmatriz(novotamanho) 
            self.resultadotext.delete(1.0, tk.END) 

    def lermatriz(self):
        try: 
            matriz = [] 
            for i in self.entradasmatriz: 
                valoreslinha = [] 
                for j in i: 
                    if j.get().strip() == "": 
                        raise ValueError("Todas as entradas devem ser preenchidas!") 
                    valor = float(j.get()) 
                    valoreslinha.append(valor) 
                matriz.append(valoreslinha) 
                
                
                
                
                
            return matriz 
        except ValueError as e: 
            raise ValueError(str(e)) 
        
    def lertermos(self):
        try: 
            termos = [] 
            for j in self.entradastermos: 
                if j.get().strip() == "": 
                    raise ValueError("Todas as entradas devem ser preenchidas!") 
                valor = float(j.get()) 
                termos.append(valor) 
            return termos 
        except ValueError as e: 
            raise ValueError(str(e)) 

    def resolver(self): 
        try: 
            coeficientes = self.lermatriz() 
            termos = self.lertermos() 
            tipo, resultado = self.resolvedor.resolver(coeficientes, termos)
            self.resultadotext.delete(1.0, tk.END)
            textoresultado = f"Tipo: {tipo}\n"
            if tipo == "sistema possível e determinado" and resultado is not None:
                variaveis = ['x', 'y', 'z', 'w'] 
                for i, valor in enumerate(resultado):
                    textoresultado += f"{variaveis[i]} = {valor:.2f}\n" 
            self.resultadotext.insert(1.0, textoresultado) 
        except ValueError as e: 
            messagebox.showerror("Erro", str(e)) 
        except Exception as e: 
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}") 
    def executar(self): 
        self.janela.mainloop() 
        
if __name__ == "__main__": 
    interface = InterfaceSistema()
    interface.executar() 