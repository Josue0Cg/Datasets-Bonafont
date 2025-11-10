import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, PrecisionRecallDisplay, RocCurveDisplay
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

print("--- Iniciando el Análisis Supervisado de Vuelos ---")

# =============================================================================
# PASO 1: CARGAR Y PREPARAR DATOS
# =============================================================================
try:
    df = pd.read_csv('flight_data_2024.csv', low_memory=False)
    print(f"Datos cargados: {df.shape[0]} vuelos encontrados.")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'flights.csv'.")
    print("Asegúrate de que el archivo esté en la misma carpeta que este script.")
    exit()
df.dropna(subset=['arr_delay'], inplace=True)
print(f"Datos después de limpiar nulos en 'arr_delay': {df.shape[0]} vuelos.")
df = df.sample(n=500000, random_state=42)
print(f"Tomando una muestra aleatoria de {df.shape[0]} vuelos para entrenar.")

# =============================================================================
# PASO 2: INGENIERÍA DE CARACTERÍSTICAS 
# =============================================================================
df['_ARRDEL15'] = (df['arr_delay'] >= 15).astype(int)
print("Variable objetivo '_ARRDEL15' creada.")
print(df['_ARRDEL15'].value_counts(normalize=True))
features_numericas = ['dep_delay', 'taxi_out', 'distance', 'crs_elapsed_time']
features_categoricas = ['op_unique_carrier', 'origin', 'dest', 'month', 'day_of_week']

# =============================================================================
# PASO 3: DEFINIR (X) E (Y) Y DIVIDIR LOS DATOS
# =============================================================================
y = df['_ARRDEL15']
X = df[features_numericas + features_categoricas]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Datos divididos: {len(X_train)} para entrenar, {len(X_test)} para probar.")

# =============================================================================
# PASO 4: CREAR EL PIPELINE DE PREPROCESAMIENTO
# =============================================================================

transformador_numerico = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
transformador_categorico = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])
preprocesador = ColumnTransformer(
    transformers=[
        ('num', transformador_numerico, features_numericas),
        ('cat', transformador_categorico, features_categoricas)
    ],
    remainder='passthrough' # Deja pasar otras columnas si las hubiera
)

# =============================================================================
# PASO 5: CREAR Y ENTRENAR EL MODELO OPTIMIZADO
# =============================================================================
modelo_optimizado = ImbPipeline(steps=[
    ('preprocesador', preprocesador),
    ('smote', SMOTE(random_state=42)),
    ('clasificador', LogisticRegression(random_state=42, max_iter=1000))
])

print("\n--- Entrenando el Modelo Optimizado (con SMOTE)... ---")
modelo_optimizado.fit(X_train, y_train)
print("¡Entrenamiento completo!")

# =============================================================================
# PASO 6: EVALUAR Y GENERAR GRÁFICAS (¡Tu objetivo!)
# =============================================================================

y_pred = modelo_optimizado.predict(X_test)

print("\n--- REPORTE DE CLASIFICACIÓN (MÉTRICAS) ---")
print(classification_report(y_test, y_pred, target_names=['Puntual (0)', 'Retraso (1)']))
print("Generando Gráfica 1: Matriz de Confusión...")
fig, ax = plt.subplots()

ConfusionMatrixDisplay.from_estimator(
    modelo_optimizado,
    X_test,
    y_test,
    cmap='Blues', 
    ax=ax,
    display_labels=['Puntual', 'Retraso']
)
ax.set_title("Matriz de Confusión - Modelo Optimizado")
plt.savefig('grafica_matriz_confusion.png') 
print("Matriz guardada en 'grafica_matriz_confusion.png'")

print("Generando Gráfica 2: Curva Precision-Recall...")
fig, ax = plt.subplots()
PrecisionRecallDisplay.from_estimator(
    modelo_optimizado, X_test, y_test,
    ax=ax, name="Modelo Optimizado"
)
ax.set_title("Curva Precision-Recall (P-R)")
plt.savefig('grafica_curva_pr.png')
print("Curva P-R guardada en 'grafica_curva_pr.png'")

print("Generando Gráfica 3: Curva ROC...")
fig, ax = plt.subplots()
RocCurveDisplay.from_estimator(
    modelo_optimizado, X_test, y_test,
    ax=ax, name="Modelo Optimizado"
)
ax.set_title("Curva ROC y AUC")
plt.savefig('grafica_curva_roc.png')
print("Curva ROC guardada en 'grafica_curva_roc.png'")
print("\n--- ¡Proceso completado! ---")
print("Revisa los 3 archivos .png generados en la carpeta.")