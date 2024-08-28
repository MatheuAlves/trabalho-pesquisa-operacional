from sys import argv

def readFile():
    try:
        with open(argv[1], 'r') as file:
            # Pegando os coeficientes de perda
            month_key = list(map(int, file.readline().strip().split(' ')))
            month_weight = list(map(float, file.readline().strip().split(' ')))
            if len(month_key) == len(month_weight):
                loss_coeficients = dict(zip(month_key, month_weight))
            else:
                raise Exception('Número de chaves e pesos diferente')
            # Pegando as necessidades macronutrientes
            entities = file.readline().strip().split(' ')
            if len(entities) != 1:
                raise Exception('0 ou +1 número de entidades passados')
            n_entities = int(entities[0])
            carbs = dict()
            proteins = dict()
            for i in range(n_entities):
                values = list(map(float, file.readline().strip().split(' ')))
                if len(values) != 2:
                    raise Exception('0, 1 ou +2 valores foram passados para uma entidades')
                carbs.update({i+1: values[0]})
                proteins.update({i+1: values[1]})
            # Pegando o estoque dos alimento/mes
            foods = file.readline().strip().split(' ')
            if len(entities) != 1:
                raise Exception('0 ou +1 número de alimentos passados')
            n_foods = int(foods[0])
            food_names = dict()
            stock = dict()
            food_month_keys = list(map(int, file.readline().strip().split(' ')))
            for f in range(n_foods):
                food_months = dict()
                food_month_values = file.readline().strip().split(' ')
                if len(food_month_keys) + 1 != len(food_month_values):
                    raise Exception('Número de chaves e estoques diferentes')
                food_names.update({f+1: food_month_values.pop()})
                for i in range(len(food_month_values)):
                    food_months.update({i+1: float(food_month_values[i])})
                stock.update({f+1: food_months})
            return loss_coeficients, carbs, proteins, food_names, stock
    except Exception as e:
        print('Erro: {}'.format(str(e)))
    except:
        print('Erro: Não foi possível abrir o arquivo {}'.format(argv[1]))
    return None, None, None, None, None

loss_coeficients, carbs, proteins, food_names, stock = readFile()
print(loss_coeficients)
print(carbs)
print(proteins)
print(food_names)
print(stock)