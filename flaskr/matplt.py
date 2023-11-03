from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from .matplot.base import controlador
from .matplot.funciones_personalizadas.funciones import num_or, list_args_convert, crear_uui, str_a_dicc, lista_de_funciones, lista_de_tipos, get_datas

import pandas as pd


bp = Blueprint("matplt", __name__)
@bp.route('/', methods=('GET', 'POST'))

#####funcion principal, esta interactúa con el formulario de la interfaz, toma los datos ingresados para los graficos
# y las opciones para los graficos
def gener():
    print("a")
    nam=crear_uui()#crea un nombre para el archivo de la imagen del grafico
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
        #recoge el tipo de grafico seleccionado en el select de formulario html
        tipo_grafica_seleccionado = request.form.get('tipo_grafica')
        contenido = request.files['archivo'] #toma el archivo dado en el formulario html
        
        if contenido:
            array_contenido=pd.read_csv(contenido)
            nam_txt=crear_uui()
            array_contenido.to_csv(f'{rut_txt}{nam_txt}.txt', sep='\t', index=False)
            #al archivo convertido en un array se guarda como .txt en la carpeta ./flask/output_tx/docs
            #aqui estamos dentro de la carpeta flaskr/ por lo que la carpeta /output_tx esta aquí tmb.
            #esto se hace con la intencion de guardar el contenido del archivo y poder reutilizarlo incluso
            #despues de refrescar la pagina al hacerse el submit


        elif request.form['array_escondido']:
            nam_request=request.form['array_escondido']
            array_contenido = pd.read_csv(f'{rut_txt}{nam_request}.txt', sep='\t')
            nam_txt=nam_request
            #si ya no existe el archivo introducido en el inptut file del formulario quiere decir que la pagina
            #se refrescó, pero cuando creas por primera vez el grafico, el nombre y drectorio de este se guarda 
            #en el value de un imput oculto dentro del html, llamado 'array_escondido', este input obtiene esta
            # informacion ya que se le pasa este dato dentro del return de la funcion, entonces, cuando ya no existe
            # el archivo dentro del input file, se busca la informacion del nombre y ruta del array convertido 
            # en txt en el input oculto, y se recupera de este txt y se vuelve a convertir en array 
        else:
            raise ValueError("no hay no documento ni array")
          
        filas=request.form['filas']
        columnas=request.form['columnas']

        x, xhor = num_or(filas)
        y, yhor = num_or(columnas)# funciones dentro del archivo funciones.py, toman la letra o numero de las 
                                    #filas o culumnas del archivo csv o excel y devuelven a q numero equivalen y si están
                                    # en vertical u horizontal, esto lo pide así la funcion de controlador más adelante 

        
        #llama a la funcion para obtener los datos del formulario según el tipo de grafica escogida
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
        elif tipo_grafica_seleccionado == 'linea':
            opciones = obtener_lista_linea(array_contenido)
                    
        opciones_ads=[]
        for op in opciones[0]:
                opciones_ads.append(str(op))#las opciones_ads se devuelven al formulario html para no perderse
                                                #al refrescarse la pagina 
        settings_ads=[]
        for setints_ in opciones[1]:
            settings_ads.append(str(setints_)) #lo mismo con los settings



        if len(opciones) > 0:

            opciones = list_args_convert(opciones)
        else:
            raise ValueError("no jala")
        
        
        if request.form['uii_oculto']:
            nam=request.form['uii_oculto']
            #si ya se crea el grafico, el nombre de este fue devuelto al formulario html, si se quiere volver a 
            #crear despues de editarlo para actualizarlo a las nuevas opciones se guarda con el mismo nombre
            #para evitar que se acumulen imagenes inecesarias cada que se refresque la pagina, así solo se sobreescribe
            #el archivo

        #el controlador recibe todos los datos, a partir del controlador se comienza a acceder a las 
        #funciones más profundas dentro del backend encargadas de la creacion de los graficos
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
################# dispercion ######################
def obtener_opciones_dispercion():
    

    titulo = request.form['titulo_dispersion']
    trazos = request.form['trazos_dispersion']
    arg_trazos = request.form['arg_trazos']

    select_mean_color=request.form.get('tipo_mean_color_dispersion')
    if select_mean_color == 'seleccionar':
        mean_color = request.form['mean_color_dispersion']
    elif select_mean_color=='random':
        mean_color='random'
    else:
        mean_color='random'

    tma_pts=request.form.get('select_size_puntos_disp')

    colores_pts=request.form.get('select_colores_pts_dispr')

    alfa=request.form['input_alfa_disp']
    if not alfa:
        alfa=1

    settings=obtener_settings_dipsersion()
    opciones = [titulo, trazos, arg_trazos, mean_color,tma_pts,colores_pts,alfa]
    return [opciones, settings]

    #obtiene los settings extras para la edicion del grafico de dispersion que aparecen despues de crear la grafica
def obtener_settings_dipsersion():
    activar_grid=request.form.get('grid_para_disp_select')
    
    if not activar_grid:
        activar_grid="False"
    
    settings=[activar_grid]
    return settings


#################end dispercion ######################

################ barras ####################
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
    
    settings = obtener_settings_barras()
    
    

    args_list = [colores, y_label, x_label, figzise, width, agrupado]
    return [args_list, settings]

#obtiene los setings del grafico de barras que aparecen despues de crear el grafico
def obtener_settings_barras():
    linea = request.form.get('select_agregar_linea_barras')
    if not linea:
        linea = "False"
    settings=[linea, None]
    return settings
###########################/barras############


######################## pastel ##################

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
        centrar='(0,2)'

    if request.form['pastel_wedgeprops']:
        wedgeprops = str_a_dicc(request.form['pastel_wedgeprops'])
    else:
        wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    

    frame = request.form['pastel_frame']
    agrupacion=request.form.get('pastel_modo_de_agrupacion')
    args_list=[color, radio, centrar, wedgeprops, frame, agrupacion]

    setings_pastel=obtener_settings_pastel()
    setting_extras=obtener_settings_extras_pastel(array_contenido)
    return [args_list, setings_pastel, setting_extras]

#obtiene los setings de pastel que aparecen despues de la creacion de la grafica
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

#obtiene el tipo de figura extra agregada a la graifica de pastel, si se selecciono una
#llamará a la funcion que recoge las opciones de ajustes de la grafica escogida 
def obtener_settings_extras_pastel(array_contenido):
    figura_extra=request.form.get('figura_extra_pastel')
    if figura_extra == "--":
        figura_extra=[None]

    if figura_extra=="barra":
        figura_extra = get_barra_pastel(array_contenido)
        
        
    return figura_extra

#funcion que recoge las opciones para la grafica de barras en la grafica de pastel
def get_barra_pastel(array_contenido):
    arch_m_n=request.form.get('pastel_barra_mism_arch_nuev')

    if arch_m_n=="mismo":
        contenido=array_contenido

    if arch_m_n=="nuevo":
        contenido=array_contenido
    filas=request.form['f_c_barra_pastel_y']
    columnas=request.form['f_c_barra_pastel_x']
    
    x_, xhor = num_or(filas)
    y_, yhor = num_or(columnas) 

    x,y=get_datas(xhor,yhor,x_,y_,contenido)

    bottom=request.form['bottom_barra_pastel']
    if not bottom:
        bottom = '1'

    width=request.form['barras_pastel_width']
    if not width:
        width='0.2'

    colores=request.form['colores_barra_pastel']

    titulo=request.form['titulo_barra_pastel']
    
    rebanada_conectada=request.form['pastel_rebanada_conectada_barra']
    if not rebanada_conectada:
        rebanada_conectada=None
    
    lista_args=[x,y,bottom,width,colores,titulo,rebanada_conectada]
        

    return lista_args

######################## end pastel ##################


#################### linea ###################
def obtener_lista_linea(array_contenido):
    nueva_file = request.form.get('linea_select_dat')

    if nueva_file == 'mismos_datos_linea':
        contenido=array_contenido
    elif nueva_file == 'nuevos_datos_linea':
        contenido=request.form['entrada_arch_barra_pastel_input']

    else:
        raise ValueError("sin datos y ni contenido")

    filas=request.form['inp_linea_segunda_linea_dx']
    columnas=request.form['inp_linea_segunda_linea_dy']

    if filas and columnas:
        x_, xhor = num_or(filas)
        y_, yhor = num_or(columnas) 
        x,y=get_datas(xhor,yhor,x_,y_,array_contenido)
    else:
        x,y=(None,None)

    linewidth=request.form['liena_linewidth']
    if not linewidth:
        linewidth = "0.1"
    else:
        if linewidth == '--':
            linewidth="0.1"


    
    lista_args = [x,y,linewidth]

    settings = obtener_settings_linea(array_contenido)

    listas=[lista_args, settings, [None]]
    return listas

def obtener_settings_linea(array_contenido):
    figura_extra=request.form.get('select_linea_figextra')
    if not figura_extra:
        figura_extra=None
        settings_fig_extra=[None]
    else:
        if figura_extra == '--':
            figura_extra = None
            settings_fig_extra=[None]
        elif figura_extra == "linea":
            settings_fig_extra=get_linea_linea(array_contenido)

    settings=[figura_extra]

    return settings

def get_linea_linea(array_contenido):
    """
    nueva_file=request.form.get('linea_fig_extra_nuev_dat')
    if nueva_file == 'mismos_datos_linea':
        contenido=array_contenido
    elif nueva_file == 'nuevos_datos_linea':
        contenido=request.form['entrada_arch_barra_pastel_input']
    

    filas=request.form['inp_linea_segunda_linea_dx']
    columnas=request.form['inp_linea_segunda_linea_dy']

    if filas and columnas:
        x_, xhor = num_or(filas)
        y_, yhor = num_or(columnas) 
        x,y=get_datas(xhor,yhor,x_,y_,array_contenido)

    lista=[x, y, "1"]
    settings=[None]
    fig_extra=[None]

    total=[lista,settings,fig_extra]
    """
    return 

################ end linea ###################

def obtener_lista_de_str(inp_lista):
    lista=[palabra.strip() for palabra in inp_lista.split()]
    return lista
