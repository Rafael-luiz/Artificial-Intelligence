class Carro(object):
    """docstring for Carro."""

    def __init__(self, area_frontal, aro, peso, relacao_transmissao, torque, velocidade_maxima, velocidade_final=0, velocidade_inicial=0, velocidade_desejada=0, angulo_inclinacao_graus=0):

        CONST_GRAVIDADE = 9.8  # m/s²
        CONST_CONVERSAO_NM_TO_KGFM = 0.1019716212978  # kgf·m
        CONST_CONVERSAO_INCH_TO_M = 39.3700787402
        CONST_RESISTENCIA_ARRASTO = 0.396  # (1.2 x 0.33) Kg/m³

        super(Carro, self).__init__()
        self.peso_kg = peso
        self.torque_nm = torque
        self.relacao_transmissao = relacao_transmissao
        self.aro_inch = aro
        self.area_frontal = area_frontal
        self.massa_kg = round(peso / CONST_GRAVIDADE, 2)
        self.torque_motor_kgfm = round(torque * CONST_CONVERSAO_NM_TO_KGFM, 2)
        self.raio_roda_m = round(aro / CONST_CONVERSAO_INCH_TO_M, 2)
        self.resistencia_arrasto = round(CONST_RESISTENCIA_ARRASTO * area_frontal, 2)
        self.velocidade_final = velocidade_final
        self.velocidade_inicial = velocidade_inicial
        self.forcaTracaoMotor = self.getforcaTracao_motor()
        self.angulo_inclinacao_graus = angulo_inclinacao_graus
        self.posicao_acelerador = 0
        self.velocidade_maxima = velocidade_maxima

    # Getters and Setters
    def getPeso(self):
        return self.peso

    def setPeso(self, peso):
        self.peso = peso

    def getTorque(self):
        return self.torque

    def setTorque(self, torque):
        self.torque = torque

    def getRel_transmissao(self):
        return self.rel_transmissao

    def setRel_transmissao(self, rel_transmissao):
        self.rel_transmissao = rel_transmissao

    def getAro(self):
        return self.aro

    def setAro(self, aro):
        self.aro = aro

    def getArea_frontal(self):
        return self.area_frontal

    def setArea_frontal(self, area_frontal):
        self.area_frontal = area_frontal

    def getvelocidade_final(self):
        return self.velocidade_final

    def setvelocidade_final(self, velocidade_final):
        self.velocidade_final = velocidade_final

    # Methods
    def getforcaTracao_motor(self):
        part1 = self.peso_kg * self.torque_motor_kgfm
        part2 = self.relacao_transmissao / self.raio_roda_m
        return part1 * part2

    def getPosicaoAcelerador(self):
        return self.posicao_acelerador

    def setPosicaoAcelerador(self, posicao):
        self.posicao_acelerador = posicao
