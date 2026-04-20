import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_csv('athlete_events.csv')

# ============================================
# ANÁLISIS: Evolución de participación femenina vs masculina
# ============================================

# Contar atletas por año y sexo
athletes_by_year_sex = df.groupby(['Year', 'Sex'])['ID'].nunique().reset_index()
athletes_by_year_sex.columns = ['Year', 'Sex', 'Athletes']

# Calcular porcentaje de mujeres por año
total_by_year = athletes_by_year_sex.groupby('Year')['Athletes'].sum().reset_index()
total_by_year.columns = ['Year', 'Total']

female_by_year = athletes_by_year_sex[athletes_by_year_sex['Sex'] == 'F'].merge(total_by_year, on='Year')
female_by_year['Percentage'] = (female_by_year['Athletes'] / female_by_year['Total']) * 100

# Crear figura con subgráficos
fig = plt.figure(figsize=(16, 8))

# Gráfico 1: Evolución de participación por sexo (área apilada)
ax1 = plt.subplot(1, 2, 1)

# Preparar datos para área apilada
pivot_data = athletes_by_year_sex.pivot(index='Year', columns='Sex', values='Athletes').fillna(0)
pivot_data = pivot_data.sort_index()

ax1.fill_between(pivot_data.index, 0, pivot_data['F'], alpha=0.7, label='Mujeres', color='lightcoral')
ax1.fill_between(pivot_data.index, pivot_data['F'], pivot_data['F'] + pivot_data['M'], 
                  alpha=0.7, label='Hombres', color='lightblue')

ax1.set_xlabel('Año', fontsize=11)
ax1.set_ylabel('Número de atletas', fontsize=11)
ax1.set_title('Evolución de Participación por Sexo\n(1896-2016)', fontsize=12, weight='bold')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3, axis='y')

# Gráfico 2: Porcentaje de mujeres a lo largo del tiempo
ax2 = plt.subplot(1, 2, 2)
ax2.plot(female_by_year['Year'], female_by_year['Percentage'], 'o-', linewidth=2.5, 
         markersize=6, color='coral', label='% Mujeres')

# Línea de tendencia
z = np.polyfit(female_by_year['Year'], female_by_year['Percentage'], 1)
p = np.poly1d(z)
ax2.plot(female_by_year['Year'], p(female_by_year['Year']), '--', 
         color='darkred', linewidth=2, label=f'Tendencia (pendiente: {z[0]:.2f}%/año)')

ax2.set_xlabel('Año', fontsize=11)
ax2.set_ylabel('Porcentaje de mujeres (%)', fontsize=11)
ax2.set_title('Porcentaje de Participación Femenina\n(1896-2016)', fontsize=12, weight='bold')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 55)

plt.suptitle('Análisis de Participación Femenina en Juegos Olímpicos\nUn siglo de progreso hacia la igualdad', 
             fontsize=16, weight='bold', y=1.02)

plt.tight_layout()
plt.show()

# ============================================
# GRÁFICO ADICIONAL: Comparación de medallas por sexo
# ============================================

fig2, ax = plt.subplots(figsize=(12, 6))

# Filtrar atletas con medalla
df_medal = df[df['Medal'].notna()]
medals_by_sex = df_medal.groupby(['Year', 'Sex'])['Medal'].count().reset_index()
medals_by_sex.columns = ['Year', 'Sex', 'Medals']

pivot_medals = medals_by_sex.pivot(index='Year', columns='Sex', values='Medals').fillna(0)

ax.plot(pivot_medals.index, pivot_medals['F'], 'o-', linewidth=2, markersize=5, 
         label='Mujeres', color='coral')
ax.plot(pivot_medals.index, pivot_medals['M'], 's-', linewidth=2, markersize=5, 
         label='Hombres', color='steelblue')

ax.set_xlabel('Año', fontsize=12)
ax.set_ylabel('Número de medallas', fontsize=12)
ax.set_title('Evolución de Medallas por Sexo (1896-2016)', fontsize=14, weight='bold')
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================
# GRÁFICO ADICIONAL: Top 10 países con mayor participación femenina
# ============================================

fig3, ax = plt.subplots(figsize=(10, 8))

# Calcular porcentaje de mujeres por país (desde 1980)
df_reciente = df[df['Year'] >= 1980]
female_by_country = df_reciente.groupby('NOC')['Sex'].apply(
    lambda x: (x == 'F').sum() / len(x) * 100
).sort_values(ascending=False).head(10)

colors = ['coral' if i == 0 else 'lightcoral' for i in range(len(female_by_country))]
ax.barh(range(len(female_by_country)), female_by_country.values, color=colors)
ax.set_yticks(range(len(female_by_country)))
ax.set_yticklabels(female_by_country.index)
ax.set_xlabel('Porcentaje de mujeres (%)', fontsize=12)
ax.set_title('Top 10 Países con Mayor Participación Femenina\n(1980-2016)', 
              fontsize=14, weight='bold')
ax.grid(True, alpha=0.3, axis='x')

# Añadir valores
for i, v in enumerate(female_by_country.values):
    ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=10)

plt.tight_layout()
plt.show()

# ============================================
# ESTADÍSTICAS CLAVE
# ============================================

print("\n" + "="*70)
print("RESUMEN DE ESTADÍSTICAS CLAVE DE LOS JUEGOS OLÍMPICOS")
print("="*70)

# Datos generales
print(f"\n📊 DATOS GENERALES:")
print(f"  • Total de atletas únicos: {df['ID'].nunique():,}")
print(f"  • Total de países participantes: {df['NOC'].nunique()}")
print(f"  • Total de deportes: {df['Sport'].nunique()}")
print(f"  • Período analizado: {df['Year'].min()} - {df['Year'].max()}")

# Participación femenina
female_pct = (df[df['Sex'] == 'F']['ID'].nunique() / df['ID'].nunique()) * 100
print(f"\n👩 PARTICIPACIÓN FEMENINA:")
print(f"  • Porcentaje total de atletas mujeres: {female_pct:.1f}%")
print(f"  • Primer año con participación femenina: {df[df['Sex'] == 'F']['Year'].min()}")
print(f"  • Año con mayor % de mujeres: {female_by_year.loc[female_by_year['Percentage'].idxmax(), 'Year']} ({female_by_year['Percentage'].max():.1f}%)")
print(f"  • Crecimiento anual (tendencia): +{z[0]:.2f}% por año")

# Medallas
total_medals = df['Medal'].count()
print(f"\n🥇 MEDALLAS:")
print(f"  • Total de medallas entregadas: {total_medals:,}")
print(f"  • Oro: {df[df['Medal'] == 'Gold'].shape[0]:,}")
print(f"  • Plata: {df[df['Medal'] == 'Silver'].shape[0]:,}")
print(f"  • Bronce: {df[df['Medal'] == 'Bronze'].shape[0]:,}")

# Medallas por sexo
medals_female = df_medal[df_medal['Sex'] == 'F'].shape[0]
medals_male = df_medal[df_medal['Sex'] == 'M'].shape[0]
print(f"\n🏅 MEDALLAS POR SEXO:")
print(f"  • Mujeres: {medals_female:,} medallas ({medals_female/total_medals*100:.1f}%)")
print(f"  • Hombres: {medals_male:,} medallas ({medals_male/total_medals*100:.1f}%)")

# Top países con mayor participación femenina
print(f"\n🏆 TOP 5 PAÍSES CON MAYOR % DE MUJERES (1980-2016):")
for i, (country, pct) in enumerate(female_by_country.head(5).items(), 1):
    print(f"  {i}. {country}: {pct:.1f}%")

# Edades
avg_age_female = df[df['Sex'] == 'F']['Age'].mean()
avg_age_male = df[df['Sex'] == 'M']['Age'].mean()
print(f"\n👶 EDAD PROMEDIO:")
print(f"  • Mujeres: {avg_age_female:.1f} años")
print(f"  • Hombres: {avg_age_male:.1f} años")
print(f"  • Atleta más joven: {df['Age'].min():.0f} años")
print(f"  • Atleta más veterano: {df['Age'].max():.0f} años")