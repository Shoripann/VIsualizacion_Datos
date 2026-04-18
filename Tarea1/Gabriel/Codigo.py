import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import urllib.request
import ssl
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import country_converter as coco


# Conexion ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Lectura dataset
df = pd.read_csv("athlete_events.csv")


# -----------|
# GRAFICO 1  |
# -----------------------------------------------------------------|
# Distribución del IMC en los 10 deportes olímpicos más practicados|
# -----------------------------------------------------------------|

df_bio = df.dropna(subset=['Height', 'Weight']).copy()
df_bio['IMC'] = df_bio['Weight'] / ((df_bio['Height'] / 100) ** 2)  # Calculo IMC
df_bio = df_bio[(df_bio['IMC'] >= 15) & (df_bio['IMC'] <= 35)] # Filtro registros poco coherentes

# Filtro top 10 deportes
top_10_deportes = df_bio['Sport'].value_counts().nlargest(10).index.tolist()
df_bio_top = df_bio[df_bio['Sport'].isin(top_10_deportes)].copy()

# Ordenar deportes por mediana de IMC (ascendente)
orden = (df_bio_top.groupby('Sport')['IMC'].median().sort_values().index.tolist())
df_bio_top['Sport'] = pd.Categorical(df_bio_top['Sport'], categories=orden, ordered=True)
df_bio_top = df_bio_top.sort_values('Sport')
medianas = df_bio_top.groupby('Sport')['IMC'].median()

sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
g = sns.FacetGrid(df_bio_top, row="Sport", hue="Sport", aspect=6, height=1.1, palette="viridis")
g.map(sns.kdeplot, "IMC", bw_adjust=.5, clip_on=True, fill=True, alpha=0.85, linewidth=1.5)
g.map(sns.kdeplot, "IMC", clip_on=True, color="w", lw=2, bw_adjust=.5)
g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

# Etiqueta deporte y mediana
def label(_, color, label, **kwargs):
    ax = plt.gca()
    mediana = medianas[label]
    ax.text(0.01, .35, f"{label}", fontweight="bold", color=color, fontsize=10, ha="left", va="center", transform=ax.transAxes)
    ax.text(0.01, .10, f"mediana: {mediana:.1f}", color=color, fontsize=8, alpha=0.85, ha="left", va="center", transform=ax.transAxes)

g.map(label, "IMC")
g.figure.subplots_adjust(hspace=-0.2, top=0.95, bottom = 0.08)
g.set_titles("")
g.set(yticks=[], ylabel="", xlim=(15, 35))
g.despine(bottom=True, left=True)
g.figure.suptitle('Distribución del IMC por Deporte Olímpico', fontsize=14, fontweight='bold')
g.set_xlabels('IMC (Índice de Masa Corporal)', fontsize=11)
plt.show()

# ---------|
# GRAFICO 2|
# -----------------------------------------------------------------|
# Red de especialización deportiva con los top 10 países medalleros|
# -----------------------------------------------------------------|

df_medals = df.dropna(subset=['Medal'])

# Filtro de los 10 paises mas medalleros
top_10_paises = df_medals['NOC'].value_counts().nlargest(10).index.tolist()
df_top = df_medals[df_medals['NOC'].isin(top_10_paises)]

# Filtro los 8 deportes con mas medallas
deportes_top = df_top['Sport'].value_counts().head(8).index.tolist()
df_cuerdas = df_top[df_top['Sport'].isin(deportes_top)]

B = nx.Graph()
B.add_nodes_from(top_10_paises, bipartite=0)
B.add_nodes_from(deportes_top, bipartite=1)

for pais in top_10_paises:
    for deporte in deportes_top:
        medallas = len(df_cuerdas[(df_cuerdas['NOC'] == pais) & (df_cuerdas['Sport'] == deporte)])
        if medallas > 0:
            B.add_edge(pais, deporte, weight=medallas)

# Fondo oscuro
fig, ax = plt.subplots(figsize=(15, 12), facecolor='#1a1a2e')
ax.set_facecolor('#1a1a2e')

# Posiciones
pos = dict()
pos_paises = np.linspace(1, -1, len(top_10_paises))
for i, p in enumerate(top_10_paises):
    pos[p] = (-1, pos_paises[i])

pos_deportes = np.linspace(1, -1, len(deportes_top))
for i, s in enumerate(deportes_top):
    pos[s] = (1, pos_deportes[i])

# Colores por país
colores_paises = {
    pais: plt.cm.tab10(i / len(top_10_paises))
    for i, pais in enumerate(top_10_paises)
}

# Grosor de cuerdas (Pesos)
peso_maximo = max(B[u][v]['weight'] for u, v in B.edges())
cuerda_peso = []
cuerda_color = []
for u, v in B.edges():
    cuerda_peso.append(B[u][v]['weight'] / peso_maximo * 8)
    pais_nodo = u if u in top_10_paises else v
    cuerda_color.append(colores_paises[pais_nodo])

# Conexiones
nx.draw_networkx_edges(B, pos, width=cuerda_peso, edge_color=cuerda_color, alpha=0.4, ax=ax)

# Nodos de deporte y etiquetas
nx.draw_networkx_nodes(B, pos, nodelist=deportes_top, node_color='#2a2a4a', node_size=2800, edgecolors='white', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(B, pos, labels={d: d.replace(' ', '\n') for d in deportes_top}, font_size=8, font_weight='bold', font_color='white', ax=ax)

# Nodos paises 

# Bandera de paises que no estan en la libreria "country_converter"
banderas_locales = {
    'URS': 'C:/Users/Gabriel/Documents/Python/bandera_urss.png',
    'GDR': 'C:/Users/Gabriel/Documents/Python/bandera_gdr.png'
}

for pais in top_10_paises:
    x, y = pos[pais]
    try:
        if pais in banderas_locales:
            img = Image.open(banderas_locales[pais]).convert('RGB')
        else:
            iso_code = coco.convert(names=pais, src='IOC', to='ISO2').lower()
            url = f"https://flagcdn.com/w80/{iso_code}.png"
            cabeceras = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=cabeceras)
            response = urllib.request.urlopen(req)
            img = Image.open(io.BytesIO(response.read())).convert('RGB')

        # Ajuste de la imagen de la bandera
        img = img.resize((80, 53), Image.LANCZOS)
        imagebox = OffsetImage(img, zoom=0.45)
        imagebox.image.axes = ax
        ab = AnnotationBbox(imagebox, (x, y), frameon=True, bboxprops=dict(edgecolor=colores_paises[pais], linewidth=2, boxstyle="round,pad=0.1"))
        ax.add_artist(ab)

        # Etiqueta de paises
        ax.text(x - 0.12, y, pais, fontsize=10, fontweight='bold', ha='right', va='center', color=colores_paises[pais])

    except Exception as e:
        print(f"Error dibujando la bandera de {pais}: {e}")
        nx.draw_networkx_nodes(B, pos, nodelist=[pais], node_color='#ff9999', node_size=1600, edgecolors='white', ax=ax)

# Leyenda de escala de medallas
for medallas, lbl in [(50, '50 medallas'), (200, '200 medallas'), (500, '500 medallas')]:
    ax.plot([], [], linewidth=medallas / peso_maximo * 8, color='white', alpha=0.6, label=lbl)

legend = ax.legend(loc='lower left', fontsize=9, title='Medallas', framealpha=0.2, facecolor='#1a1a2e', labelcolor='white', title_fontsize=10)
legend.get_title().set_color('white')

plt.xlim(-1.8, 1.7)
plt.ylim(-1.2, 1.2)
plt.title("Red de Especialización Olímpica: Top 10 Países", fontsize=17, fontweight='bold', pad=20, color='white')
plt.axis('off')
plt.tight_layout()
plt.subplots_adjust(top=0.93)
plt.show()