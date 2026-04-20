import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Cargar el dataset
df = pd.read_csv('athlete_events.csv')

# Filtrar datos desde 1980 en adelante y solo para Athletics
df_filtrado = df[(df['Year'] >= 1980) & (df['Sport'] == 'Athletics')].copy()

# Contar la cantidad de atletas únicos por año para Athletics
athletes_by_year = df_filtrado.groupby('Year')['ID'].nunique().sort_index()

print("Atletas en Athletics por año (desde 1980):")
print(athletes_by_year)
print(f"\nTotal de atletas únicos en Athletics desde 1980: {athletes_by_year.sum()}")
print(f"Años analizados: {len(athletes_by_year)}")
print(f"Año con más atletas: {athletes_by_year.idxmax()} ({athletes_by_year.max():.0f})")
print(f"Año con menos atletas: {athletes_by_year.idxmin()} ({athletes_by_year.min():.0f})")

# Preparar datos para el gráfico de radar
years = athletes_by_year.index.tolist()
values = athletes_by_year.values.tolist()

# Número de variables (años)
N = len(years)

# Ángulos para cada eje
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]  # Cerrar el gráfico

# Valores (cerrar el gráfico)
values += values[:1]

# Inicializar el gráfico
fig, ax = plt.subplots(figsize=(14, 12), subplot_kw=dict(projection='polar'))

# Dibujar el gráfico principal
ax.plot(angles, values, 'o-', linewidth=2.5, markersize=7, 
        label='Atletas en Athletics (1980-2016)', color='#2E86AB', zorder=3)
ax.fill(angles, values, alpha=0.25, color='#2E86AB', zorder=2)

# Añadir etiquetas (años)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(years, size=16, ha='center', weight='bold')

# Añadir etiquetas radiales
ax.set_ylim(0, max(values) * 1.15)
ax.set_rlabel_position(30)
ax.set_ylabel('Número de atletas', fontsize=11, weight='bold')

# Personalizar las líneas radiales
ax.grid(True, linestyle='--', alpha=0.5)

# Título
plt.title(f'Cantidad de Atletas entre (1980-2016) \n- Gráfico de Radar', 
          size=16, weight='bold', pad=30)

# Leyenda
plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.05), fontsize=16, framealpha=0.9)

# Mostrar valores en cada punto
for i, (angle, value) in enumerate(zip(angles[:-1], values[:-1])):
    offset = max(values) * 0.03
    # Ajustar posición de la etiqueta según el ángulo
    if angle < pi/2 or angle > 3*pi/2:
        ha = 'left'
    else:
        ha = 'right'
    
    ax.text(angle, value + offset, str(int(value)), 
            ha=ha, va='bottom', fontsize=16, weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='gray'))

# Resaltar años con Juegos Olímpicos (los años pares)
for i, (angle, year) in enumerate(zip(angles[:-1], years)):
    if year % 2 == 0:  # Años olímpicos
        ax.scatter(angle, values[i], c='red', s=120, zorder=5, alpha=0.8, 
                  edgecolors='darkred', linewidth=1.5)

# Añadir nota sobre años olímpicos
plt.figtext(0.5, 0.02, 'Nota: Los puntos rojos indican años con Juegos Olímpicos', 
            ha='center', fontsize=16, style='italic', 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.show()