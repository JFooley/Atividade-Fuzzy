# Observação:
# Fiz com as entradas inseridas manualmente, mas dá pra automatizar usando 
# dicionário e o método .inputs (no plural) no objeto ControlSystemSimulation
# que nesse caso eu chamei de "output(...)"

import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

def calcularManual(output, pressao):
    loop = True
    while loop:
        print('Digite as entradas')
        temperaturaIn = input('Temperatura: ')
        volumeIn = input('Volume: ')

        output.input['temperatura'] = int(temperaturaIn)
        output.input['volume'] = float(volumeIn)

        output.compute()

        pressao.view(sim=output)
        print(output.output['pressão'])

# Entradas
temperatura = ctrl.Antecedent(np.arange(800, 1200, 1), 'temperatura')
volume = ctrl.Antecedent(np.arange(2, 12, 1), 'volume')

# Saída
pressao = ctrl.Consequent(np.arange(4, 12, 1), 'pressão')

# Funções de pertinencia
temperatura['baixa'] = fuzzy.trapmf(temperatura.universe, [800, 800, 900, 1000])
temperatura['média'] = fuzzy.trimf(temperatura.universe, [900, 1000, 1100])
temperatura['alta'] = fuzzy.trapmf(temperatura.universe, [1000, 1100, 1200, 1200])

volume['pequeno'] = fuzzy.trapmf(volume.universe, [2, 2, 4.5, 7])
volume['médio'] = fuzzy.trimf(volume.universe, [4.5, 7, 9.5])
volume['grande'] = fuzzy.trapmf(volume.universe, [7, 9.5, 12, 12])

pressao['baixa'] = fuzzy.trapmf(pressao.universe, [4, 4, 5, 8])
pressao['média'] = fuzzy.trimf(pressao.universe, [6, 8, 10])
pressao['alta'] = fuzzy.trapmf(pressao.universe, [8, 11, 12, 12])

# Regras
# Regra 1: Se (Temperatura é Baixa) e (Volume é Pequeno)
# Então (Pressão é Baixa)
regra1 = ctrl.Rule(temperatura['baixa'] & volume['pequeno'], pressao['baixa'])

# Regra 2: Se (Temperatura é Média) e (Volume é Pequeno)
# Então (Pressão é Baixa)
regra2 = ctrl.Rule(temperatura['média'] & volume['pequeno'], pressao['baixa'])

# Regra 3: Se (Temperatura é Alta) e (Volume é Pequeno)
# Então (Pressão é Média)
regra3 = ctrl.Rule(temperatura['alta'] & volume['pequeno'], pressao['média'])

# Regra 4: Se (Temperatura é Baixa) e (Volume é Médio)
# Então (Pressão é Baixa)
regra4 = ctrl.Rule(temperatura['baixa'] & volume['médio'], pressao['baixa'])

# Regra 5: Se (Temperatura é Média) e (Volume é Médio)
# Então (Pressão é Média)
regra5 = ctrl.Rule(temperatura['média'] & volume['médio'], pressao['média'])

# Regra 6: Se (Temperatura é Alta) e (Volume é Médio)
# Então (Pressão é Alta)
regra6 = ctrl.Rule(temperatura['alta'] & volume['médio'], pressao['alta'])

# Regra 7: Se (Temperatura é Baixa) e (Volume é Grande)
# Então (Pressão é Média)
regra7 = ctrl.Rule(temperatura['baixa'] & volume['grande'], pressao['média'])

# Regra 8: Se (Temperatura é Média) e (Volume é Grande)
# Então (Pressão é Alta)
regra8 = ctrl.Rule(temperatura['média'] & volume['grande'], pressao['alta'])

# Regra 9: Se (Temperatura é Alta) e (Volume é Grande)
# Então (Pressão é Alta)
regra9 = ctrl.Rule(temperatura['alta'] & volume['grande'], pressao['alta'])

# Criar sistema de controole fuzzy
volumeControle = ctrl.ControlSystem([
    regra1, 
    regra2, 
    regra3, 
    regra4, 
    regra5, 
    regra6, 
    regra7, 
    regra8, 
    regra9 ])
outputPressao = ctrl.ControlSystemSimulation(volumeControle)

# Calcula a saída (inserindo manualmente)
calcularManual(outputPressao, pressao)
