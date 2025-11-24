import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import os

# --- CARGAR DATOS ---
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(ruta_script, 'vuelos_con_clusters.csv')

try:
    df = pd.read_csv(ruta_csv)
except FileNotFoundError:
    print("Error: No se encuentra 'vuelos_con_clusters.csv'")
    exit()

# Configuración de estilo
sns.set(style="whitegrid")

# --- GRÁFICA 1: BOXPLOT MEJORADO (Retrasos) ---
plt.figure(figsize=(12, 6))
# Filtramos outliers extremos visualmente para que se aprecie la caja
sns.boxplot(x='Cluster', y='arr_delay', data=df, showfliers=False, palette="Set2")
plt.title('Distribución de Retrasos por Clúster (Sin Outliers Extremos)', fontsize=14)
plt.ylabel('Minutos de Retraso en Llegada')
plt.xlabel('ID de Clúster')
plt.xticks([0, 1, 2, 3], ['0: Largo Alcance', '1: Congestión', '2: Eficiente', '3: Crítico'])
plt.savefig(os.path.join(ruta_script, 'boxplot_final.png'))
print("1. Boxplot generado.")

# --- GRÁFICA 2: SCATTER PLOT CON PCA ---
# Recalculamos PCA solo para visualizar 2D
features = ['dep_delay', 'arr_delay', 'taxi_out', 'distance', 'air_time']
x = StandardScaler().fit_transform(df[features])
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
pca_df = pd.DataFrame(data=principalComponents, columns=['PC1', 'PC2'])
pca_df['Cluster'] = df['Cluster']

plt.figure(figsize=(10, 8))
sns.scatterplot(x="PC1", y="PC2", hue="Cluster", data=pca_df, palette="viridis", s=60, alpha=0.7)
plt.title('Mapa de Clústeres (Proyección PCA 2D)', fontsize=14)
plt.xlabel('Componente Principal 1 (Varianza Principal)')
plt.ylabel('Componente Principal 2')
plt.legend(title='Clúster', loc='upper right')
plt.savefig(os.path.join(ruta_script, 'pca_clusters.png'))
print("2. Gráfica PCA generada.")

# --- GRÁFICA 3: RADAR CHART (COMPARATIVA) ---
# Normalizamos los datos para que sean comparables en el radar (0 a 1)
scaler_minmax = MinMaxScaler()
df_normalized = pd.DataFrame(scaler_minmax.fit_transform(df[features]), columns=features)
df_normalized['Cluster'] = df['Cluster']
perfil_norm = df_normalized.groupby('Cluster').mean().reset_index()

# Preparar datos para radar
labels = features
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1] # Cerrar el círculo

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Dibujar cada clúster
colores = ['blue', 'orange', 'green', 'red']
nombres = ['0: Largo Alcance', '1: Congestión', '2: Eficiente', '3: Crítico']

for i, row in perfil_norm.iterrows():
    values = row[features].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, linestyle='solid', label=nombres[i], color=colores[i])
    ax.fill(angles, values, color=colores[i], alpha=0.1)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], labels)
plt.title("Perfil 'Personalidad' de cada Clúster (Normalizado)", y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
plt.savefig(os.path.join(ruta_script, 'radar_chart.png'))
print("3. Radar Chart generado.")