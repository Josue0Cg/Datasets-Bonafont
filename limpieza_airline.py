import pandas as pd
import os

FILE_NAME = 'L_AIRLINE_ID_bruto.csv'
OUTPUT_NAME = 'L_AIRLINE_ID_limpio.csv'

try:
    df = pd.read_csv(FILE_NAME)
    print("Carga inicial exitosa. Filas:", len(df))
    print("\nColumnas antes de la limpieza:")
    print(df.head())
    print("\nInformación del DataFrame:")
    df.info()

except FileNotFoundError:
    print(f"ERROR: Archivo no encontrado en la ruta: {FILE_NAME}")
    exit()

# paso 1, renombrar las columnas
print("\n--- PASO 1: Renombrando Columnas ---")

df.rename(columns={'Code': 'AirlineID', 'Description': 'AirlineName'}, inplace=True)

print("Nuevas columnas:", df.columns.tolist())
print(df.head())

# paso 3, manejo de valores nulos y duplicados
print("\n--- PASO 2: Manejo de Nulos y Duplicados ---")

# nulos
nulos_antes = df.isnull().sum()
print("Nulos en AirlineName antes de limpiar:", nulos_antes['AirlineName'])

df.dropna(subset=['AirlineID', 'AirlineName'], inplace=True)

nulos_despues = df.isnull().sum()
print("Nulos en AirlineName despues de limpiar:", nulos_despues['AirlineName'])
print("Filas restantes después de eliminar nulos:", len(df))

# duplicados
duplicados_antes = df.duplicated().sum()
df.drop_duplicates(inplace=True)
duplicados_despues = df.duplicated().sum()

print(f"Se eliminaron {duplicados_antes - duplicados_despues} filas duplicadas.")

