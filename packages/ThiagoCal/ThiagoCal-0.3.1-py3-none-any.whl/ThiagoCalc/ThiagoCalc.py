class Calculadora:
    def __init__(self, numero1, numero2):
        self.numero1 = numero1
        self.numero2 = numero2

    def somar(self):
        return self.numero1 + self.numero2

    def subtrair(self):
        return self.numero1 - self.numero2

    def multiplicar(self):
        return self.numero1 * self.numero2

    def dividir(self):
        if self.numero2 != 0:
            return self.numero1 / self.numero2
        else:
            return "Erro: divisão por zero não é permitida"