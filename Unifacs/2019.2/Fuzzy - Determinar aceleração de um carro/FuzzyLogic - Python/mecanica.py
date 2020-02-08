import math


class Mecanica(object):
    """docstring for Mecanica."""

    def __init__(self, carro, intervalo=4, velocidade_desejada=0):

        super(Mecanica, self).__init__()
        self.CONST_GRAVIDADE = 9.8  # m/s²
        self.CONST_ATRITO_ROLAMENTO = 0.01
        self.CONST_CONVERSAO_KMH_TO_MS = 3.6

        self.carro = carro
        self.intervalo = intervalo
        self.velocidade_desejada_km = velocidade_desejada
        self.velocidade_desejada_m_s = round(velocidade_desejada / self.CONST_CONVERSAO_KMH_TO_MS, 2)
        self.forcaTotal = self.calcular_forcaTotal_carro()
        self.aceleracao = self.calcular_aceleracao_carro()
        self.deltaVelocidade = self.calcular_deltaVelocidade()
        self.forcaAtritoRolamento = self.calcular_forcaAtrito_rolamento()
        self.forcaArrastoAr = self.calcular_forcaResistencia_arrasto()

    # Methods
    def calcular_deltaVelocidade(self):
        return self.carro.velocidade_final - self.carro.velocidade_inicial

    def calcular_forcaResistencia_arrasto(self):
        forca = (-1) * (self.carro.resistencia_arrasto * self.carro.velocidade_final**2)
        return round(forca, 2)

    def calcular_forcaAtrito_rolamento(self):
        forcaRolamento = (-1) * (self.CONST_ATRITO_ROLAMENTO * self.carro.massa_kg * self.CONST_GRAVIDADE)
        forcaGravidade = self.calcular_forcaGravidade_sobre_carro(1)
        tracaoPlusGravidade = self.carro.forcaTracaoMotor + forcaGravidade

        if self.carro.velocidade_final != 0 or forcaRolamento < tracaoPlusGravidade:
            return round(forcaRolamento, 2)
        else:
            return round(tracaoPlusGravidade, 2)

    def calcular_forcaGravidade_sobre_carro(self, apenasForca=0):
        inclinacao = math.sin(math.radians(self.carro.angulo_inclinacao_graus))
        forca = - (self.CONST_GRAVIDADE * self.carro.massa_kg * inclinacao)
        status = 'Plano'
        if inclinacao > 0:
            status = 'Subida'
        elif inclinacao < 0:
            status = 'Descida'
        dados = {"forca": forca, "status": status}
        if apenasForca:
            return round(forca, 2)
        else:
            return dados

    def calcular_forcaTotal_carro(self):
        part1 = self.carro.forcaTracaoMotor
        part2 = self.calcular_forcaResistencia_arrasto() + self.calcular_forcaAtrito_rolamento() + self.calcular_forcaGravidade_sobre_carro(1)
        forcaTotal = part1 - part2
        return round(forcaTotal, 2)

    def calcular_aceleracao_carro(self):
        aceleracao = self.calcular_forcaTotal_carro() / self.carro.massa_kg
        # aceleracao = self.calcular_deltaVelocidade() / self.intervalo
        return round(aceleracao, 2)
