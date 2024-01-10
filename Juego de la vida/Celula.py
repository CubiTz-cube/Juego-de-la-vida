import Config as cf

class Celula:
    def __init__(self, num, muere, nace) -> None:
        self.num = num
        self.muere = muere
        self.nace = nace

    def _celuadyac(self, x, y, mat): #Que cuente cuantas celulas vivas hay alrededor de la celula
        vivas = 0
        if 0 < x < cf.ancho_tablero and 0 < y < cf.alto_tablero:
            for i in range(-1,2):
                for j in range(-1,2):
                    if mat[y+i][x+j][0] == self.num and (i != 0 or j != 0):
                        vivas+=1

        return vivas
  
    def nacer(self, x ,y ,mat):
        celu = self._celuadyac(x, y, mat)

        if celu in self.nace:
            return True
        
        return False
        
    def morir(self, x, y, mat): 
        celu = self._celuadyac(x,y,mat)

        if celu <= self.muere[0] or celu >= self.muere[1]:
            return True

        return False

cel1 = Celula(1, cf.muere_celula, cf.nace_nuevacelula)
cel2 = Celula(2, cf.muere_celula2, cf.nace_nuevacelula2)
cel3 = Celula(3, cf.muere_celula3, cf.nace_nuevacelula3)