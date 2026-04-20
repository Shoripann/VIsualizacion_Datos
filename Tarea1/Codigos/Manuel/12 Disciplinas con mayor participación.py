import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import seaborn as sns

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 10)

# Cargar datos
df = pd.read_csv('athlete_events.csv')

df = df[df['Year'] >= 1980].copy()

# Contar atletas por deporte
sport_counts = df.groupby('Sport')['ID'].nunique().sort_values(ascending=False)
top_sports = sport_counts.head(12)  # Tomamos 12 deportes

# Preparar datos
categories = top_sports.index.tolist()
values = top_sports.values.tolist()

# Crear figura con subplot polar
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='polar')

# Ángulos
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Valores (cerrar el círculo)
values_closed = values + values[:1]

# Colores degradados
colors = plt.cm.viridis(np.linspace(0, 1, N))

# Dibujar área
ax.fill(angles, values_closed, alpha=0.3, color='steelblue')

# Dibujar línea
ax.plot(angles, values_closed, 'o-', linewidth=2, color='darkblue', markersize=8)

# Colorear puntos según valor
for i, (angle, value) in enumerate(zip(angles[:-1], values)):
    ax.scatter(angle, value, c=[colors[i]], s=100, zorder=5)

# Configurar etiquetas
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=16, weight='bold')

# Configurar círculos radiales
ax.set_ylim(0, max(values) * 1.1)
ax.yaxis.grid(True)
ax.xaxis.grid(True)

# Personalizar etiquetas radiales
ax.set_rlabel_position(0)
ax.set_yticklabels([str(int(x)) for x in ax.get_yticks()], size=10)

# Título
plt.title('Cantidad de Atletas por Disciplina\nGráfico de Radar', size=16, weight='bold', pad=30)

# Añadir anotaciones con valores
for angle, value, sport in zip(angles[:-1], values, categories):
    # Ajustar posición de la etiqueta
    offset = max(values) * 0.05
    ax.text(angle, value + offset, str(value), 
            ha='center', va='bottom', size=16, weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

plt.tight_layout()
plt.show()