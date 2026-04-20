import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_csv("athlete_events.csv")

# Filtrar solo atletas con medalla
df_medal = df[df['Medal'].notna()]

# Crear gráfico de violín
plt.figure(figsize=(10, 6))
sns.violinplot(x='Medal', y='Age', data=df_medal, 
               palette={'Gold': 'gold', 'Silver': 'silver', 'Bronze': '#cd7f32'},
               inner='quartile')

plt.title('Distribución de Edad por Tipo de Medalla', fontsize=14, weight='bold')
plt.xlabel('Tipo de Medalla', fontsize=12)
plt.ylabel('Edad (años)', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()