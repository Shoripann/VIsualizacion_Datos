# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_csv("athlete_events.csv")

# Filtrar solo atletas con medalla
df_medal = df[df['Medal'].notna()]

# Crear gráfico de violín por Sexo
plt.figure(figsize=(10, 6))
sns.violinplot(x='Sex', y='Age', data=df_medal, 
               palette={'M': 'lightblue', 'F': 'lightcoral'},
               inner='quartile')

plt.title('Distribución de Edad por Sexo (Atletas con Medalla)', fontsize=14, weight='bold')
plt.xlabel('Sexo', fontsize=12)
plt.ylabel('Edad (años)', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')

# Cambiar etiquetas del eje X
plt.xticks([0, 1], ['Masculino', 'Femenino'])

plt.tight_layout()
plt.show()