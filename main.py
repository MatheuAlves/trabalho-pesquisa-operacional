# -*- coding: utf-8 -*-
from sys import argv
import gurobipy as gp
from gurobipy import GRB
from tabulate import tabulate

def readFile():
    try:
        with open(argv[1], 'r') as file:
            # Pegando os macronutrientes dos alimentos
            qtd_foods = file.readline().strip().split(' ')
            if len(qtd_foods) != 1:
                raise Exception('0 ou +1 número de alimentos passados')
            num_foods = int(qtd_foods[0])
            macronutrients = dict()
            for i in range(num_foods):
                n_values = file.readline().strip().split('-')
                name = n_values[0].strip()
                mn_values = list(map(float, n_values[1].strip().split(' ')))
                macronutrients.update({i+1: {'name': name, 'carbs': mn_values[0], 'proteins': mn_values[1]}})
            
            # Pegando os coeficientes de perda
            month_keys = list(map(int, file.readline().strip().split(' ')))
            month_weights = list(map(float, file.readline().strip().split(' ')))
            if len(month_keys) == len(month_weights):
                loss_coeficients = dict(zip(month_keys, month_weights))
            else:
                raise Exception('Número de chaves e pesos diferente')
            
            # Pegando as necessidades das entridades de macronutrientes
            entities = file.readline().strip().split(' ')
            if len(entities) != 1:
                raise Exception('0 ou +1 número de entidades passados')
            num_entities = int(entities[0])
            needed_carbs = dict()
            needed_proteins = dict()
            for i in range(num_entities):
                needed_values = list(map(float, file.readline().strip().split(' ')))
                if len(needed_values) != 2:
                    raise Exception('0, 1 ou +2 valores foram passados para uma entidades')
                needed_carbs.update({i+1: needed_values[0]})
                needed_proteins.update({i+1: needed_values[1]})

            # Pegando o estoque dos alimento/mes
            stock = dict()
            food_month_keys = list(map(int, file.readline().strip().split(' ')))
            if len(food_month_keys) != len(month_keys):
                raise Exception('Coeficientes de pErdas e mesês de alimentos do estoque diferentes')
            for f in range(num_foods):
                food_months = dict()
                food_month_values = file.readline().strip().split(' ')
                if len(food_month_keys) != len(food_month_values):
                    raise Exception('Número de chaves e estoques diferentes')
                for i in range(len(food_month_values)):
                    food_months.update({i+1: float(food_month_values[i])})
                stock.update({f+1: food_months})
                
            return macronutrients, loss_coeficients, needed_carbs, needed_proteins, stock
    except Exception as e:
        print('Erro: {}'.format(str(e)))
    except:
        print('Erro: Não foi possível abrir o arquivo {}'.format(argv[1]))
    return None, None, None, None, None

macronutrients, loss_coeficients, needed_carbs, needed_proteins, stock = readFile()

if macronutrients != None:
    foods = len(macronutrients.keys())
    months = len(loss_coeficients)
    entities = len(needed_carbs)

    # Criando um novo modelo
    model = gp.Model()
    model.setParam(GRB.Param.LogToConsole, 1)
    model.setParam('MIPGap', 0.001)

    # Gerando as variáveis do problema
    x = [model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER) for i in range(foods) for j in range(months) for k in range(entities)]

    # Definição da função objetivo
    obj = gp.LinExpr()
    for i in range(foods):
        for j in range(months):
            for k in range(entities):
                index_x = (i * months * entities) + (j * entities) + k
                obj = obj + x[index_x] * loss_coeficients[j+1]
    model.setObjective(obj, sense=GRB.MINIMIZE)

    # Define as restrições de estoque
    for i in range(foods):
        for j in range(months):
            expr = gp.LinExpr()
            for k in range(entities):
                index_x = (i * months * entities) + (j * entities) + k
                expr = expr + x[index_x]
            model.addConstr(expr <= stock[i+1][j+1])

    # Define as restrições de carboidratos
    for k in range(entities):
        expr = gp.LinExpr()
        for i in range(foods):
            for j in range(months):
                index_x = (i * months * entities) + (j * entities) + k
                expr = expr + x[index_x] * macronutrients[i+1]['carbs']
        model.addConstr(expr >= needed_carbs[k+1])

    # Define as restrições de proteínas
    for k in range(entities):
        expr = gp.LinExpr()
        for i in range(foods):
            for j in range(months):
                index_x = (i * months * entities) + (j * entities) + k
                expr = expr + x[index_x] * macronutrients[i+1]['proteins']
        model.addConstr(expr >= needed_proteins[k+1])

    # Resolvendo o problema
    model.optimize()
    data  = []

    header = []
    header.append('Alimento\\Mês')
    for i in loss_coeficients.keys():
        header.append(i)
    header.append('Total')

    data.append(header)

    for i in range(foods):
        row = []
        sum_food = 0
        row.append(macronutrients[i+1]['name'])
        for j in range(months):
            sum_month = 0
            for k in range(entities):
                index_x = (i * months * entities) + (j * entities) + k
                sum_month += x[index_x].X
            sum_food += sum_month
            row.append(sum_month)
        row.append(sum_food)
        data.append(row)
        
    print(tabulate(data, headers="firstrow", tablefmt="grid"))