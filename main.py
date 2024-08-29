# -*- coding: utf-8 -*-
from sys import argv
import gurobipy as gp
from gurobipy import GRB

def readFile():
    try:
        with open(argv[1], 'r') as file:
            # Pegando os macronutrientes dos alimentos
            t_foods = file.readline().strip().split(' ')
            if len(t_foods) != 1:
                raise Exception('0 ou +1 número de alimentos passados')
            n_foods = int(t_foods[0])
            nutrients = dict()
            for i in range(n_foods):
                values = file.readline().strip().split('-')
                name = values[0].strip()
                nutrients_values = list(map(float, values[1].strip().split(' ')))
                nutrients.update({i+1: {'name': name, 'carbs': nutrients_values[0], 'proteins': nutrients_values[1]}})

            # Pegando os coeficientes de perda
            month_key = list(map(int, file.readline().strip().split(' ')))
            month_weight = list(map(float, file.readline().strip().split(' ')))
            if len(month_key) == len(month_weight):
                loss_coeficients = dict(zip(month_key, month_weight))
            else:
                raise Exception('Número de chaves e pesos diferente')
            
            # Pegando as necessidades das entridades de macronutrientes
            entities = file.readline().strip().split(' ')
            if len(entities) != 1:
                raise Exception('0 ou +1 número de entidades passados')
            n_entities = int(entities[0])
            needed_carbs = dict()
            needed_proteins = dict()
            for i in range(n_entities):
                values = list(map(float, file.readline().strip().split(' ')))
                if len(values) != 2:
                    raise Exception('0, 1 ou +2 valores foram passados para uma entidades')
                needed_carbs.update({i+1: values[0]})
                needed_proteins.update({i+1: values[1]})

            # Pegando o estoque dos alimento/mes
            stock = dict()
            food_month_keys = list(map(int, file.readline().strip().split(' ')))
            for f in range(n_foods):
                food_months = dict()
                food_month_values = file.readline().strip().split(' ')
                if len(food_month_keys) != len(food_month_values):
                    raise Exception('Número de chaves e estoques diferentes')
                for i in range(len(food_month_values)):
                    food_months.update({i+1: float(food_month_values[i])})
                stock.update({f+1: food_months})
                
            return nutrients, loss_coeficients, needed_carbs, needed_proteins, stock
    except Exception as e:
        print('Erro: {}'.format(str(e)))
    except:
        print('Erro: Não foi possível abrir o arquivo {}'.format(argv[1]))
    return None, None, None, None, None

nutrients, loss_coeficients, needed_carbs, needed_proteins, stock = readFile()

foods = len(nutrients.keys())
months = len(loss_coeficients)
entities = len(needed_carbs)

# Criando um novo modelo
# model = gp.Model()
# model.setParam(GRB.Param.LogToConsole, 1)

# Gerando as variáveis do problema
# x = [model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS) for i in range(len(food_names)) for j in range(len(loss_coeficients)) for k in range(len(needed_carbs))]
x = [f'{i+1}, {j+1}, {k+1}' for i in range(foods) for j in range(months) for k in range(entities)]

# Definição da função objetivo
# obj = gp.LinExpr()
obj = ''
for i in range(foods):
    for j in range(months):
        for k in range(entities):
            index_x = (i * months * entities) + (j * entities) + k
            # obj = obj + x[index_x] * loss_coeficients[j+1]
            obj = obj + '(' + x[index_x] + ') * ' + str(loss_coeficients[j+1]) + '\n'
# model.setObjective(obj, sense=GRB.MINIMIZE)

# Define as restrições de estoque
for i in range(foods):
    for j in range(months):
        # expr = gp.LinExpr()
        expr = ''
        for k in range(entities):
            index_x = (i * months * entities) + (j * entities) + k
            # expr = expr + x[index_x]
            expr = expr + '(' + x[index_x] + ')'
        expr = expr + ' <= ' + str(stock[i+1][j+1])
        # model.addConstr(expr <= stock[i+1][j+1])

# Define as restrições de carboidratos
for k in range(entities):
    # expr = gp.LinExpr()
    expr = ''
    for i in range(foods):
        for j in range(months):
            index_x = (i * months * entities) + (j * entities) + k
            # expr = expr + x[index_x] * nutrients[i+1]['carbs']
            expr = expr + '(' + x[index_x] + ') * ' + str(nutrients[i+1]['carbs']) + ' + '
        expr = expr + ' >= ' + str(needed_carbs[k+1])
        # model.addConstr(expr >= needed_carbs[k+1])

# Define as restrições de proteínas
for k in range(entities):
    # expr = gp.LinExpr()
    expr = ''
    for i in range(foods):
        for j in range(months):
            index_x = (i * months * entities) + (j * entities) + k
            # expr = expr + x[index_x] * nutrients[i+1]['proteins']
            expr = expr + '(' + x[index_x] + ') * ' + str(nutrients[i+1]['proteins']) + ' + '
        expr = expr + ' >= ' + str(needed_proteins[k+1])
        print(expr)
        # model.addConstr(expr >= needed_proteins[k+1])

# Resolvendo o problema
# model.optimize()