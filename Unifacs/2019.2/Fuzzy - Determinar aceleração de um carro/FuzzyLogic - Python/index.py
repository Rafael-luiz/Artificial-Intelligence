import carro
import mecanica
import json
import numpy as np
from skfuzzy import control as ctrl
from pprint import pprint

# FUZZY LOGIC -----------------------
carros_json = json.load(open('carros.json', 'r'))

for car in carros_json:
    modeloCarro = car['audi_a4_sedan']
    details = [
        modeloCarro['area_frontal_m2'],
        modeloCarro['aro_roda_inch'],
        modeloCarro['peso_kg'],
        modeloCarro['relacao_transmissao'],
        modeloCarro['torque_motor_nm'],
        modeloCarro['velocidade_maxima']
    ]
    condicao = [
        modeloCarro['condicao']['velocidade_final'],
        modeloCarro['condicao']['velocidade_inicial'],
        modeloCarro['condicao']['velocidade_desejada'],
        modeloCarro['condicao']['angulo_inclinacao_graus']
    ]

Carro = carro.Carro(details[0], details[1], details[2], details[3], details[4], details[5], condicao[0], condicao[1], condicao[2], condicao[3])
Mecanica = mecanica.Mecanica(Carro)

# FUZZY LOGIC -----------------------

# New Antecedent/Consequent objects hold universe variables and membership
# functions
resistencia_rolamento = ctrl.Antecedent(np.arange(0, 101, 1), 'resistencia_rolamento')
diferenca_velocidade = ctrl.Antecedent(np.arange(0, 101, 1), 'diferenca_velocidade')
angulo_inclinacao_graus = ctrl.Antecedent(np.arange(-60, 61, 1), 'angulo_inclinacao_graus')

posicao_acelerador = ctrl.Consequent(np.arange(0, 101, 1), 'posicao_acelerador')

# Auto-membership function population is possible with .automf(3, 5, or 7)
angulo_inclinacao_graus.automf(3, "quant")
posicao_acelerador.automf(3, "quant")
diferenca_velocidade.automf(3, "quant")
resistencia_rolamento.automf(3, "quant")
angulo_inclinacao_graus.view()
# FUZZY RULES
rule1 = ctrl.Rule(
        angulo_inclinacao_graus['low'] &
        diferenca_velocidade['low'] &
        resistencia_rolamento['average'],
        posicao_acelerador['low'])

rule2 = ctrl.Rule(
        angulo_inclinacao_graus['average'] &
        diferenca_velocidade['low'] &
        resistencia_rolamento['low'],
        posicao_acelerador['low'])

rule3 = ctrl.Rule(
        angulo_inclinacao_graus['high'] &
        diferenca_velocidade['average'] &
        resistencia_rolamento['average'],
        posicao_acelerador['high'])

rule4 = ctrl.Rule(
        angulo_inclinacao_graus['high'] &
        diferenca_velocidade['average'] &
        resistencia_rolamento['high'],
        posicao_acelerador['high'])

rule5 = ctrl.Rule(
        angulo_inclinacao_graus['average'] &
        diferenca_velocidade['high'] &
        resistencia_rolamento['high'],
        posicao_acelerador['high'])

# CONTROL SYSTEM CREATION AND SIMULATION
acelerador_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
acelerador = ctrl.ControlSystemSimulation(acelerador_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
constante_velocidade_maxima = 100 / Carro.velocidade_maxima
acelerador.input['diferenca_velocidade'] = abs(condicao[2] - condicao[0]) * constante_velocidade_maxima # (velocidade_final - velocidade_desejada)
acelerador.input['resistencia_rolamento'] = abs(Mecanica.forcaAtritoRolamento) + Carro.torque_motor_kgfm * 1.3
acelerador.input['angulo_inclinacao_graus'] = Carro.angulo_inclinacao_graus

pprint('Resistencia_rolamento: =====================')
pprint(abs(Mecanica.forcaAtritoRolamento) + Carro.torque_motor_kgfm * 1.3)
pprint('Diferenca_velocidade: =====================')
pprint(abs(condicao[2] - condicao[0]) * constante_velocidade_maxima)

# Crunch the numbers
acelerador.compute()
posicao_acelerador.view(sim=acelerador)


print()
pprint("__________ CARRO ___________")
pprint(vars(Carro))
print()
pprint("__________ MECANICA ___________")
pprint(vars(Mecanica))
input('Press ENTER to exit')
