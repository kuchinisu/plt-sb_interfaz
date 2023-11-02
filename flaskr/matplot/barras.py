"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
from funciones_personalizadas.funciones import *
from funciones_personalizadas.graficos_plt_f import *


pad = "recursos/pokemons.csv"
datas = pd.read_csv(pad)

_x, _ = get_x_y(datas,5,5, x_orient="v", y_orient="v")

y=[]
x = list(set(_x))
for _key in x:
    _y=0
    for _p in _x:
        if _key == _p:
            _y+=1
    y.append(_y)

len(y)



fig, ax = plt.subplots(figsize=(15,6))

colores = plt.get_cmap("pink")(np.linspace(.2,.7, len(x)))

ax.bar(x, y, color=colores)

ax.set_ylabel('cantidad')
ax.set_title('cantidad de pokemon por tipo')
#ax.legend(title='cantidad de pokemon por tipo')

plt.show()




###### test
pad="recursos/pokemons.csv"
datas = pd.read_csv(pad)
x, y = get_x_y(datas, 11, 12, x_orient='v', y_orient='v')
x = np.array(x).astype(float)
y = np.array(y).astype(float)

fig, ax = plt.subplots()
ax = dispercion(x,y,ax=ax ,trazos=["elipse"],arg_trazos=True, edgecolor='red')

plt.show()


#barras

fig, ax = plt.subplots(figsize=(15,6))

ax = barras(x,y,"pink",ax=ax)

plt.show()




#pastel


x= list(np.linspace(1,10,50))

fig,ax=plt.subplots()

ax =pastel(x, "pink", ax)

plt.show()



x = [21,2,45,12]
y = ["a","b","x","z"]
bar_rations=[0.25, 0.25, 0.50]
bar_labels=["aa","bb","cc"]

pastel_con_barra(x=x,explode_p=0,labels=y,colores="pink",bar_ratios=bar_rations,bar_labels=bar_labels,title="el pepe")




#####################################################################

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

recipe = ["375 g flour",
          "75 g sugar",
          "250 g butter",
          "300 g berries"]

data = [float(x.split()[0]) for x in recipe]
ingredients = [x.split()[-1] for x in recipe]

wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data, False),
                                  textprops=dict(color="w"),frame=True)

ax.legend(wedges, ingredients,
          title="Ingredients",
          loc="center",
          bbox_to_anchor=(1.4, 0, 0, 1))

plt.setp(autotexts, size=10, weight="bold")

ax.set_title("Matplotlib bakery: A pie")

plt.show()





def func(pct, allvals,absol):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    if absol: 
        return f"{pct:.1f}%\n({absolute:d} )"
    else:
        return f"{pct:.1f}%"

pcts_1=[]
for dat in data:
    pcts_1.append(func(dat, data))
pcts_1


pcts = [func(pct, data) for pct in data]

pcts




labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, hatch=['**O'])





import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import ConnectionPatch

# make figure and assign axis objects
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
fig.subplots_adjust(wspace=0)

# pie chart parameters
overall_ratios = [.27, .56, .17]
labels = ['Approve', 'Disapprove', 'Undecided']
explode = [0.1, 0, 0]
# rotate so that first wedge is split by the x-axis
angle = -180 * overall_ratios[0]
wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                     labels=labels, explode=explode)

# bar chart parameters
age_ratios = [.33, .54, .07, .06]
age_labels = ['Under 35', '35-49', '50-65', 'Over 65']
bottom = 1
width = .2

# Adding from the top matches the legend.
for j, (height, label) in enumerate(reversed([*zip(age_ratios, age_labels)])):
    bottom -= height
    bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                 alpha=0.1 + 0.25 * j)
    ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

ax2.set_title('Age of approvers')
ax2.legend()
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
theta1, theta2 = wedges[0].theta1, wedges[0].theta2
center, r = wedges[0].center, wedges[0].r
bar_height = sum(age_ratios)

# draw top connecting line

x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

plt.show()










import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

recipe = ["375 g flour",
          "75 g sugar",
          "250 g butter",
          "300 g berries"]

data = [float(x.split()[0]) for x in recipe]
ingredients = [x.split()[-1] for x in recipe]


def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d} g)"


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, ingredients,
          title="Ingredients",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("Matplotlib bakery: A pie")

plt.show()

"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import ConnectionPatch

# make figure and assign axis objects
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
fig.subplots_adjust(wspace=0)

# pie chart parameters
overall_ratios = [.27, .56, .17]
labels = ['Approve', 'Disapprove', 'Undecided']
explode = [0.1, 0, 0]
# rotate so that first wedge is split by the x-axis
angle = -180 * overall_ratios[0]
wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                     labels=labels, explode=explode)

# bar chart parameters
age_ratios = [.33, .54, .07, .06]
age_labels = ['Under 35', '35-49', '50-65', 'Over 65']
bottom = 1
width = .2

# Adding from the top matches the legend.
for j, (height, label) in enumerate(reversed([*zip(age_ratios, age_labels)])):
    bottom -= height
    bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                 alpha=0.1 + 0.25 * j)
    
    ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')
    print(f"el valor de .1 más 0.25 por {j} es igual a: {0.1 + 0.25 * j}")

ax2.set_title('Age of approvers')
ax2.legend()
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
theta1, theta2 = wedges[0].theta1, wedges[0].theta2
center, r = wedges[0].center, wedges[0].r
bar_height = sum(age_ratios)

# draw top connecting line
x = r * np.cos(np.pi / 360 * theta2) + center[0]
y = r * np.sin(np.pi / 360 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

plt.show()


360*33/100

