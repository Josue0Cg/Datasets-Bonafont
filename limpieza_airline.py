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