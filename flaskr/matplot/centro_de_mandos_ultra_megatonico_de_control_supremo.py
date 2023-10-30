import matplotlib.pyplot as plt
from .funciones_personalizadas.graficos_plt_f import *


def super_receptor_de_comandos(mando):
    diccionario_hdspm={
        "dispersion":dispercion,
        "pastel":pastel,
        "pastel_con_barra":pastel_con_barra,
        "barras":barras
    }

    if mando in diccionario_hdspm:
        return diccionario_hdspm[mando]
    else:
        raise ValueError (f"no existe la funcion {mando}") 


