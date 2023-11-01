import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np
import matplotlib.cbook as cbook

from .matematicas import *
from .funciones import *

# grafica de disperción

def dict_functs(funct_name, x, y, ax, **kwargs):
    dic_func = {
        "elipse": confidence_ellipse,
        "linea": curva_for_scatter
    }
    if funct_name in dic_func:
        select_funct = dic_func[funct_name]
        if len(kwargs) > 0:
            return select_funct(x, y, ax, **kwargs)  # Pasa los argumentos kwargs aquí
        else:
            return select_funct(x,y,ax)
    else:
        raise ValueError(f"{funct_name} no es una función válida")

#titulo=None, trazos=None, arg_trazos=None, mean_color='red'
def dispercion(x, y, ax, args_t, **kwargs):
    #try:
        titulo, trazos, arg_trazos, mean_color,size_pts, colores_pts, alfa = args_t[0]
        ad_grid = args_t[1][0]
        
        if ax is None:
            fig, ax = plt.subplots()

        x, y= limpiar_arrays(
            x,y,[str,bool],[str,bool],"float","float",tipo_array_x="float64", tipo_array_y="float64"
            )
        
        if mean_color == 'random':
            N = len(x)
            mean_color = 'c'
        if size_pts == 'area':
            size_pts=(30 * np.random.rand(len(x)))**2
        
        if colores_pts=="random":
            N=len(x)
            colores_pts=np.random.rand(N)

        covalencia, coeficiente = cov_coef(x, y)

        x = np.array(x).astype(float)
        y = np.array(y).astype(float)

        ax.scatter(x, y, s=size_pts,c=colores_pts, alpha=alfa)
        ax.axvline(c="grey", lw=1)
        ax.axhline(c="grey", lw=1)

        if isinstance(trazos, list):
            for trazo in trazos:
                if arg_trazos is True:
                    dict_functs(trazo, x, y, ax, **kwargs)
                else:
                    dict_functs(trazo, x, y, ax)
        elif isinstance(trazos, str):
                if arg_trazos is True:
                    dict_functs(trazos, x, y, ax, **kwargs)
                else:
                    dict_functs(trazos, x, y, ax)

        mean_x = np.mean(x)
        mean_y = np.mean(y)

        ax.scatter(mean_x, mean_y, c='red')
        if titulo:
            ax.set_title(titulo)
        #grid
        if ad_grid is not None:
                ax.grid(ad_grid)
        else:
            raise TypeError(f"el valor de 'ad_grid' tiene que ser booleano y es {type(ad_grid)} y contiene {ad_grid}")
        
        


        return ax
    
    #except:
    #    return False


    

#grafico de barras

def barras_superpuestas(x,y,ax,width):
    bottom=np.zeros(3)

    if width is None:
            width=0.6

    for _y,count_y in y.items():
            p=ax.bar(x,count_y,width, width,label=_y,bottom=bottom)

def agrupado_dict(metodo):
    diccionario = {
        "individual": get_elementos_individuales,
        "sumatoria": get_sumatoria_p_grupo,
        "medias": get_medias_p_grupo,
        "mediana":get_mediana_p_grupo ,
        "moda": get_grupo_p_moda,
        "formula":entrada_de_formulas,
        "porcentaje":list_porcentaje
    }
    if metodo in diccionario:
        return diccionario[metodo]
    else:
        raise ValueError(f"{metodo} no está en las formas posibles de agrupar los datos")

def barras(x, y, ax, vars_t):
    colores, y_label, x_label, figzise, width, agrupado = vars_t[0]
    lienal, _ = vars_t[1]

    if ax is None:
        if figzise is None:
            fig, ax = plt.subplots()
        else:
            fig, ax = plt.subplots(figzise=figzise)

    x, y = agrupado_dict(agrupado)(x,y)

    x=[str(val) for val in x]

    if isinstance(colores, list):
        colors=colores
    elif isinstance(colores, str):
        cmap = plt.get_cmap(colores)
        colors=[cmap(value) for value in np.linspace(0.2, 0.7, len(x))]
        
    else:
       raise ValueError("el argumento colores tiene que ser una lista de colores o el nombre de un color valido de matplotlib")
    
    if isinstance(y, dict):
        ax = barras_superpuestas(x,y,ax,width)
    else:
        #ax.bar(y,x) 
        try:
            ax.bar(x,y, color=colors)
           
        except: 
            raise ValueError(f"x: {type(x)}, x[0]: {type(x[2])} y: {type(y)} y[0]: {type(y[2])}")
    
    if lienal is not None:
        if lienal: 
            ax.plot(x,y)
    
    if y_label:
        ax.set_ylabel(y_label)
    if x_label:
        ax.set_xlabel(x_label)
    

    return ax


 
#de pastel


def pastel(x,y,ax, tot_list ):
    lista_val, lista_editor, fig_extra_settings, = tot_list
    colores,radius,center,wedgeprops, frame, forma_agrupacion=lista_val
    #colores,radius=3,center=(4,4),wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True
    if lista_editor is not None:
        try:
            autopact_, total_pct, unidad_de_total, pct_distance_, hatch_, label_distance_,explode_ ,cuanto_explode ,start_angle, filter_def, textporps, legend, legend_tit,\
            leyend_loc, legend_loc_y, legend_loc_x, fig_extra, = lista_editor
        except:
            raise ValueError(f"{lista_editor} tamaño: {len(lista_editor)}")
    else: 
        explode_=None
        fig_extra=None
        hatch_ = None
        pct_distance_=0.6
        label_distance_=1.1
        start_angle=0
        filter_def=None
        textporps=None
        autopact_=False
        cuanto_explode=0
        legend=None
        legend_tit=None
        leyend_loc='center'
        legend_loc_y=0
        legend_loc_x=0
        total_pct=False
        unidad_de_total=''

    if y is not None:
        y=[y_.strip() for y_ in y]

    if fig_extra is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
        fig.subplots_adjust(wspace=0)

    

    else:
        fig, ax1 = plt.subplots()

    #sacar el tipo de coloreado
    if isinstance(colores, str):
        colors = plt.get_cmap(colores)(np.linspace(0.2, 0.7, len(x)))
    elif isinstance(colores, list):
        colors = colores
    else:
        raise ValueError(f"el parametro 'colores' espera un argumento tipo str o lista, no {type(colores)}")
        
    #agrupar los datos en
    if forma_agrupacion:
        if y is not None:
            y ,x = agrupado_dict(forma_agrupacion)(y, x)


    #obtener el start angle index
    if start_angle:
        if isinstance(start_angle,int):
            startangle=start_angle

        elif isinstance(start_angle, str) and y is not None:
            angulos=np.linspace(0,360,len(y))
            try:
                angulo=[y.index(start_angle)]
                porcientos=list_porcentaje(x)
                startangle = -angulos[(angulo[0] + 1) % len(angulos)] * porcientos[angulo[0]]

                
            except:
                startangle=0

        else:
            startangle=0
    else:
        startangle=0

    
    if explode_ is not None:
        explode=[]
        for _ in range(len(x)):
            explode.append(0)
        
        if isinstance(explode_, str) and y is not None:
            rebanada = [y.index(explode_)]
            print(f"la posicion de la rebanada para aplicar el explode es: {rebanada} y es tipo: {type(rebanada)} y explode contiene: {explode_} y Y contiene{y}")
            for slice in rebanada:
                explode[slice]=cuanto_explode
        elif isinstance(explode_, int):
            explode[explode_]=cuanto_explode
        else:
            explode=explode
    else:
        explode = None
        

    

    wedges_ax1, texts_ax1, autotexts_ax1 = ax1.pie(x, explode=explode, labels=y, 
        colors=colors, autopct=lambda pct: pastel_pct(pct, x, total_pct, unidad_de_total, autopact_), pctdistance=pct_distance_, 
         shadow=False, labeldistance=label_distance_, startangle=startangle, 
         radius=radius, counterclock=True, wedgeprops=wedgeprops, 
         textprops=textporps, center=center, frame=frame, 
         rotatelabels=False,  normalize=True, hatch=hatch_, data=None
         )
    
    if filter_def and y is not None:
        svg_filter_pie(ax1,filter_def,y)

    if legend and y is not None:
        ax1.legend(wedges_ax1, y,
          title=legend_tit,
          loc=leyend_loc,
          bbox_to_anchor=(legend_loc_x, legend_loc_y, 0.5, 1))

    if autotexts_ax1:
        plt.setp(autotexts_ax1, size=8, weight="bold")
    
    if fig_extra is not None:
        ax2=fig_extra_pastel(fig_extra=fig_extra)(ax2, ax1, len(x) ,wedges_ax1, angulo, fig_extra_settings)
        return ax1, ax2
    else:
        return ax1



def pastel_con_barra(x,explode_p,labels,colores,bar_ratios,bar_labels,radius=3,wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True,title=None):
    fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0)

    #ajustes del pastel (tengo ganas de pastel)
    overall_ratios=list_porcentaje(x)
    explode=[0 for _ in range(len(x))]
    explode[explode_p]+=0.1
    
    angles = np.linspace(0,-360, len(x))

    angle = angles[explode_p] * overall_ratios[explode_p]

    if isinstance(colores, list):
        colors = colores
    elif isinstance(colores, str):
        colors=plt.get_cmap(colores)(np.linspace(0.2,0.7,len(x)))
    else:
       raise ValueError("el parametro 'colores' espera como argumento el nombre de un color o una lista de colores")

    wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                     labels=labels, explode=explode,colors=colors)

    #parametros de la barra
    bar_ratios = bar_ratios
    bar_labels = bar_labels 
    bottom = 1
    width = .2

    #leyendas
    for j, (height, label) in enumerate(reversed([*zip(bar_ratios, bar_labels)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                    alpha=0.1 + 0.25 * j)
        ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')
    
    if title:
        ax2.set_title(title)
    #theta1
    ax2.legend()
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(bar_ratios)

    #lineas

    # linea superior
    pos_ange=abs(angle)
    
    x,y = conectin_x_y_line(r,pos_ange,theta2,center)
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0 for _ in range(len(bar_ratios))])
    con.set_linewidth(len(bar_ratios))
    ax2.add_artist(con)

    #liena inferior
    
    
    x,y = conectin_x_y_line(r,pos_ange,theta1,center)
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0 for _ in range(len(bar_ratios))])
    ax2.add_artist(con)



    con.set_linewidth(len(bar_ratios))

    plt.show()
#y