import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import os  # <--- Importante: Agregamos esto

# --- PASO 1: CARGAR DATOS (CORREGIDO) ---
print("--- Cargando datos de vuelos ---")

ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(ruta_script, 'flight_data_2024.csv')

print(f"Buscando archivo en: {ruta_csv}")

try:
    df = pd.read_csv(ruta_csv, low_memory=False)
    print(f"¡Archivo cargado! {df.shape[0]} registros encontrados.")
except FileNotFoundError:
    print("Error: Aún no se encuentra el archivo.")
    print("Verifica que el nombre sea exactamente 'flight_data_2024.csv'")
    exit()

features = ['dep_delay', 'arr_delay', 'taxi_out', 'distance', 'air_time']
df_cluster = df[features].dropna()

if len(df_cluster) > 50000:
    print(f"Dataset grande ({len(df_cluster)} filas). Tomando muestra de 50,000 para optimización.")
    df_cluster = df_cluster.sample(n=50000, random_state=42)

# --- PASO 2: ESTANDARIZACIÓN ---
print("--- Estandarizando datos ---")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster)

# --- PASO 3: DESARROLLO Y EVALUACIÓN (Iterar K) ---
print("--- Iniciando búsqueda del K óptimo (2 a 10 clústeres) ---")

results = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    
    score_silhouette = silhouette_score(X_scaled, labels)
    score_calinski = calinski_harabasz_score(X_scaled, labels)
    score_davies = davies_bouldin_score(X_scaled, labels)
    
    results.append({
        'K': k,
        'Silhouette': score_silhouette,
        'Calinski_Harabasz': score_calinski,
        'Davies_Bouldin': score_davies
    })
    print(f"K={k}: Silueta={score_silhouette:.3f}, Calinski={score_calinski:.1f}, Davies={score_davies:.3f}")
    
df_results = pd.DataFrame(results)

# --- PASO 4: VISUALIZACIÓN ---
print("--- Generando gráficas de evaluación ---")

fig, axes = plt.subplots(3, 1, figsize=(10, 15))

axes[0].plot(df_results['K'], df_results['Silhouette'], marker='o', color='teal')
axes[0].set_title('Coeficiente de Silueta (Más alto es mejor)')
axes[0].set_ylabel('Score')
axes[0].grid(True)
axes[1].plot(df_results['K'], df_results['Calinski_Harabasz'], marker='o', color='orange')
axes[1].set_title('Índice Calinski-Harabasz (Más alto es mejor)')
axes[1].set_ylabel('Score')
axes[1].grid(True)
axes[2].plot(df_results['K'], df_results['Davies_Bouldin'], marker='o', color='crimson')
axes[2].set_title('Índice Davies-Bouldin (Más bajo es mejor)')
axes[2].set_xlabel('Número de Clústeres (K)')
axes[2].set_ylabel('Score')
axes[2].grid(True)

plt.tight_layout()
ruta_imagen = os.path.join(ruta_script, 'evaluacion_clustering.png')
plt.savefig(ruta_imagen)
print(f"Gráfica guardada en: {ruta_imagen}")