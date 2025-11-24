import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- PASO 1: CARGAR DATOS CON CLÚSTERES ---
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(ruta_script, 'vuelos_con_clusters.csv')

try:
    df = pd.read_csv(ruta_csv)
    print("Datos cargados correctamente.")
except FileNotFoundError:
    print("Error: No se encuentra 'vuelos_con_clusters.csv'. Ejecuta el paso anterior primero.")
    exit()

# --- PASO 2: PERFILADO DE CLÚSTERES (ESTADÍSTICAS) ---
perfil = df.groupby('Cluster').mean().reset_index()
conteo = df['Cluster'].value_counts().sort_index()
perfil['Cantidad_Vuelos'] = conteo.values

print("\n--- PERFIL DE LOS GRUPOS DETECTADOS ---")
print(perfil.round(2).to_string())

# --- PASO 3: VISUALIZACIÓN DE PERFILES (BOXPLOTS) ---
plt.figure(figsize=(12, 5))
sns.boxplot(x='Cluster', y='arr_delay', data=df, showfliers=False)
plt.title('Distribución de Retrasos en la Llegada por Clúster')
plt.ylabel('Minutos de Retraso')
ruta_img = os.path.join(ruta_script, 'interpretacion_retrasos.png')
plt.savefig(ruta_img)
print(f"\nGráfica guardada en: {ruta_img}")
plt.figure(figsize=(12, 5))
sns.boxplot(x='Cluster', y='distance', data=df, showfliers=False)
plt.title('Distribución de Distancias por Clúster')
plt.ylabel('Millas')
ruta_img_dist = os.path.join(ruta_script, 'interpretacion_distancias.png')
plt.savefig(ruta_img_dist)
print(f"Gráfica guardada en: {ruta_img_dist}")