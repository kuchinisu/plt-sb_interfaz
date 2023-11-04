from .centro_de_mandos_ultra_megatonico_de_control_supremo import super_receptor_de_comandos
from .funciones_personalizadas.funciones import get_datas

import matplotlib.pyplot as plt
from random import randint

def controlador(rut,ui,pad, x_or, y_or, x, y, mando, args_t, **kwargs):
    x , y = get_datas(x_or,y_or,x,y,pad) #cuando recibe el numero de las fials y sus orientaciones obtiene los datos ya en array
    print(x, y)
    #fig, ax, = plt.subplots()
    ax=None

    x, y = float_type_grafica(x,y,mando)
    
    
    if len(kwargs) > 0:
        ver =    super_receptor_de_comandos(mando)(x, y, ax, args_t , **kwargs)
    else:
        ver =    super_receptor_de_comandos(mando)(x, y, ax, args_t )

    

    # Generar un nombre de archivo único
    

    plt.savefig(f"{rut}{ui}.png") 

    #if ver is False:
    #    print("nel") 
    #else:
        
    #    plt.show()

def float_type_grafica(x_,y_,comando):
    x=x_
    y=y_

    if isinstance(x[0], (int, float)):
        x = x.astype(float)

    if isinstance(y[0], (int, float)):
        y = y.astype(float)

    return x, y
