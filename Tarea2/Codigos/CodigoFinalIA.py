import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1. Cargar el dataset
file_path = "Percepción sobre los Juegos Olímpicos (respuestas) - Respuestas de formulario 1.csv"
df = pd.read_csv(file_path)
df.columns = [c.strip() for c in df.columns]

# Simplificar la columna de 'Masa'
def simplificar_masa(val):
    if "fuerza" in str(val).lower(): return "Fuerza"
    if "resistencia" in str(val).lower(): return "Resistencia"
    if "técnico" in str(val).lower(): return "Técnicos"
    return "No seguro"

df['Masa_simp'] = df['Masa'].apply(simplificar_masa)

# 2. Inicializar el grafo
G = nx.Graph()
freqs = {}

for col in ['Pais', 'Disciplina', 'Masa_simp']:
    for val in df[col]:
        freqs[val] = freqs.get(val, 0) + 1

# 3. Construir las conexiones
for _, row in df.iterrows():
    pais = row['Pais']
    disc = row['Disciplina']
    masa = row['Masa_simp']
    
    if G.has_edge(pais, disc): G[pais][disc]['weight'] += 1
    else: G.add_edge(pais, disc, weight=1)
        
    if G.has_edge(disc, masa): G[disc][masa]['weight'] += 1
    else: G.add_edge(disc, masa, weight=1)

# 4. Asignar colores y tamaños a los nodos
colors = []
sizes = []

for node in G.nodes():
    if node in df['Pais'].values: 
        colors.append('#FF6B6B') # Rojo
    elif node in df['Disciplina'].values: 
        colors.append('#4ECDC4') # Celeste
    else: 
        colors.append('#FFE66D') # Amarillo
    
    # Escala controlada para evitar que los nodos tapen las líneas (Multiplicador reducido)
    sizes.append(freqs.get(node, 1) * 150 + 1000)

# 5. Configurar la figura (Lienzo más grande)
fig, ax = plt.subplots(figsize=(18, 14), facecolor='#1E1E24')
ax.set_facecolor('#1E1E24')

# Layout muy espaciado para alargar las líneas entre nodos grandes (k=4.5)
pos = nx.spring_layout(G, k=4.5, iterations=200, seed=123)

# Configurar el grosor de las líneas
edges = G.edges()
weights = [G[u][v]['weight'] * 1.2 for u, v in edges]

# Dibujar las líneas debajo
nx.draw_networkx_edges(G, pos, edge_color='#D1D5DB', width=weights, alpha=0.9, ax=ax)

# Dibujar nodos encima
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=sizes, edgecolors='#FFFFFF', linewidths=2.5, ax=ax)

# Añadir las etiquetas en BLANCO
nx.draw_networkx_labels(G, pos, font_size=11, font_color='white', font_weight='bold', ax=ax)

# 6. Crear la Leyenda
red_patch = mpatches.Patch(color='#FF6B6B', label='País dominante')
blue_patch = mpatches.Patch(color='#4ECDC4', label='Disciplina con mayor cantidad de deportistas')
yellow_patch = mpatches.Patch(color='#FFE66D', label='Tipo de deporte que requiere mayor masa muscular')

leg = ax.legend(handles=[red_patch, blue_patch, yellow_patch], 
                 loc='lower right', 
                 fontsize=12, 
                 frameon=True, 
                 facecolor='#2A2A35', 
                 edgecolor='white', 
                 labelcolor='white',
                 title="Leyenda de Nodos",
                 title_fontsize=14)
leg.get_title().set_color('white')

# 7. Añadir Título
plt.title("Mapa de Asociaciones Olímpicas: Naciones, Disciplinas y Demandas Físicas", 
          color='white', fontsize=21, pad=20, fontweight='bold', y=0.92)

plt.axis('off')
plt.tight_layout()

# Mostrar la visualización
plt.show()