from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from .matplot.base import controlador
from .matplot.funciones_personalizadas.funciones import num_or, list_args_convert, crear_uui, str_a_dicc, lista_de_funciones, lista_de_tipos, get_datas
import pandas as pd
import ast 
import os

bp = Blueprint("matplt", __name__)
@bp.route('/', methods=('GET', 'POST'))

def gener():
    print("a")
    nam=crear_uui()
    opciones_ads=[[]]
    tipo_grafica_seleccionado=''
    opciones=[[],[]]
    settings_ads=[]
    filas=''
    columnas=''
    contenido=''
    contenido_array_str=''
    df=''
    rut="./flaskr/static/show/"
    rut_txt="./flaskr/output_tx/docs/"
    nam_txt=''
    img_Gen=False
    if request.method == 'POST':
        tipo_grafica_seleccionado = request.form.get('tipo_grafica')
        contenido = request.files['archivo']
        
        if contenido:
            array_contenido=pd.read_csv(contenido)
            nam_txt=crear_uui()
            array_contenido.to_csv(f'{rut_txt}{nam_txt}.txt', sep='\t', index=False)


        elif request.form['array_escondido']:
            nam_request=request.form['array_escondido']
            array_contenido = pd.read_csv(f'{rut_txt}{nam_request}.txt', sep='\t')
            nam_txt=nam_request
        else:
            raise ValueError("no hay no documento ni array")
          
        filas=request.form['filas']
        columnas=request.form['columnas']

        x, xhor = num_or(filas)
        y, yhor = num_or(columnas) 

        
        if tipo_grafica_seleccionado == 'barras':
            opciones = obtener_opciones_barras()
            
        elif tipo_grafica_seleccionado == 'dispersion':
            opciones=obtener_opciones_dispercion()
            

        elif tipo_grafica_seleccionado == 'pastel':
            opciones = obtener_lista_de_pastel(array_contenido)
            opciones_ads=[]
            for op in opciones:
                for op_ in op: 
                    opciones_ads.append(str(op_))
                    
        opciones_ads=[]
        for op in opciones[0]:
                opciones_ads.append(str(op))
        settings_ads=[]
        for setints_ in opciones[1]:
            settings_ads.append(str(setints_))



        if len(opciones) > 0:

            opciones = list_args_convert(opciones)
        else:
            raise ValueError("no jala")
        
        
        if request.form['uii_oculto']:
            nam=request.form['uii_oculto']

        
        controlador(rut,nam ,array_contenido, xhor, yhor,x, y, tipo_grafica_seleccionado, opciones)
        fig=f"{rut.replace('.','')}{nam}.png"
        rut_temp=f"salida_test/{nam}.png"
        print(opciones)

        img_Gen=True

    
    return render_template('matplt/base_dat.html', 
                           fig=nam, opciones_ads=opciones_ads,
                           tipo_grafica_seleccionada=tipo_grafica_seleccionado,
                           func=lista_de_funciones,
                           types=lista_de_tipos,
                           opciones=opciones[0],
                           settings=opciones[1],
                           settings_ads=settings_ads,
                           filas_=filas,
                           columnas_=columnas,
                           array=nam_txt,
                           uuid_r=nam,
                           ygen=img_Gen,
                           false=False,
                           true=True
                           )



def error_test(arg):
    raise ValueError(f"{arg}")

def obtener_opciones_dispercion():
    

    titulo = request.form['titulo_dispersion']
    trazos = request.form['trazos_dispersion']
    arg_trazos = request.form['arg_trazos']
    mean_color = request.form['mean_color_dispersion']
    

    opciones = [titulo, trazos, arg_trazos, mean_color]
    return [opciones]

def obtener_opciones_barras():
    tipo_de_coloreado = request.form.get('barras_colores_por')
    if tipo_de_coloreado == "lista":
        inp_lista=request.form['_barras_mapa_de_color_inp']
        colores = obtener_lista_de_str(inp_lista)
    elif tipo_de_coloreado == "rango":
        colores = request.form.get('barras_select_cmap').strip()
    else:
        raise ValueError(f"{tipo_de_coloreado} no está disponible")
    
    y_label = request.form['barras_y_label']
    x_label = request.form['barras_x_label']

    figzise = request.form['barras_figsize']
    width = request.form['barras_width']

    agrupar_por = request.form.get('barras_agupar_por')

    if agrupar_por == "formula":
        formula = request.form['entrada_para_formula_barras_entrada']
        agrupado = formula
    else:
        agrupado = agrupar_por

    args_list = [colores, y_label, x_label, figzise, width, agrupado]
    return [args_list]

def obtener_lista_de_pastel(array_contenido):
    color_por=request.form.get('pastel_colores_por')
    if color_por=="lista":
        color=request.form['entrada_colores_pastel_input']
    elif color_por == "rango":
        color=request.form.get('selector_colores_pastel')
    else:
        raise ValueError(f"{color}")
     
    
    
    if request.form['pastel_radio']:
        radio = request.form['pastel_radio']
    else:
        radio = '4'
    
    if request.form['centrado_pastel']:
        centrar = request.form['centrado_pastel']
    else:
        centrar='(4,4)'

    if request.form['pastel_wedgeprops']:
        wedgeprops = str_a_dicc(request.form['pastel_wedgeprops'])
    else:
        wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    

    frame = request.form['pastel_frame']
    agrupacion=request.form.get('pastel_modo_de_agrupacion')
    args_list=[color, radio, centrar, wedgeprops, frame, agrupacion]

    setings_pastel=obtener_settings_pastel()
    setting_extras=obtener_settings_extras_pastel(array_contenido)
    return [args_list, setings_pastel, [None]]

def obtener_settings_pastel():
    autopack_activado=request.form.get('selector_autopack_pastel')
    
    if not autopack_activado:
        autopack_activado="False"

    total_pct=request.form.get('total_pct_pastel_activar')
    if not total_pct:
        total_pct="False"

    uni_tot_pct=request.form['entrada_unidades_de_totales_pastel']
    if not uni_tot_pct:
        uni_tot_pct=""
    
    pct_dist=request.form['inputpct_distance_pastel']
    if not pct_dist:
        pct_dist="0.6"

    hatch=request.form['hatch_pastel']
    if not hatch:
        hatch=None
    
    label_dist=request.form['label_distance_pastel']
    if not label_dist:
        label_dist='1.1'
    
    explode=request.form['pastel_explode'].strip()
    if not explode:
        explode=None
    
    cuanto_explode=request.form['cuanto_explode_pastel']
    if not cuanto_explode:
        cuanto_explode=.3

    startang=request.form['start_angle_pastel']
    if not startang:
        startang='0'

    filter_def=request.form['filter_def_pastel']
    if not filter_def:
        filter_def=None

    textprops=request.form['text_porps_pastel']
    if not textprops:
        textprops=None
    
    legend=request.form.get('legend_pastel')
    if not legend:
        legend="False"
    
    titulo_legend=request.form['legend_tit_pastel']
    
    loc_l=request.form['leyend_loc_pastel']
    if not loc_l:
        loc_l="center"

    loc_y=request.form['legend_loc_y_pastel']
    if not loc_y:
        loc_y='0'

    loc_x=request.form['legend_loc_x_pastel']
    if not loc_x:
        loc_x='0'

    figura_extra=request.form.get('figura_extra_pastel')
    if not figura_extra or figura_extra=="--":
        figura_extra=None

    lista_de_settings=[autopack_activado, total_pct, uni_tot_pct, pct_dist, hatch,
                       label_dist, explode, cuanto_explode, startang, filter_def, textprops,
                       legend, titulo_legend, loc_l,loc_y, loc_x, figura_extra]

    return lista_de_settings

def obtener_settings_extras_pastel(array_contenido):
    figura_extra=request.form.get('figura_extra_pastel')
    if figura_extra == "--":
        figura_extra=None

    if figura_extra=="barra":
        barra = get_barra_pastel(array_contenido)
        
    return 


def get_barra_pastel(array_contenido):
    arch_m_n=request.form.get('pastel_barra_mism_arch_nuev')

    if arch_m_n=="mismo":
        array_contenido=array_contenido

    if arch_m_n=="nuevo":
        contenido=request.form['entrada_arch_barra_pastel_input']
        array_contenido=pd.read_csv(contenido)
    filas=request.form['f_c_barra_pastel_y']
    columnas=request.form['f_c_barra_pastel_x']
    
    x_, xhor = num_or(filas)
    y_, yhor = num_or(columnas) 

    x,y=get_datas(xhor,yhor,x_,y_,array_contenido)

    bottom=request.form['bottom_barra_pastel']
    if not bottom:
        bottom = '1'

    width=request.form['barras_pastel_width']
    if not width:
        width='0.2'

    colores=request.form['colores_barra_pastel']

    titulo=request.form['titulo_barra_pastel']
    
    lista_args=[x,y,bottom,width,colores,titulo]
        

    return lista_args

def obtener_lista_de_str(inp_lista):
    lista=[palabra.strip() for palabra in inp_lista.split()]
    return lista


    
 #try:  
            #controlador(array_contenido, xhor, yhor,x, y, tipo_grafica_seleccionado, opciones)
        #except:
            #ocpiones_valores=[] 
            #for i in opciones:
                #ocpiones_valores.append(f"{i}:{type(i)} \n")
            #raise ValueError(f"{ocpiones_valores}")