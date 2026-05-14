import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. Cargar el dataset
file_path = "Percepción sobre los Juegos Olímpicos (respuestas) - Respuestas de formulario 1.csv"
df = pd.read_csv(file_path)
df.columns = [c.strip() for c in df.columns]

# Simplificar la columna de 'Masa' para la gráfica
def simplificar_masa(val):
    if "fuerza" in str(val).lower(): return "Fuerza"
    if "resistencia" in str(val).lower(): return "Resistencia"
    if "técnico" in str(val).lower(): return "Técnicos"
    return "No seguro"

df['Masa_simp'] = df['Masa'].apply(simplificar_masa)

# 2. Inicializar el grafo y contar frecuencias
G = nx.Graph()
freqs = {}

for col in ['Pais', 'Disciplina', 'Masa_simp']:
    for val in df[col]:
        freqs[val] = freqs.get(val, 0) + 1

# 3. Construir las conexiones (Aristas) basadas en las respuestas
for _, row in df.iterrows():
    pais = row['Pais']
    disc = row['Disciplina']
    masa = row['Masa_simp']
    
    # Conexión País -> Disciplina
    if G.has_edge(pais, disc): G[pais][disc]['weight'] += 1
    else: G.add_edge(pais, disc, weight=1)
        
    # Conexión Disciplina -> Percepción Física (Masa)
    if G.has_edge(disc, masa): G[disc][masa]['weight'] += 1
    else: G.add_edge(disc, masa, weight=1)

# 4. Asignar colores y tamaños
colors = []
sizes = []

for node in G.nodes():
    if node in df['Pais'].values: 
        colors.append('#FF6B6B') # Rojo: País
    elif node in df['Disciplina'].values: 
        colors.append('#4ECDC4') # Turquesa: Disciplina
    else: 
        colors.append('#FFE66D') # Amarillo: Atributo físico
    
    sizes.append(freqs.get(node, 1) * 350 + 800)

# 5. Dibujar el Grafo
plt.figure(figsize=(14, 10), facecolor='#1E1E24')
ax = plt.gca()
ax.set_facecolor('#1E1E24')

# Layout del grafo
pos = nx.spring_layout(G, k=1.2, seed=42)
edges = G.edges()
weights = [G[u][v]['weight'] * 1.5 for u, v in edges]

# Dibujar elementos
nx.draw_networkx_edges(G, pos, edge_color='#929AAB', width=weights, alpha=0.6)
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=sizes, edgecolors='white', linewidths=2)
nx.draw_networkx_labels(G, pos, font_size=11, font_color='white', font_weight='bold')

plt.title("Red de Creencias: Países, Disciplinas y Tipo de Deporte Percibido", color='white', fontsize=18, pad=20)
plt.axis('off')
plt.tight_layout()

# Guardar la imagen
plt.savefig('red_creencias_olimpicas.png', dpi=300, bbox_inches='tight', facecolor='#1E1E24')
plt.show()