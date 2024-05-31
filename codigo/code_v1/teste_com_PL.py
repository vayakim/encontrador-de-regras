from apyori import apriori
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

import random

# Definindo um dataset aleatório de transações
transactions = [
    ['leite', 'pão', 'manteiga'],
    ['leite', 'cerveja', 'pão', 'manteiga'],
    ['leite', 'pão', 'manteiga', 'sorvete'],
    ['leite', 'pão', 'manteiga'],
    ['leite', 'cerveja', 'pão', 'manteiga']
]

# Executando o algoritmo Apriori para descobrir regras de associação
rules = list(apriori(transactions, min_support=0.4, min_confidence=0.6))
for rule in rules:
    print(rule)

# Parâmetros
limite_baldes = 5

# Crie o problema de otimização
prob = LpProblem("Configuracao_Baldes", LpMaximize)

# Variáveis de decisão: uso ou não de cada balde em cada intervalo de tempo
baldes = LpVariable.dicts("Balde", ((i, j) for i in range(len(rules)) for j in range(limite_baldes)), cat="Binary")

# Função objetivo: maximizar a quantidade e qualidade das regras
prob += lpSum(baldes[i, j] * rules[i].support for i in range(len(rules)) for j in range(limite_baldes)), "Total_Regras"

# Restrições:
# 1. Cada regra deve ser atribuída a pelo menos um balde
for i in range(len(rules)):
    prob += lpSum(baldes[i, j] for j in range(limite_baldes)) >= 1, f"Regra_{i}"

# 2. Número máximo de baldes
prob += lpSum(baldes[i, j] for i in range(len(rules)) for j in range(limite_baldes)) <= limite_baldes, "Limite_Baldes"

# Resolva o problema
prob.solve()

# Imprima a solução
print("Status:", prob.status)
print("Número ideal de baldes:", sum(balde.varValue for balde in prob.variables()))
