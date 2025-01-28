import numpy as np
class ResolvedorSistema:
    def __init__(self): 
        self.resultado = None 
        self.tiposistema = None 
    def resolver(self, coeficientes, termosindependentes):
        try: 
            A = np.array(coeficientes, dtype=float)
            b = np.array(termosindependentes, dtype=float)
            if A.shape[0] == A.shape[1]: 
                det = np.linalg.det(A)                
                if round(det, 5) != 0:
                    self.resultado = np.linalg.solve(A, b)
                    self.tiposistema = "sistema possível e determinado"
                else:
                    rankA = np.linalg.matrix_rank(A)
                    rankAb = np.linalg.matrix_rank(np.c_[A, b])
                    if rankA == rankAb:
                        self.tiposistema = "sistema possível e indeterminado"
                    else:
                        self.tiposistema = "sistema impossível"
            else:
                raise ValueError("o sistema não é quadrado.")
            return self.tiposistema, self.resultado
        except Exception as e:
            raise Exception(f"x_x ocorreu um erro ao resolver o sistema: {str(e)}")