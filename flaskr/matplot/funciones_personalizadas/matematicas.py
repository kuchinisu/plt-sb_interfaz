import numpy as np
import math
import ast 
from .funciones import get_keys_groups

def cov_coef(x,y):
    return np.cov(x,y), np.cov(x,y)[0,1] / np.sqrt(np.cov(x,y)[0,0]*np.cov(x,y)[1,1])

# la funcion 'list_porcentaje' simplemente toma una lista de numeros, y saca el porcentaje al que equivale cada
# valor de la lista, es decir, si la lista es [2,2,2,2,2] toma uno a uno los valores, y devueve [.20,.20,.20,.20,.20] osea veinte porciento cada uno
def list_porcentaje(lista, a_string=False):
    total=np.sum(lista)
    list_per=[]
    for n in lista:
        if a_string:
            list_per.append(f"{n / total}")
        else:
            list_per.append(n / total)
    return list_per

def conectin_x_y_line(r,pos_ange,theta,center):
    x = r * np.cos(np.pi / pos_ange * theta) + center[0]
    y = r * np.sin(np.pi / pos_ange * theta) + center[1]
    return x,y

def get_medias_p_grupo(x,y):
    x_ = list(set(x))
    y_ = []
    for x_i in range(len(x_)):
            y__=[]
            for x__i in range(len(x)):
                if x_[x_i] == x[x__i]:
                    y__.append(y[x__i])
            y_.append(np.sum(y__)/len(y__))

    return x_, y_



def entrada_de_formulas(x_, y_, formula_str):
    if isinstance(formula_str, str):
        if "individual" in formula_str:
            formula_str = formula_str.replace("individual", "")
            x_, y_grupos = get_elementos_individuales(x_, y_)
            modo = "ind"
        else:
            x_, y_grupos = get_keys_groups(x_, y_)
            modo = "grup"
        resultados = []

        for i in range(len(y_grupos)):  # Corrección aquí
            y = y_grupos[i]
            x = x_[i]
            n = len(y)
            if modo == "grup":
                maximo_y = max(y)
                if isinstance(x, list):
                    if isinstance(x[0], int):
                        maximo_x = max(x[i])
                    else:
                        maximo_x = None
            else:
                maximo_x = None
                maximo_y = None
            try:
                resultado = ast.literal_eval(formula_str)
                resultados.append(resultado)
            except (ValueError, SyntaxError):
                resultados.append(None)  # Manejar fórmulas no válidas

        return x, resultados
    else:
        raise ValueError(f'{formula_str} no es un str')
    #aun no funciona la netrada de formula para grupamiento


def get_sumatoria_p_grupo(x,y):
    x_ = list(set(x))
    y_ = []
    for x_i in range(len(x_)):
            y__=[]
            for x__i in range(len(x)):
                if x_[x_i] == x[x__i]:
                    y__.append(y[x__i])
            y_.append(np.sum(y__))
    return x_, y_

def get_elementos_individuales(x,y):
     return x,y

def orfenar_min_may(x,y):
    x_ = list(set(x))
    y_ = []
    for x_i in range(len(x_)):
            y__=[]
            for x__i in range(len(x)):
                if x_[x_i] == x[x__i]:
                    y__.append(y[x__i])
            y_.append(np.sum(y__))

    x = x_
    y = y_
    n = len(y)
    for i in range(n):
        for j in range(0, n - i - 1):
            if y[j] < y[j + 1]:
                y[j], y[j + 1] = y[j + 1], y[j]
                x[j], x[j + 1] = x[j + 1], x[j]
    # mediante un metodo de burbuja ordena de mayor a menor los datos
    
    return x, y


def get_mediana_p_grupo(x, y):
    x_key, y_grupos = get_keys_groups(x, y)
    resultados = []

    for grupo in y_grupos:
        n = len(grupo)
        for i in range(n):
            for j in range(0, n - i - 1):
                if grupo[j] < grupo[j + 1]:
                    grupo[j], grupo[j + 1] = grupo[j + 1], grupo[j]

        if len(grupo) % 2 == 0:
            if len(grupo) > 1:
                try:
                    mit_grup1 = grupo[len(grupo) // 2 - 1]
                    mit_grup2 = grupo[len(grupo) // 2]
                    mediana = (mit_grup1 + mit_grup2) / 2
                except:
                    raise ValueError(f"{len(grupo)}")
            elif len(grupo)==1:
                mediana=grupo[0]
            else:
                mediana=0
            # si la lista de numeros no tiene u numero en el medio, o es una cantidad que se puede dividir 
            # entre 2, entonces se toma el ultimo numero de la primera mitad, el primer numero de la segunda mitad
            # y se saca la media entre estos 2, así obteniendo una mediana 
        else:
            if len(grupo) > 0:
                mediana = grupo[math.floor(len(grupo) / 2)]
            else:
                mediana=0

        resultados.append(mediana)

    return x_key, resultados

def get_grupo_p_moda(x,y):
    x_key, y_grupos = get_keys_groups(x,y)
    lista_modas=[]

    for grupo in y_grupos:
        maximo_conteo=0
        moda=None
        if len(grupo) > 0:
            for u in set(grupo):
                conteo = len(np.argwhere(grupo == u))
                if conteo > maximo_conteo:
                    moda = u
                    maximo_conteo = conteo
        else:
            moda=0
            
        lista_modas.append(moda)

               
    return x_key, lista_modas

    # obtiene la moda de una lista de numeros, de la lista de numeros toma uno por uno, de ese numero busca
    # todas las posiciones donde existe un valor igual, y esto obtiene una lista de las posiciones y toma 
    # la longitud de esta lista, y lo compara con el conteo maximo, si lo supera ese numero ocupa la posicion
    # de la moda, se obtiene el siguente numero, busca las posiciones en as que se repite, los vuelve a anotar
    # en una lista de sus posiciones, lo compara de nuevo con el conteo maximo, y si lo supera el conteo máximo se
    # actualiza a ese nuevo conteo y la moda se actualiza tambien