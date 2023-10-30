import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms 
import time
import uuid
import json
import io
import xml.etree.ElementTree as ET
from matplotlib.patches import Shadow
from matplotlib.patches import ConnectionPatch
import re
from .otras_cosillas.notitas import notitas_explicativas_mult_col


#funciones de ayuda y detalles de las graficas
    #'confidence_ellipse' es una funcion sacada directamente de la documentacion de la pagina web de matplotlib
    # https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html#sphx-glr-gallery-statistics-confidence-ellipse-py
    # este articulo en especifico trata lo fundamental para hacer el elipse de confianza en el grafico de dispercion 
def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    
    print(x)
    print(y)
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset. 
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson) 
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs) 

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x) 

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def get_correlated_dataset(n, dependency, mu, scale):
    latent = np.random.randn(n, 2)
    dependent = latent.dot(dependency)
    scaled = dependent * scale
    scaled_with_offset = scaled + mu
    # return x and y of the new, correlated dataset
    return scaled_with_offset[:, 0], scaled_with_offset[:, 1]

 #el coeficiente de correlacion puede obtenerce mediante la funcion 'coeficiente'

def coeficiente(x,y):
    covalencia=np.cov(x,y)
    return covalencia[0,1]/np.sqrt(covalencia[0,0] * covalencia[1,1])

    #así como el elipse, se trata de sacar los datos donde se marcará la linea de coorrelacion para el grafico de dispercion 

def curva_for_scatter(x,y,si,ax):
            #y
    y_ = np.sum(y) / len(y)
    x_ = np.sum(x) / len(x)
    
    b = ((len(y) * np.sum(x*y)) - (np.sum(x) * np.sum(y))) / ((len(y) * np.sum(x**2)) - (np.sum(x)**2))

    a = y_-b*x_
    X=np.sum(x)
    yc=a-b

    
    py=yc * si
    print(f"b: {b}")
    print(f"a: {a}")
    print(yc)
    print(py)
    
    ax.plot(si,py)


def pastel_pct(pct, allvals, absl_, unidad,autopact_):

    if autopact_:
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        if absl_: 
            return f"{pct:.1f}%\n({absolute:d} {unidad})"
        else:
            return f"{pct:.1f}%"

#contenido de la funcion adaptada de la documetacion de matplotlib en el ejemplo de guardar como svg el grafico de pastel
#https://matplotlib.org/stable/gallery/misc/svg_filter_pie.html#sphx-glr-gallery-misc-svg-filter-pie-py
def svg_filter_pie(ax,filter_def, labels):

    pies=ax

    for w in pies[0]:
        # set the id with the label.
        w.set_gid(w.get_label())

        # we don't want to draw the edge of the pie
        w.set_edgecolor("none")

    for w in pies[0]:
        # create shadow patch
        s = Shadow(w, -0.01, -0.01)
        s.set_gid(w.get_gid() + "_shadow")
        s.set_zorder(w.get_zorder() - 0.1)
        ax.add_patch(s)


        # save
        f = io.BytesIO()
        plt.savefig(f, format="svg")


    tree, xmlid = ET.XMLID(f.getvalue())

    # insert the filter definition in the svg dom tree.
    tree.insert(0, ET.XML(filter_def))

    for i, pie_name in enumerate(labels):
        pie = xmlid[pie_name]
        pie.set("filter", 'url(#MyFilter)')

        shadow = xmlid[pie_name + "_shadow"]
        shadow.set("filter", 'url(#dropshadow)')

    fn = "svg_filter_pie.svg"
    print(f"Saving '{fn}'")
    ET.ElementTree(tree).write(fn)

def fig_extra_pastel(fig_extra):
    diccionario = {
        "barra": barra_pastel
    }

    if fig_extra in diccionario:
        return diccionario[fig_extra]
    

def barra_pastel(ax2, ax1, x_len, wedges, angulo_rebanada_conectada,rebanada_a_conectar ,argumentos_lista,):
    ratios,labels,bottom,width,color,titulo=argumentos_lista

    for j, (height, label) in enumerate(reversed([*zip(ratios, labels)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color=color, label=label,
                    alpha=0.1 + 0.25 * j)
        ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

    ax2.set_title(titulo)
    ax2.legend()
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(ratios)

    # draw top connecting line
    x = r * np.cos(np.pi / angulo_rebanada_conectada * theta2) + center[rebanada_a_conectar]
    y = r * np.sin(np.pi / angulo_rebanada_conectada * theta2) + center[rebanada_a_conectar % len(center)]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData)
    list_set_color=[]
    for x_i in x_len:
        list_set_color.append(0)
    con.set_color(list_set_color)
    con.set_linewidth(4)
    ax2.add_artist(con)

    x = r * np.cos(np.pi / angulo_rebanada_conectada * theta1) + center[rebanada_a_conectar]
    y = r * np.sin(np.pi / angulo_rebanada_conectada * theta1) + center[rebanada_a_conectar % len(center)]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData)
    con.set_color(list_set_color)
    ax2.add_artist(con)
    con.set_linewidth(4) 



    return ax2


#/



#funciones para obtener y manejar datos

def get_datas(x_or,y_or,x_,y_,pad):
    #data = pd.read_csv(pad)
    x, y = get_x_y(pad,x_,y_,x_or,y_or)
    return x, y

def get_x_y(datos,x,y,x_orient="h",y_orient="v"):
    datos=datos.values
       
    if x_orient == "h":
        x=datos[x,:]
    else:
        
        x=datos[:,x]

    if y_orient == "v":
        y=datos[:,y]
    else:
        y=datos[y,:]
        
    return x, y

# la funcion num_or obtiene las filas o culumnas seleccionadas del archivo csv en str, si esta es un numero significa que se
    # está especificando una fila del archivo, así que solo se convierte en un int y su orientacion es h, pero si es una letra, significa que se está
    # seleccionando una columna (la columna A, B, AB, CD, etc.) por lo tanto su orientacion es 'v' 
def num_or(e):
    if e.isalpha():
        h = "v"
        e = letra_a_numero(e) #en caso de ser una letra, es una columna, y se saca a que numero de columna corresponde la letra

    elif e.isdigit():
        h = "h"
        e = int(e) - 1

    else:
        raise ValueError("se debe proporcionar el numero de una fila o el nombre de una columna")
    
    return e,h

#si es solo una letra entonces es una de las primeras 26 columnas que se pueden ver en una hoja de excel (de la a a la z sin contar la ñ)

def letra_a_numero(letra):
    letra.lower()
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    num = 0

    if len(letra) == 1:
        num = alfabeto.index(letra)
        print(f"es solo una letra y su indice es: {num}")
    elif len(letra) > 1:
        num = multiples_columnas(letra)
    else:
        raise ValueError("no contiene letras")

    return num
  
#la funcion busca la columna correspondiente cuando la letra a superado el limite de la z o es una columna más allá de la 26
#(AA:27, AB:28, AAA: creo que era la 703)
#la funcion en la condicion verifica si la letra está dentro del abecedario, verificando que esté entre A y Z
def multiples_columnas(cadena):
    cadena = cadena.upper() 
    resultado = 0

    for letra in cadena:
        if 'A' <= letra <= 'Z':
            valor_letra = ord(letra) - ord('A') + 1
            resultado = resultado * 26 + valor_letra

    return resultado
#para saver más del funcionamiento de esta, elimina el '#' de la sigiente funcion llamada y mirala con click + ctrl
#notitas_explicativas_mult_col()
#/

#los argumentos enviados por el formulario html son todos str, pero son mandados de una forma en la que sugieren el tipo
#de variable que pretende ser, los que se supone que deben ser int los manda '12' los float '1.0' incluslo las tuplas las 
#envía como '(1,4)' y así y así, la funcion 'list_args_conver' identifica el tipo de variable que sugieren ser y las convierte
def list_args_convert(listas):
    
    lista_args=[]
    for lista in listas:
        args_procesados = []
        print(f"la lista en la que se va iterar contiene {lista}")
        for l in lista:
            if l is not None:
                if isinstance(l, list):
                    mini_lista = list_args_convert(l)
                    args_procesados.append(mini_lista)
                else:
                    caracteres=re.compile(r'[a-z]')
                    if isinstance(l, str):
                        if contiene_numero(l) and "(" not in l and any(c.isalpha() for c in l) is False:
                            if '.' in l:
                                print(f"contenido de: {l} tipo {type(l)}")
                                args_procesados.append(float(l.strip()))
                            else:
                                args_procesados.append(int(l.strip()))

                        elif isinstance(es_booleano(l.strip()), bool):
                            args_procesados.append(es_booleano(l.strip()))
                        
                        elif '(' in l and ')' in l and contiene_numero(l):
                            a_replace=[')','(', ',']
                            for a_rep in a_replace:
                                l = l.replace(a_rep, ' ')

                            tuo_list = [int(dig.strip()) for dig in l.split()]
                            tupla = tuple(tuo_list)

                            args_procesados.append(tupla)

                        else:

                            args_procesados.append(l.strip())
                    else:
                        args_procesados.append(l)
            else:
                args_procesados.append(l)
        lista_args.append(args_procesados)

    return lista_args


def get_keys_groups(x_f,y_f):
    x_keys=list(set(x_f))

    y=[]
    for key in x_keys:
        lugares=np.argwhere(x_f==key)
        y_groups = []
        for lugar in lugares[:,0]:
            y_groups.append(y_f[lugar])
        y.append(y_groups)
            
    return x_keys, y 


def get_medias_de_listas_en_lista(lista_listas):
    medias=[]

    for lista in lista_listas:
        medias.append(sum(lista)/len(lista))
    
    return medias
#print

def str_a_dicc(input_str, conv=False):
    try:
        diccionario = json.loads(input_str)
        if conv:
            for key, val in diccionario.items():
                diccionario[key] = args_convert(val)
            return diccionario
        else:
            return diccionario
    except json.JSONDecodeError:
        return {}


##/

#anti errores 
"""
funciones pensadas para verificar el tipo de valor que contiene una variable, y cambiarlo si 
es necesario, tomar decisiones diferentes y dar excepciones en el caso de que finalmente algo
se escape de las posibilidades anticipadas
"""


#funcion par atratar de limpiar el contenido de una lista o array

def limpiar_arrays(x,y,tipos_x_non,tipos_y_non,tipo_covert_x,tipo_covert_y , tipo_array_x=None, tipo_array_y=None):
    x_mark=x
    for tipo_x in tipos_x_non: #la variable iterada es una lista de tipos no desiados
        for x_i in range(len(x)): #se busca s dentro del array x hay un elemento de algun tipo no deseado
            if isinstance(x[x_i], tipo_x):
               mark = dict_tipos(x_i, tipo_covert_x)#funcion que si encunetra que el elemento es del tipo no deseado lo devuelve transformado o marcado en caso de no ser posible
               x_mark[x_i]=mark  #la lista reemplaza sus valores por los valores nuevos
    y_mark=y
    for tipo_y in tipos_y_non:
        for y_i in range(len(y)):
            if isinstance(y[y_i], tipo_y):
               mark = dict_tipos(y_i, tipo_covert_y)
               y_mark[y_i]=mark

    
    n_x,n_y=eliminar_elementos_marcados(x_mark,y_mark)
    n_y,n_x=eliminar_elementos_marcados(n_y,n_x)

    if isinstance(tipo_array_x, str):
        n_x=tipo_array_covert(n_x,tipo_array_x)

    if isinstance(tipo_array_y, str):
        n_y=tipo_array_covert(n_y,tipo_array_y)

    return n_x, n_y

#/    
                
#diccionario de tipos y funciones llamadas por esta
"""
el diccionario de tipos llamado por la funcion limpiar_arrays,llama a diferentes funciones según
el tipo al que se necesite cambiar un elemento y estas funciones tratan de cambiarlo, de no ser posible cambiarlo
el elemento se reemplazará por una etiqueta que indica que ese elemento tendrá que ser eliminado
"""
def dict_tipos(var, convert_a):
    diccionario = {
        "float": a_float,
        "int": a_int,
        "str": a_str,
        "bool": a_bool,
        
    }

    if diccionario[convert_a]:
        return diccionario[convert_a](var)
    else:
        raise KeyError(f"{convert_a} no wstá en el diccionario")
    
def a_float(var):
    try:
        return  float(var)
    except:
        return "eliminar_elemento"
    
def a_int(var):
    try:
        return int(var)
    except:
        return "eliminar_elemento"
    
def a_str(var):
    try:
        return str(var)
    except:
        return "eliminar_elemento"
    
def a_bool(var):
    if isinstance(es_booleano(var), bool):
        return es_booleano(var)
    else:
        return "eliminar_elemento"

#/    

#busca los elementos etiquetados para borrar, los elimina y elimina su par en el segundo array

def eliminar_elementos_marcados(array1, array2):
    indices = np.where(array1 == "eliminar_elemento")[0]
    nuevo_array1 = np.delete(array1, indices)
    nuevo_array2 = np.delete(array2, indices)
    return nuevo_array1, nuevo_array2

#/



#las funciones convierten el array en un tipo personalisado según se indique 
def tipo_array_covert(array, tipo):
    diccionario={
        "float64":float64_conv,
        "float32":float32_conv,
        "int64": int64_conv,
        "str":str_conv
    }

    if tipo in diccionario:
        return diccionario[tipo](array)
    else:
        raise KeyError(f"{tipo} no wstá en el diccionario")

def float64_conv(c):
    c = c.astype(float)
    return c

def float32_conv(c):
    c=c.astype(np.float32)
    return c

def int64_conv(c):
    c=c.astype(np.int64)

def str_conv(c):
    c=c.astype(str)
#/



#las funciones verifican si una variable str pretende ser de otro tipo y la cambian al tipo que
#indican ser
def contiene_numero(cadena):
    return any(char.isdigit() for char in cadena)

def es_booleano(cadena):
    diction = {
        "False": False,
        "True": True
    }

    return diction.get(cadena, None)

def args_convert(arg):
    
    if contiene_numero(arg):
                if '.' in arg:
                    arg = float(arg.strip())
                else:
                    arg=int(arg.strip())
    elif isinstance(es_booleano(arg), bool):
                arg = es_booleano(arg.strip())

    else:
        arg=arg.strip()
    
    return arg


#funciones para seguridad, trabajan junto a la base de datos, ofrecen nombres y claves

def crear_uui():
    timestamp = int(time.time()) 
    random_str = str(uuid.uuid4())  

    file_name = f"{timestamp}_{random_str}"

    return file_name


#funciones de apoyo con jinja
def lista_de_funciones(num):
    funciones=[isinstance]
    return funciones[num]

def lista_de_tipos(num):
    tipos=[str,list]
    return tipos[num]