import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import os

# --- PASO 1: CARGA ROBUSTA ---
print("--- Carga de Datos ---")
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(ruta_script, 'flight_data_2024.csv')

try:
    df = pd.read_csv(ruta_csv, low_memory=False)
except FileNotFoundError:
    print("Error: No se encuentra 'flight_data_2024.csv'.")
    exit()

features = ['dep_delay', 'arr_delay', 'taxi_out', 'distance', 'air_time']
df_model = df[features].dropna()

if len(df_model) > 100000:
    df_model = df_model.sample(n=100000, random_state=42)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_model)

print("\n--- Optimizando Componentes PCA ---")
pca = PCA().fit(X_scaled)

varianza_acumulada = np.cumsum(pca.explained_variance_ratio_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(varianza_acumulada) + 1), varianza_acumulada, marker='o', linestyle='--')
plt.title('Varianza Explicada por Componentes PCA')
plt.xlabel('Número de Componentes')
plt.ylabel('Varianza Acumulada')
plt.axhline(y=0.85, color='r', linestyle='-', label='Umbral 85% Info')
plt.axhline(y=0.95, color='g', linestyle='-', label='Umbral 95% Info')
plt.legend()
plt.grid()
ruta_img_pca = os.path.join(ruta_script, 'optimizacion_pca.png')
plt.savefig(ruta_img_pca)
print(f"Gráfica de PCA guardada en: {ruta_img_pca}")

n_componentes_optimos = np.argmax(varianza_acumulada >= 0.90) + 1
print(f"-> Se necesitan {n_componentes_optimos} componentes para explicar el 90% de la varianza.")

# --- PASO 3: ENTRENAMIENTO DEL MODELO FINAL OPTIMIZADO ---
K_OPTIMO = 4  
print(f"\n--- Entrenando Modelo Final con K={K_OPTIMO} y PCA={n_componentes_optimos} ---")

pca_final = PCA(n_components=n_componentes_optimos)
X_pca = pca_final.fit_transform(X_scaled)

kmeans_final = KMeans(
    n_clusters=K_OPTIMO,
    init='k-means++',
    n_init=20,
    max_iter=500,
    random_state=42
)
cluster_labels = kmeans_final.fit_predict(X_pca)

df_model['Cluster'] = cluster_labels

print("¡Modelo optimizado entrenado exitosamente!")
print(df_model['Cluster'].value_counts())

ruta_resultado = os.path.join(ruta_script, 'vuelos_con_clusters.csv')
df_model.to_csv(ruta_resultado, index=False)
print(f"Datos etiquetados guardados en: {ruta_resultado}")